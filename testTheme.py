import wx

class ThemedFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Online Computer Store", size=(1000, 700))

        # Color Palette
        bg_color = wx.Colour("#D6EAF8")         # Light blue background
        header_color = wx.Colour("#003366")     # Dark blue for header text
        button_color = wx.Colour("#FFFFFF")     # Softer blue for buttons
        button_text = wx.Colour("#003366")

        # Panel and Sizer
        panel = wx.Panel(self)
        panel.SetBackgroundColour(bg_color)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="Online Computer Store")
        title_font = wx.Font(22, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour(header_color)
        vbox.Add(title, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 30)

        # Buttons
        button_labels = ["Registration & Management", "Online Sales", "Sale Statistics"]

        for label in button_labels:
            btn = wx.Button(panel, label=label, size=(250, 50))
            btn.SetBackgroundColour(button_color)
            btn.SetForegroundColour(button_text)
            btn.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            vbox.Add(btn, 0, wx.ALIGN_CENTER | wx.TOP, 15)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    ThemedFrame()
    app.MainLoop()
