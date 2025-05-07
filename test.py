import wx
import wx.grid
import datetime
from DatabaseSchema import SQLConnections

class SaleStatistics(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Sale Statistics", size=(1400, 800))

        # Define colors as instance variables so they can be accessed in all methods
        self.BG_COLOR = wx.Colour("#68428D")      # Dark purple
        self.FONT_COLOR = wx.Colour("#C8A2E0")    # Light purple
        self.BUTTON_COLOR = wx.Colour("#FFFFFF")  # White

        # Database connection
        # You'll need to update these parameters with your actual credentials
        self.db = SQLConnections(host="localhost", user="root", password="KHlovesburton13!")

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(self.BG_COLOR)
        
        # Main vertical sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title section
        title_label = wx.StaticText(self.panel, label="Sale Statistics")
        title_font = wx.Font(24, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(self.FONT_COLOR)
        main_sizer.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)
        
        # Create a horizontal sizer for the three columns
        columns_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # First column - Labels
        labels_column = wx.BoxSizer(wx.VERTICAL)
        
        # Statistics labels
        labels = [
            "1) Total Amount Charged per Credit Card",
            "2) 10 Best Customers",
            "3) Most Frequently Sold Products",
            "4) Products Sold to Highest Number of Customers",
            "5) Maximum Basket Total per Credit Card",
            "6) Average Product Price Per Type"
        ]
        
        # Add statistics labels to first column
        for label in labels:
            stat_label = wx.StaticText(self.panel, label=label)
            stat_label.SetForegroundColour(self.FONT_COLOR)
            stat_label.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            labels_column.Add(stat_label, 0, wx.ALL | wx.EXPAND, 15)
        
        # Second column - Input fields
        inputs_column = wx.BoxSizer(wx.VERTICAL)
        
        # Placeholder for stats 1-2 (no inputs needed)
        for i in range(2):
            placeholder = wx.StaticText(self.panel, label="")
            inputs_column.Add(placeholder, 0, wx.ALL, 15)
        
        # Date inputs for stats 3-6
        for i in range(4):
            # Create a container for each statistic's inputs
            date_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            # Start date
            start_label = wx.StaticText(self.panel, label="Start:")
            start_label.SetForegroundColour(self.FONT_COLOR)
            date_sizer.Add(start_label, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
            
            start_date = wx.TextCtrl(self.panel, id=200+i*2, size=(100, -1))
            start_date.SetHint("YYYY-MM-DD")
            start_date.SetBackgroundColour(wx.Colour("#FFFFFF"))
            start_date.SetForegroundColour(wx.Colour("#000000"))
            date_sizer.Add(start_date, 0, wx.RIGHT, 10)
            
            # End date
            end_label = wx.StaticText(self.panel, label="End:")
            end_label.SetForegroundColour(self.FONT_COLOR)
            date_sizer.Add(end_label, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
            
            end_date = wx.TextCtrl(self.panel, id=201+i*2, size=(100, -1))
            end_date.SetHint("YYYY-MM-DD")
            end_date.SetBackgroundColour(wx.Colour("#FFFFFF"))
            end_date.SetForegroundColour(wx.Colour("#000000"))
            date_sizer.Add(end_date, 0, wx.RIGHT, 10)
            
            # Add date sizer to inputs column
            inputs_column.Add(date_sizer, 0, wx.ALL, 15)
        
        # Third column - Buttons
        buttons_column = wx.BoxSizer(wx.VERTICAL)
        
        # Add buttons for all stats
        for i in range(6):
            generate_button = wx.Button(self.panel, id=100+i, label="Generate Report", size=(150, 30))
            generate_button.SetBackgroundColour(self.BUTTON_COLOR)
            generate_button.SetForegroundColour(self.FONT_COLOR)
            buttons_column.Add(generate_button, 0, wx.ALL, 15)
        
        # Bind buttons to the general generate function
        column_data = [
            {"id": 1, "columns": ["Credit Card Number", "Total Amount"], "date_required": False},
            {"id": 2, "columns": ["CID", "FNAME", "LNAME" "TOTAL_SPENT"], "date_required": False},
            {"id": 3, "columns": ["Product ID", "Product Name", "Sales Count"], "date_required": True, "date_ids": [200, 201]},
            {"id": 4, "columns": ["Product ID", "Product Name", "Customer Count"], "date_required": True, "date_ids": [202, 203]},
            {"id": 5, "columns": ["Credit Card", "Maximum Basket Total"], "date_required": True, "date_ids": [204, 205]},
            {"id": 6, "columns": ["Product Type", "Average Price"], "date_required": True, "date_ids": [206, 207]}
        ]
        
        for i in range(6):
            self.FindWindowById(100+i).Bind(wx.EVT_BUTTON, 
                lambda event, stat_id=i+1, data=column_data[i]: 
                self.on_generate_stat(event, stat_id, data))
        
        # Add columns to the horizontal sizer
        columns_sizer.Add(labels_column, 1, wx.EXPAND | wx.LEFT, 20)
        columns_sizer.Add(inputs_column, 1, wx.EXPAND)
        columns_sizer.Add(buttons_column, 1, wx.EXPAND | wx.RIGHT, 20)
        
        # Add columns sizer to main sizer
        main_sizer.Add(columns_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Create grid for results
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(1, 1)
        self.grid.SetColLabelSize(30)
        self.grid.SetRowLabelSize(50)
        self.grid.SetLabelBackgroundColour(self.BG_COLOR)
        self.grid.SetLabelTextColour(self.FONT_COLOR)
        
        # Add grid to main sizer
        main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 20)
        
        # Set the main sizer for panel
        self.panel.SetSizer(main_sizer)
        self.Centre()
        self.Show()
        
    def clear_and_prepare_grid(self, col_count, col_names):
        """Clear existing grid content and prepare with new column names"""
        # Clear existing grid
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())
        if self.grid.GetNumberCols() > 0:
            self.grid.DeleteCols(0, self.grid.GetNumberCols())
            
        # Create new columns
        self.grid.AppendCols(col_count)
        
        # Set column labels
        for col_idx, col_name in enumerate(col_names):
            self.grid.SetColLabelValue(col_idx, col_name)
            
        # Refresh grid
        self.grid.ForceRefresh()
    
    def populate_grid(self, results):
        """Populate grid with query results"""
        if not results:
            self.grid.AppendRows(1)
            self.grid.SetCellValue(0, 0, "No results found")
            return
            
        # Add rows
        self.grid.AppendRows(len(results))
        
        # Populate grid with data
        for row_idx, row_data in enumerate(results):
            for col_idx, cell_value in enumerate(row_data):
                value = str(cell_value) if cell_value is not None else ""
                self.grid.SetCellValue(row_idx, col_idx, value)
                
        # Auto-size columns
        for col_idx in range(self.grid.GetNumberCols()):
            self.grid.AutoSizeColumn(col_idx)
    
    def validate_dates(self, start_ctrl_id, end_ctrl_id):
        """Validate date inputs"""
        start_ctrl = self.FindWindowById(start_ctrl_id)
        end_ctrl = self.FindWindowById(end_ctrl_id)
        
        start_date = start_ctrl.GetValue().strip()
        end_date = end_ctrl.GetValue().strip()
        
        # Basic validation - check if dates are provided
        if not start_date or not end_date:
            wx.MessageBox("Please enter both start and end dates", "Input Error", 
                          wx.OK | wx.ICON_ERROR)
            return None, None
        
        # You could add more sophisticated date validation here
        
        return start_date, end_date
    
    # General event handler for all statistics
    def on_generate_stat(self, event, stat_id, data):
        """General function to generate reports for any statistic"""
        
        # Prepare grid with appropriate columns
        self.clear_and_prepare_grid(len(data["columns"]), data["columns"])
        
        try:
            # If date input is required, validate and get dates
            if data["date_required"]:
                start_date, end_date = self.validate_dates(data["date_ids"][0], data["date_ids"][1])
                if not start_date:
                    return
                
                # Call appropriate database method with date parameters
                method_name = f"statistic_{stat_id}"
                if hasattr(self.db, method_name):
                    results = getattr(self.db, method_name)(start_date, end_date)
                else:
                    raise AttributeError(f"Database method {method_name} not found")
            else:
                # Call appropriate database method without parameters
                method_name = f"statistic_{stat_id}"
                if hasattr(self.db, method_name):
                    results = getattr(self.db, method_name)()
                else:
                    raise AttributeError(f"Database method {method_name} not found")
            
            # Populate grid with results
            self.populate_grid(results)
            
        except Exception as e:
            wx.MessageBox(f"Error generating report: {str(e)}", "Database Error", 
                          wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    frame = SaleStatistics(None)
    app.MainLoop()