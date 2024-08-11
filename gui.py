import pickle
from pathlib import Path
from tkinter import *
from tkinter import ttk

SETTING_FILE = "setting.conf"


class RootWindow(Tk):
    def __init__(
            self,
            title: str = "Main window",
            screenName: str | None = None,
            baseName: str | None = None,
            className: str = "Tkk",
            useTk: bool = True,
            sync: bool = False,
            use: str | None = None
            ) -> None:
        

        super().__init__(
            screenName,
            baseName,
            className,
            useTk,
            sync,
            use
            )
        
        self.title(title)
        self.__load_setting()

        self.protocol("WM_DELETE_WINDOW", self.__on_closing)


    
    def __save_setting(self) -> None:
        setting = {
            'width': self.winfo_width(),
            'height': self.winfo_height(),
            'x': self.winfo_x(),
            'y': self.winfo_y()
        }
        
        with open(SETTING_FILE, "bw") as file:
            pickle.dump(setting, file)

    def __load_setting(self) -> dict:
        self.attributes("-topmost", True)

        

        if Path(SETTING_FILE).exists():
            with open(SETTING_FILE, "br") as file:
                setting = pickle.load(file)

            width = setting['width']
            height = setting['height']
            x = setting['x']
            y = setting['y']

            if x < 0 or x > self.winfo_screenwidth() - width:
                x = int(self.winfo_screenwidth() / 2 - width / 2)

            if y < 0 or y > self.winfo_screenheight() - height:
                y = int(self.winfo_screenheight() / 2 - height / 2)

            self.geometry(
                f"{width}x{height}+{x}+{y}"
                )
        else:
            width = 400
            height = 500
            x = int(self.winfo_screenwidth() / 2 - width / 2)
            y = int(self.winfo_screenheight() / 2 - height / 2)
            self.geometry(
                f"{width}x{height}+{x}+{y}"
                )

    def __on_closing(self):
        self.__save_setting()
        self.destroy()


class ParserApp(RootWindow):
    def __init__(self,
                 title: str = "Parser",
                 screenName: str | None = None,
                 baseName: str | None = None,
                 className: str = "Tkk",
                 useTk: bool = True,
                 sync: bool = False,
                 use: str | None = None
                 ) -> None:

        super().__init__(title,
                         screenName,
                         baseName,
                         className,
                         useTk,
                         sync,
                         use)
        

        style = ttk.Style()
        style.configure("Main.TFrame", background="red")
        style.configure("Panel.TFrame", background="green")
        style.configure("LogText.TFrame", background="grey")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mainFrame = ttk.Frame(self, padding=(5,5,5,5), style="Main.TFrame")
        self.mainFrame.grid(column=0, row=0, sticky=(N, S, E, W))

        self.mainFrame.grid_rowconfigure(1, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)

        self.panel = ttk.Frame(self.mainFrame, height=50, width=-1, style="Panel.TFrame")
        self.panel.grid(column=0, row=0, sticky=(E, W))
        
        
        self.logText = ttk.Frame(self.mainFrame, height=50, style="LogText.TFrame")
        self.logText.grid(column=0, row=2, sticky=(E, W))
        