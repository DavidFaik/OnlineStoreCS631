import wx

class MenuApplication(wx.Frame):
    def __init__(self, parent):
        #Main Window: 1) Registration + Management 2) Online Sales 3) Sale Statstics 
        super().__init__(parent, title="Online Computer Store", size=(1200, 800))    
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

        btn1 = wx.Button(mainWindow, label="Registration + Management", size=(250, 40))
        btn2 = wx.Button(mainWindow, label="Online Sales", size=(250, 40))
        btn3 = wx.Button(mainWindow, label="Sale Statistics", size=(250, 40))

        for btn, event in [(btn1, self.registrationAndManagement), (btn2, self.onlineSales), (btn3, self.saleStatistics)]:
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
        pass


    def saleStatistics(self, event):
        pass

class RegistrationAndManagement(wx.Frame):
    def __init__(self,parent):
        super().__init__(parent, title="Registration and Management", size=(1000, 700))

        BG_COLOR = wx.Colour("#D6EAF8")         
        FONT_COLOR = wx.Colour("#003366")     
        BUTTON_COLOR = wx.Colour("#FFFFFF")

        panel = wx.Panel(self)
        panel.SetBackgroundColour(BG_COLOR)
        regManBox = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(panel, label="Registration and Management")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(FONT_COLOR)
        regManBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)
        
        btn1 = wx.Button(panel, label="Register", size=(250, 40))
        btn2 = wx.Button(panel, label="Login", size=(250, 40))

        for btn, event in [(btn1, self.registrationInformation), (btn2, self.login)]:
            btn.SetBackgroundColour(BUTTON_COLOR)
            btn.SetForegroundColour(FONT_COLOR)
            btn.SetFont(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            regManBox.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
            btn.Bind(wx.EVT_BUTTON, event)
        
        panel.SetSizer(regManBox)
        self.Centre()

    def login(self, event):
        pass
        #btn1 = wx.Button(mainWindow, label="Registration Information", size=(250, 40))
        #btn2 = wx.Button(mainWindow, label="Credit Card Information", size=(250, 40))
        #btn3 = wx.Button(mainWindow, label="Shipping Address", size=(250, 40))

    def registrationInformation(self, event):
        pass
        #update registration information

# Run the app
if __name__ == "__main__":
    app = wx.App(False)
    MenuApplication(None)
    app.MainLoop()
