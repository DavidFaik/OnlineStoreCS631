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

        BG_COLOR = wx.Colour("#D6EAF8")         
        FONT_COLOR = wx.Colour("#003366")     
        BUTTON_COLOR = wx.Colour("#FFFFFF")

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BG_COLOR)
        self.salesBox = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(self.panel, label="Registration and Management")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(FONT_COLOR)
        self.salesBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

class saleStatistics(wx.Frame):
    def __init__(self,parent):
        super().__init__(parent, title="Sale Statistics", size=(1000, 700))

        BG_COLOR = wx.Colour("#D6EAF8")         
        FONT_COLOR = wx.Colour("#003366")     
        BUTTON_COLOR = wx.Colour("#FFFFFF")

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BG_COLOR)
        self.statisticsBox = wx.BoxSizer(wx.VERTICAL)

        title_label = wx.StaticText(self.panel, label="Sale Statistics")
        title_font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(FONT_COLOR)
        self.statisticsBox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

if __name__ == "__main__":
    app = wx.App(False)
    MenuApplication(None)
    app.MainLoop()
