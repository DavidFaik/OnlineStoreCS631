import wx
import wx.grid as gridlib

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(5, 3)  # 5 rows, 3 columns

        # Optional: set some values
        self.grid.SetColLabelValue(0, "Name")
        self.grid.SetColLabelValue(1, "Age")
        self.grid.SetColLabelValue(2, "Occupation")

        self.grid.SetCellValue(0, 0, "Alice")
        self.grid.SetCellValue(0, 1, "30")
        self.grid.SetCellValue(0, 2, "Engineer")

        # Layout using sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(sizer)

        self.SetTitle("wxPython Grid Example")
        self.SetSize((400, 300))
        self.Centre()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
