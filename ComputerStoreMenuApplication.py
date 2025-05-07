# ComputerStoreMenuApplication.py for interface

import wx
import wx.grid as gridlib
from DatabaseSchema import SQLConnections

class MenuApplication(wx.Frame):
    def __init__(self, parent):
        #Main Window: 1) Registration + Management 2) Online Sales 3) Sale Statstics 
        super().__init__(parent, title="Online Computer Store", size=(500, 400))    
        BG_COLOR = wx.Colour("#D6EAF8")         
        FONT_COLOR = wx.Colour("#003366")     
        BUTTON_COLOR = wx.Colour("#FFFFFF")

        mainWindow = wx.Panel(self)
        mainWindow.SetBackgroundColour(BG_COLOR)
        mainBox = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(mainWindow, label="Online Computer Store")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(FONT_COLOR)
        mainBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

        main_menu_labels = [
            ("Registration + Management", self.registrationAndManagement), 
            ("Online Sales", self.onlineSales), 
            ("Sale Statistics", self.saleStatistics)
            ]
        
        for label, event in main_menu_labels:
            btn = wx.Button(mainWindow, label=label, size=(250, 40))
            btn.SetBackgroundColour(BUTTON_COLOR)
            btn.SetForegroundColour(FONT_COLOR)
            btn.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            mainBox.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
            btn.Bind(wx.EVT_BUTTON, event)

        mainWindow.SetSizer(mainBox)
        self.Centre()
        self.Show()
    
    def registrationAndManagement(self, event):
        reg_window = RegistrationAndManagement(self)
        reg_window.Show()

    def onlineSales(self, event):
        sales_window = OnlineSales(self)
        sales_window.Show()

    def saleStatistics(self, event):
        sales_statistics = SaleStatistics(self)
        sales_statistics.Show()

class RegistrationAndManagement(wx.Frame):
    def __init__(self,parent):
        super().__init__(parent, title="Registration and Management", size=(1000, 700))

        BG_COLOR = wx.Colour("#D6EAF8")         
        FONT_COLOR = wx.Colour("#003366")     
        BUTTON_COLOR = wx.Colour("#FFFFFF")

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BG_COLOR)
        self.regManBox = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(self.panel, label="Registration and Management")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(FONT_COLOR)
        self.regManBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)
        
        btn1 = wx.Button(self.panel, label="Register", size=(250, 40))
        btn2 = wx.Button(self.panel, label="Login", size=(250, 40))

        for btn, event in [(btn1, self.registrationInformation), (btn2, self.login)]:
            btn.SetBackgroundColour(BUTTON_COLOR)
            btn.SetForegroundColour(FONT_COLOR)
            btn.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            self.regManBox.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
            btn.Bind(wx.EVT_BUTTON, event)
        
        self.panel.SetSizer(self.regManBox)
        self.Centre()

    def login(self, event):
        self.regManBox.Clear(True)

        #btn1 = wx.Button(mainWindow, label="Registration Information", size=(250, 40))
        #btn2 = wx.Button(mainWindow, label="Credit Card Information", size=(250, 40))
        #btn3 = wx.Button(mainWindow, label="Shipping Address", size=(250, 40))

    def registrationInformation(self, event):
        self.regManBox.Clear(True)

        title_label = wx.StaticText(self.panel, label="Registration Information")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        self.regManBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

        form_sizer = wx.FlexGridSizer(rows=6, cols=2, vgap=15, hgap=10)
        form_sizer.AddGrowableCol(1, 1)  # Make the second column expandable
        
        # Text fields with labels
        field_labels = ["First Name:", "Last Name:", "Email:", "Address:", "Phone:"]
        self.form_fields = {}
        
        for label in field_labels:
            # Create the label
            text_label = wx.StaticText(self.panel, label=label)
            text_label.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            
            # Create the text input field
            field_name = label.replace(":", "").replace(" ", "_").lower()
            text_field = wx.TextCtrl(self.panel, size=(300, -1))
            self.form_fields[field_name] = text_field
            
            # Add to the form sizer
            form_sizer.Add(text_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
            form_sizer.Add(text_field, 0, wx.EXPAND)

class OnlineSales(wx.Frame):
    def __init__(self,parent):
        super().__init__(parent, title="Online Sales", size=(1000, 700))

        self.BG_COLOR = wx.Colour("#D6EAF8")         
        self.FONT_COLOR = wx.Colour("#003366")     
        self.BUTTON_COLOR = wx.Colour("#FFFFFF")

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(self.BG_COLOR)
        self.salesBox = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(self.panel, label="Registration and Management")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(self.FONT_COLOR)
        self.salesBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

class SaleStatistics(wx.Frame):
    def __init__(self,parent):
        super().__init__(parent, title="Sale Statistics", size=(1400, 800))
        self.db = SQLConnections(host="localhost", user="root", password="KHlovesburton13!")

        self.BG_COLOR = wx.Colour("#D6EAF8")         
        self.FONT_COLOR = wx.Colour("#003366")     
        self.BUTTON_COLOR = wx.Colour("#FFFFFF")

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(self.BG_COLOR)
        self.statistics_box = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(self.panel, label="Sale Statistics")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(self.FONT_COLOR)
        self.statistics_box.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

        columns_sizer = wx.BoxSizer(wx.HORIZONTAL)
        labels_column = wx.BoxSizer(wx.VERTICAL)

        statistic_labels = [
            "1) Total Amount Charged per Credit Card",
            "2) 10 Best Customers",
            "3) Most Frequently Sold Products",
            "4) Products Sold to Highest Number of Customers",
            "5) Maximum Basket Total per Credit Card",
            "6) Average Product Price Per Type"
        ]

        for label in statistic_labels:
            stat_label = wx.StaticText(self.panel, label=label)
            stat_label.SetForegroundColour(self.FONT_COLOR)
            stat_label.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            labels_column.Add(stat_label, 0, wx.ALL | wx.EXPAND, 15)
        
        inputs_column = wx.BoxSizer(wx.VERTICAL)
        for i in range(2):
            placeholder = wx.StaticText(self.panel, label="")
            inputs_column.Add(placeholder, 0, wx.ALL, 20)
        
        for i in range(4):
            date_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            start_label = wx.StaticText(self.panel, label="Start:")
            start_label.SetForegroundColour(self.FONT_COLOR)
            date_sizer.Add(start_label, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)
            
            start_date = wx.TextCtrl(self.panel, id=200+i*2, size=(100, -1))
            start_date.SetHint("YYYY-MM-DD")
            start_date.SetBackgroundColour(wx.Colour("#FFFFFF"))
            start_date.SetForegroundColour(wx.Colour("#000000"))
            date_sizer.Add(start_date, 0, wx.RIGHT, 10)
            
            end_label = wx.StaticText(self.panel, label="End:")
            end_label.SetForegroundColour(self.FONT_COLOR)
            date_sizer.Add(end_label, 0, wx.ALIGN_CENTER | wx.RIGHT, 15)
            
            end_date = wx.TextCtrl(self.panel, id=201+i*2, size=(100, -1))
            end_date.SetHint("YYYY-MM-DD")
            end_date.SetBackgroundColour(wx.Colour("#FFFFFF"))
            end_date.SetForegroundColour(wx.Colour("#000000"))
            date_sizer.Add(end_date, 0, wx.RIGHT, 10)
            
            inputs_column.Add(date_sizer, 0, wx.ALL, 15)

        buttons_column = wx.BoxSizer(wx.VERTICAL)
        for i in range(6):
            btn = wx.Button(self.panel, id=100+i, label=f"Generate Report {i+1}", size=(150, 30))
            btn.SetBackgroundColour(self.BUTTON_COLOR)
            btn.SetForegroundColour(self.FONT_COLOR)
            buttons_column.Add(btn, 0, wx.ALL, 15)

        column_data = [
            {"id": 1, "columns": ["CCCNUMBER", "TOTAL_CHARGED"], "date_required": False},
            {"id": 2, "columns": ["CID", "FNAME", "LNAME" "TOTAL_SPENT"], "date_required": False},
            {"id": 3, "columns": ["PID", "PNAME", "TOTAL_SOLD"], "date_required": True, "date_ids": [200, 201]},
            {"id": 4, "columns": ["PID", "PNAME", "NUM_CUSTOMERS"], "date_required": True, "date_ids": [202, 203]},
            {"id": 5, "columns": ["CCNUMBER", "MAX_BASKET_TOTAl"], "date_required": True, "date_ids": [204, 205]},
            {"id": 6, "columns": ["PTYPE", "AVG_AVG_SELLING_PRICE"], "date_required": True, "date_ids": [206, 207]}
        ]

        for i in range(6):
            self.FindWindowById(100+i).Bind(wx.EVT_BUTTON, 
                lambda event, stat_id=i+1, data=column_data[i]: 
                self.on_generate_stat(event, stat_id, data))

        columns_sizer.Add(labels_column, 1, wx.EXPAND | wx.LEFT, 20)
        columns_sizer.Add(inputs_column, 1, wx.EXPAND)
        columns_sizer.Add(buttons_column, 1, wx.EXPAND | wx.RIGHT, 20)
        
        self.statistics_box.Add(columns_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(1, 1)
        self.grid.SetColLabelSize(30)
        self.grid.SetRowLabelSize(50)
        self.grid.SetLabelBackgroundColour(self.BG_COLOR)
        self.grid.SetLabelTextColour(self.FONT_COLOR)
        
        self.statistics_box.Add(self.grid, 1, wx.EXPAND | wx.ALL, 20)
        self.panel.SetSizer(self.statistics_box)
        self.Centre()
        self.Show()
    
    def on_generate_stat(self, event, stat_id, data):
        """General function to generate reports for any statistic"""
        self.clear_grid(len(data["columns"]), data["columns"])
        
        try:
            if data["date_required"]:
                start_date = data["date_ids"][0]
                end_date = data["date_ids"][1]
                if not start_date:
                    return
                
                method_name = f"statistic_{stat_id}"
                if hasattr(self.db, method_name):
                    results = getattr(self.db, method_name)(start_date, end_date)
                else:
                    raise AttributeError(f"Database method {method_name} not found")
            else:
                method_name = f"statistic_{stat_id}"
                if hasattr(self.db, method_name):
                    results = getattr(self.db, method_name)()
                else:
                    raise AttributeError(f"Database method {method_name} not found")
            self.populate_grid(results)
            
        except Exception as e:
            wx.MessageBox(f"Error generating report: {str(e)}", "Database Error", 
                          wx.OK | wx.ICON_ERROR)

    def clear_grid(self, col_count, col_names):
        """Clear grid & set up with query column names"""
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())
        if self.grid.GetNumberCols() > 0:
            self.grid.DeleteCols(0, self.grid.GetNumberCols())
            
        self.grid.AppendCols(col_count)
        
        for col_idx, col_name in enumerate(col_names):
            self.grid.SetColLabelValue(col_idx, col_name)
            
        self.grid.ForceRefresh()

    def populate_grid(self, results):
        """Populate grid with query results"""
        if not results:
            self.grid.AppendRows(1)
            self.grid.SetCellValue(0, 0, "No results found")
            return
        
        self.grid.AppendRows(len(results))  

        for row_idx, row_data in enumerate(results):
            for col_idx, cell_value in enumerate(row_data):
                value = str(cell_value) if cell_value is not None else ""
                self.grid.SetCellValue(row_idx, col_idx, value)
            
        for row_idx, row_data in enumerate(results):
            for col_idx, cell_value in enumerate(row_data):
                value = str(cell_value) if cell_value is not None else ""
                self.grid.SetCellValue(row_idx, col_idx, value)
                
        for col_idx in range(self.grid.GetNumberCols()):
            self.grid.AutoSizeColumn(col_idx)

if __name__ == "__main__":
    app = wx.App(False)
    MenuApplication(None)
    app.MainLoop()
