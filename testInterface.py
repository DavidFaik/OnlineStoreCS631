import wx
import wx.grid
import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple

# Import our MySQL interface class
from mysql_python_interface import MySQLInterface


class MySQLConnectDialog(wx.Dialog):
    """Dialog for entering MySQL connection details"""
    
    def __init__(self, parent):
        super().__init__(parent, title="Connect to MySQL Database", size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Host input
        host_box = wx.BoxSizer(wx.HORIZONTAL)
        host_label = wx.StaticText(self.panel, label="Host:")
        self.host_input = wx.TextCtrl(self.panel, value="localhost")
        host_box.Add(host_label, flag=wx.RIGHT, border=8)
        host_box.Add(self.host_input, proportion=1)
        self.vbox.Add(host_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # User input
        user_box = wx.BoxSizer(wx.HORIZONTAL)
        user_label = wx.StaticText(self.panel, label="User:")
        self.user_input = wx.TextCtrl(self.panel, value="root")
        user_box.Add(user_label, flag=wx.RIGHT, border=8)
        user_box.Add(self.user_input, proportion=1)
        self.vbox.Add(user_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # Password input
        pass_box = wx.BoxSizer(wx.HORIZONTAL)
        pass_label = wx.StaticText(self.panel, label="Password:")
        self.pass_input = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        pass_box.Add(pass_label, flag=wx.RIGHT, border=8)
        pass_box.Add(self.pass_input, proportion=1)
        self.vbox.Add(pass_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # Database input
        db_box = wx.BoxSizer(wx.HORIZONTAL)
        db_label = wx.StaticText(self.panel, label="Database:")
        self.db_input = wx.TextCtrl(self.panel)
        db_box.Add(db_label, flag=wx.RIGHT, border=8)
        db_box.Add(self.db_input, proportion=1)
        self.vbox.Add(db_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        # Connect button
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        self.connect_btn = wx.Button(self.panel, label="Connect")
        self.cancel_btn = wx.Button(self.panel, label="Cancel")
        button_box.Add(self.connect_btn)
        button_box.Add(self.cancel_btn, flag=wx.LEFT, border=5)
        self.vbox.Add(button_box, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)
        
        # Bind events
        self.connect_btn.Bind(wx.EVT_BUTTON, self.on_connect)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
        
        self.panel.SetSizer(self.vbox)
        self.connection_info = None
    
    def on_connect(self, event):
        """Handle the connect button click"""
        self.connection_info = {
            "host": self.host_input.GetValue(),
            "user": self.user_input.GetValue(),
            "password": self.pass_input.GetValue(),
            "database": self.db_input.GetValue()
        }
        self.EndModal(wx.ID_OK)
    
    def on_cancel(self, event):
        """Handle the cancel button click"""
        self.EndModal(wx.ID_CANCEL)
    
    def get_connection_info(self):
        """Return the entered connection information"""
        return self.connection_info


class QueryPanel(wx.Panel):
    """Panel for entering and executing SQL queries"""
    
    def __init__(self, parent, db_interface):
        super().__init__(parent)
        
        self.db = db_interface
        
        # Create main vertical sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Query label
        query_label = wx.StaticText(self, label="Enter SQL Query:")
        vbox.Add(query_label, flag=wx.LEFT | wx.TOP, border=10)
        
        # Query text input
        self.query_input = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
        vbox.Add(self.query_input, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=0)
        
        # Buttons horizontal box
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Execute query button
        self.execute_btn = wx.Button(self, label="Execute Query")
        self.execute_btn.Bind(wx.EVT_BUTTON, self.on_execute)
        button_box.Add(self.execute_btn)
        
        # Show tables button
        self.tables_btn = wx.Button(self, label="Show Tables")
        self.tables_btn.Bind(wx.EVT_BUTTON, self.on_show_tables)
        button_box.Add(self.tables_btn, flag=wx.LEFT, border=10)
        
        # Clear results button
        self.clear_btn = wx.Button(self, label="Clear Results")
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear_results)
        button_box.Add(self.clear_btn, flag=wx.LEFT, border=10)
        
        vbox.Add(button_box, flag=wx.ALIGN_LEFT | wx.LEFT | wx.TOP | wx.BOTTOM, border=10)
        
        # Results label
        results_label = wx.StaticText(self, label="Results:")
        vbox.Add(results_label, flag=wx.LEFT | wx.TOP, border=10)
        
        # Status text
        self.status_text = wx.StaticText(self, label="")
        vbox.Add(self.status_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        # Grid for displaying results
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(1, 1)
        vbox.Add(self.grid, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        
        self.SetSizer(vbox)
    
    def on_execute(self, event):
        """Execute the SQL query and display results"""
        query = self.query_input.GetValue().strip()
        
        if not query:
            wx.MessageBox("Please enter a SQL query", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        try:
            # Check if it's a SELECT query
            is_select = query.lower().strip().startswith("select")
            
            if is_select:
                df = self.db.fetch_as_dataframe(query)
                self.display_dataframe(df)
                row_count = len(df)
                self.status_text.SetLabel(f"Query executed successfully. {row_count} rows returned.")
            else:
                success = self.db.execute_query(query)
                if success:
                    self.status_text.SetLabel("Query executed successfully. No results to display.")
                    # Clear the grid
                    self.clear_grid()
                else:
                    self.status_text.SetLabel("Query execution failed.")
        
        except Exception as e:
            wx.MessageBox(f"Error executing query: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            self.status_text.SetLabel(f"Error: {str(e)}")
    
    def on_show_tables(self, event):
        """Show all tables in the current database"""
        try:
            df = self.db.fetch_as_dataframe("SHOW TABLES")
            self.display_dataframe(df)
            self.status_text.SetLabel(f"Retrieved {len(df)} tables")
        except Exception as e:
            wx.MessageBox(f"Error retrieving tables: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
            self.status_text.SetLabel(f"Error: {str(e)}")
    
    def on_clear_results(self, event):
        """Clear the results grid"""
        self.clear_grid()
        self.status_text.SetLabel("")
    
    def clear_grid(self):
        """Clear the grid display"""
        if self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows(0, self.grid.GetNumberRows())
        if self.grid.GetNumberCols() > 0:
            self.grid.DeleteCols(0, self.grid.GetNumberCols())
    
    def display_dataframe(self, df):
        """Display a pandas DataFrame in the grid"""
        # Clear existing grid
        self.clear_grid()
        
        if df.empty:
            self.grid.AppendRows(1)
            self.grid.AppendCols(1)
            self.grid.SetCellValue(0, 0, "No data returned")
            return
        
        # Create new grid with proper dimensions
        num_rows, num_cols = df.shape
        self.grid.AppendRows(num_rows)
        self.grid.AppendCols(num_cols)
        
        # Set column headers
        for col_idx, col_name in enumerate(df.columns):
            self.grid.SetColLabelValue(col_idx, str(col_name))
        
        # Fill data
        for row_idx, row in df.iterrows():
            for col_idx, col_name in enumerate(df.columns):
                value = row[col_name]
                self.grid.SetCellValue(row_idx, col_idx, str(value))
        
        # Auto-size columns
        self.grid.AutoSizeColumns()


class TableEditorPanel(wx.Panel):
    """Panel for creating and modifying tables"""
    
    def __init__(self, parent, db_interface):
        super().__init__(parent)
        
        self.db = db_interface
        
        # Create main vertical sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Create a notebook for tabs
        self.notebook = wx.Notebook(self)
        vbox.Add(self.notebook, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Create Table tab
        self.create_tab = wx.Panel(self.notebook)
        self.notebook.AddPage(self.create_tab, "Create Table")
        
        # Insert Data tab
        self.insert_tab = wx.Panel(self.notebook)
        self.notebook.AddPage(self.insert_tab, "Insert Data")
        
        # Set up Create Table tab
        self.setup_create_table_tab()
        
        # Set up Insert Data tab
        self.setup_insert_data_tab()
        
        self.SetSizer(vbox)
    
    def setup_create_table_tab(self):
        """Set up the Create Table tab"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Table name input
        table_box = wx.BoxSizer(wx.HORIZONTAL)
        table_label = wx.StaticText(self.create_tab, label="Table Name:")
        self.table_name_input = wx.TextCtrl(self.create_tab)
        table_box.Add(table_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        table_box.Add(self.table_name_input, proportion=1)
        vbox.Add(table_box, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Column definition section
        columns_label = wx.StaticText(self.create_tab, label="Define Columns:")
        vbox.Add(columns_label, flag=wx.LEFT | wx.TOP, border=10)
        
        # List control for columns
        column_list_box = wx.BoxSizer(wx.HORIZONTAL)
        self.column_list = wx.ListCtrl(self.create_tab, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.column_list.InsertColumn(0, "Column Name", width=150)
        self.column_list.InsertColumn(1, "Data Type", width=150)
        self.column_list.InsertColumn(2, "Primary Key", width=100)
        column_list_box.Add(self.column_list, proportion=1, flag=wx.EXPAND)
        vbox.Add(column_list_box, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        # Add column section
        add_column_box = wx.BoxSizer(wx.HORIZONTAL)
        
        # Column name input
        col_name_label = wx.StaticText(self.create_tab, label="Name:")
        self.col_name_input = wx.TextCtrl(self.create_tab)
        add_column_box.Add(col_name_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        add_column_box.Add(self.col_name_input, proportion=1, flag=wx.RIGHT, border=10)
        
        # Data type selection
        data_types = ["INT", "VARCHAR(255)", "TEXT", "DATE", "DECIMAL(10,2)", "BOOLEAN"]
        type_label = wx.StaticText(self.create_tab, label="Type:")
        self.type_choice = wx.Choice(self.create_tab, choices=data_types)
        self.type_choice.SetSelection(0)
        add_column_box.Add(type_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=5)
        add_column_box.Add(self.type_choice, flag=wx.RIGHT, border=10)
        
        # Primary key checkbox
        self.pk_checkbox = wx.CheckBox(self.create_tab, label="Primary Key")
        add_column_box.Add(self.pk_checkbox)
        
        vbox.Add(add_column_box, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Add Column / Create Table buttons
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self.add_column_btn = wx.Button(self.create_tab, label="Add Column")
        self.add_column_btn.Bind(wx.EVT_BUTTON, self.on_add_column)
        button_box.Add(self.add_column_btn)
        
        self.remove_column_btn = wx.Button(self.create_tab, label="Remove Column")
        self.remove_column_btn.Bind(wx.EVT_BUTTON, self.on_remove_column)
        button_box.Add(self.remove_column_btn, flag=wx.LEFT, border=10)
        
        self.create_table_btn = wx.Button(self.create_tab, label="Create Table")
        self.create_table_btn.Bind(wx.EVT_BUTTON, self.on_create_table)
        button_box.Add(self.create_table_btn, flag=wx.LEFT, border=10)
        
        vbox.Add(button_box, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)
        
        self.create_tab.SetSizer(vbox)
    
    def setup_insert_data_tab(self):
        """Set up the Insert Data tab"""
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Table selection
        table_box = wx.BoxSizer(wx.HORIZONTAL)
        table_label = wx.StaticText(self.insert_tab, label="Select Table:")
        self.table_choice = wx.Choice(self.insert_tab, choices=[])
        self.refresh_table_btn = wx.Button(self.insert_tab, label="Refresh")
        self.refresh_table_btn.Bind(wx.EVT_BUTTON, self.on_refresh_tables)
        
        table_box.Add(table_label, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
        table_box.Add(self.table_choice, proportion=1, flag=wx.RIGHT, border=10)
        table_box.Add(self.refresh_table_btn)
        
        vbox.Add(table_box, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Load table schema button
        self.load_schema_btn = wx.Button(self.insert_tab, label="Load Table Schema")
        self.load_schema_btn.Bind(wx.EVT_BUTTON, self.on_load_schema)
        vbox.Add(self.load_schema_btn, flag=wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, border=10)
        
        # Column inputs
        self.column_panel = wx.ScrolledWindow(self.insert_tab)
        self.column_panel.SetScrollRate(0, 10)
        self.column_sizer = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        self.column_sizer.AddGrowableCol(1, 1)
        self.column_panel.SetSizer(self.column_sizer)
        
        vbox.Add(self.column_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Insert Data button
        self.insert_data_btn = wx.Button(self.insert_tab, label="Insert Data")
        self.insert_data_btn.Bind(wx.EVT_BUTTON, self.on_insert_data)
        vbox.Add(self.insert_data_btn, flag=wx.ALIGN_RIGHT | wx.ALL, border=10)
        
        self.insert_tab.SetSizer(vbox)
        
        # Call refresh tables to populate the dropdown
        self.on_refresh_tables(None)
    
    def on_add_column(self, event):
        """Add a column to the list"""
        col_name = self.col_name_input.GetValue().strip()
        data_type = self.type_choice.GetString(self.type_choice.GetSelection())
        is_pk = "Yes" if self.pk_checkbox.GetValue() else "No"
        
        if not col_name:
            wx.MessageBox("Please enter a column name", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        # Add to list control
        idx = self.column_list.GetItemCount()
        self.column_list.InsertItem(idx, col_name)
        self.column_list.SetItem(idx, 1, data_type)
        self.column_list.SetItem(idx, 2, is_pk)
        
        # Clear inputs
        self.col_name_input.SetValue("")
        self.type_choice.SetSelection(0)
        self.pk_checkbox.SetValue(False)
    
    def on_remove_column(self, event):
        """Remove selected column from the list"""
        selected = self.column_list.GetFirstSelected()
        if selected != -1:
            self.column_list.DeleteItem(selected)
    
    def on_create_table(self, event):
        """Create a new table in the database"""
        table_name = self.table_name_input.GetValue().strip()
        
        if not table_name:
            wx.MessageBox("Please enter a table name", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if self.column_list.GetItemCount() == 0:
            wx.MessageBox("Please add at least one column", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        # Build column definitions dictionary
        columns = {}
        primary_key = None
        
        for i in range(self.column_list.GetItemCount()):
            col_name = self.column_list.GetItemText(i, 0)
            data_type = self.column_list.GetItemText(i, 1)
            is_pk = self.column_list.GetItemText(i, 2) == "Yes"
            
            # Add AUTO_INCREMENT to primary key INT columns
            if is_pk and data_type == "INT":
                data_type += " AUTO_INCREMENT"
                primary_key = col_name
            elif is_pk:
                primary_key = col_name
            
            columns[col_name] = data_type
        
        # Create the table
        success = self.db.create_table(table_name, columns, primary_key)
        
        if success:
            wx.MessageBox(f"Table '{table_name}' created successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            self.table_name_input.SetValue("")
            self.column_list.DeleteAllItems()
            
            # Refresh tables list in insert tab
            self.on_refresh_tables(None)
        else:
            wx.MessageBox("Failed to create table", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_refresh_tables(self, event):
        """Refresh the list of tables in the database"""
        try:
            df = self.db.fetch_as_dataframe("SHOW TABLES")
            
            # Get the first column name
            if df.empty or len(df.columns) == 0:
                tables = []
            else:
                col_name = df.columns[0]
                tables = df[col_name].tolist()
            
            # Update choice control
            self.table_choice.Clear()
            for table in tables:
                self.table_choice.Append(table)
            
            if tables:
                self.table_choice.SetSelection(0)
        
        except Exception as e:
            wx.MessageBox(f"Error refreshing tables: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_load_schema(self, event):
        """Load table schema for the selected table"""
        if self.table_choice.GetSelection() == -1:
            wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        table_name = self.table_choice.GetString(self.table_choice.GetSelection())
        
        try:
            # Get column information
            columns = self.db.get_column_names(table_name)
            
            # Clear existing fields
            self.column_sizer.Clear(True)
            self.column_inputs = []
            
            # Create input fields for each column
            for col in columns:
                label = wx.StaticText(self.column_panel, label=f"{col}:")
                text_ctrl = wx.TextCtrl(self.column_panel)
                
                self.column_sizer.Add(label, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
                self.column_sizer.Add(text_ctrl, flag=wx.EXPAND)
                
                self.column_inputs.append((col, text_ctrl))
            
            self.column_panel.Layout()
            self.column_panel.FitInside()
            
        except Exception as e:
            wx.MessageBox(f"Error loading schema: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
    
    def on_insert_data(self, event):
        """Insert data into the selected table"""
        if self.table_choice.GetSelection() == -1:
            wx.MessageBox("Please select a table", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        if not hasattr(self, 'column_inputs') or not self.column_inputs:
            wx.MessageBox("Please load the table schema first", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        table_name = self.table_choice.GetString(self.table_choice.GetSelection())
        
        # Build data dictionary from inputs
        data = {}
        for col, ctrl in self.column_inputs:
            value = ctrl.GetValue().strip()
            if value:  # Only add non-empty values
                data[col] = value
        
        if not data:
            wx.MessageBox("Please enter at least one value", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        # Insert the data
        success = self.db.insert_row(table_name, data)
        
        if success:
            wx.MessageBox("Data inserted successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            
            # Clear input fields
            for _, ctrl in self.column_inputs:
                ctrl.SetValue("")
        else:
            wx.MessageBox("Failed to insert data", "Error", wx.OK | wx.ICON_ERROR)


class MySQLGUIApp(wx.Frame):
    """Main application frame"""
    
    def __init__(self):
        super().__init__(None, title="MySQL Database GUI", size=(900, 700))
        
        self.db = None
        
        # Create a status bar
        self.CreateStatusBar()
        self.SetStatusText("Not connected to database")
        
        # Create menu bar
        menubar = wx.MenuBar()
        
        # File menu
        file_menu = wx.Menu()
        connect_item = file_menu.Append(wx.ID_ANY, "&Connect to Database", "Connect to MySQL database")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "E&xit", "Exit application")
        
        menubar.Append(file_menu, "&File")
        self.SetMenuBar(menubar)
        
        # Bind menu events
        self.Bind(wx.EVT_MENU, self.on_connect, connect_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        
        # Create notebook for tabs
        self.notebook = wx.Notebook(self)
        
        # Initially disable the notebook until connected
        self.notebook.Enable(False)
        
        # Add tabs once the database is connected
        
        # Close event
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        
        # Connect dialog on startup
        wx.CallAfter(self.on_connect, None)
    
    def on_connect(self, event):
        """Show dialog to connect to database"""
        connect_dialog = MySQLConnectDialog(self)
        
        if connect_dialog.ShowModal() == wx.ID_OK:
            connection_info = connect_dialog.get_connection_info()
            
            # Create MySQL interface
            self.db = MySQLInterface(
                host=connection_info["host"],
                user=connection_info["user"],
                password=connection_info["password"],
                database=connection_info["database"]
            )
            
            # Try to connect
            if self.db.connect():
                self.SetStatusText(f"Connected to {connection_info['database']} on {connection_info['host']}")
                
                # Enable and setup notebook
                self.notebook.Enable(True)
                
                # Clear existing pages
                while self.notebook.GetPageCount() > 0:
                    self.notebook.DeletePage(0)
                
                # Add tabs
                self.query_panel = QueryPanel(self.notebook, self.db)
                self.notebook.AddPage(self.query_panel, "Query Database")
                
                self.table_editor = TableEditorPanel(self.notebook, self.db)
                self.notebook.AddPage(self.table_editor, "Table Editor")
                
                # Add notebook to layout if not already added
                if not hasattr(self, 'sizer'):
                    self.sizer = wx.BoxSizer()
                    self.sizer.Add(self.notebook, proportion=1, flag=wx.EXPAND)
                    self.SetSizer(self.sizer)
            else:
                wx.MessageBox("Failed to connect to the database", "Connection Error", wx.OK | wx.ICON_ERROR)
        
        connect_dialog.Destroy()
    
    def on_exit(self, event):
        """Handle application exit"""
        # Close database connection if exists
        if self.db:
            self.db.disconnect()
        
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = MySQLGUIApp()
    frame.Show()
    app.MainLoop()