import wx
import mysql.connector

class SchemaViewer(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(700, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "Table")
        self.list_ctrl.InsertColumn(1, "Column")
        self.list_ctrl.InsertColumn(2, "Type")
        self.list_ctrl.InsertColumn(3, "Nullable")
        self.list_ctrl.InsertColumn(4, "Key")

        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(vbox)

        self.fetch_schema()

        self.Centre()
        self.Show()

    def fetch_schema(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="KHlovesburton13!",
            database="OnlineStoreDB"
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            for row in cursor.fetchall():
                index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), table)
                self.list_ctrl.SetItem(index, 1, row[0])  # Column name
                self.list_ctrl.SetItem(index, 2, row[1])  # Type
                self.list_ctrl.SetItem(index, 3, row[2])  # Nullable
                self.list_ctrl.SetItem(index, 4, row[3])  # Key

        cursor.close()
        conn.close()

# Run the app
if __name__ == "__main__":
    app = wx.App(False)
    SchemaViewer(None, "MySQL Schema Viewer")
    app.MainLoop()
