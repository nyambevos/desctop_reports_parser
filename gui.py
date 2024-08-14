from typing import Literal, Callable
import pickle
from pathlib import Path
from tkinter import *
from tkinter import Misc, ttk

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
        # style.theme_use('alt')
        style.configure("Main.TFrame", background="red")
        style.configure("Panel.TFrame", background="green")
        style.configure("LogText.TFrame", background="grey")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mainFrame = ttk.Frame(self, padding=(5,5,5,5), style="Main.TFrame")
        self.mainFrame.grid(column=0, row=0, sticky=(N, S, E, W))

        self.mainFrame.grid_rowconfigure(1, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        
        self.logTextPanel = LogTextPanel(self.mainFrame, height=120)
        self.logTextPanel.grid(column=0, row=2, sticky=(E, W))

        self.buttomPanel = ButtomPanel(self.mainFrame, output_frame=self.logTextPanel, style="Panel.TFrame")
        self.buttomPanel.grid(column=0, row=0, sticky=(E, W))


class LogTextPanel(ttk.Frame):
    def __init__(
            self,
            master: Misc | None = None,
            *,
            border: str | float = "",
            borderwidth: str | float = "",
            class_: str = "",
            cursor: str | tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str] = "",
            height: str | float = 0,
            name: str = "",
            padding: str | float | tuple[str | float] | tuple[str | float, str | float] | tuple[str | float, str | float, str | float] | tuple[str | float, str | float, str | float, str | float] = "",
            relief: Literal['raised'] | Literal['sunken'] | Literal['flat'] | Literal['ridge'] | Literal['solid'] | Literal['groove'] = 'flat',
            style: str = "",
            takefocus: bool | Callable[[str], bool | None] | Literal[0] | Literal[1] | Literal[''] = "",
            width: str | float = 0
            ) -> None:
        super().__init__(
            master,
            border=border,
            borderwidth=borderwidth,
            class_=class_,
            cursor=cursor,
            height=height,
            name=name,
            padding=padding,
            relief=relief,
            style=style,
            takefocus=takefocus,
            width=width
            )
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.logText = Text(self, highlightthickness=1, highlightcolor='gray', wrap="word", borderwidth=5)
        self.logText.grid(column=0, row=0, sticky=(E, W))

        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.logText.yview)
        self.scrollbar.grid(column=1, row=0, sticky=(N,S))
        self.logText['yscrollcommand'] = self.scrollbar.set

        
    
    def print(self, string: str) -> None:
        self.logText.config(state="normal")
        self.logText.insert("end", string)
        self.logText.config(state="disabled")
        self.logText.see("end")


class ButtomPanel(ttk.Frame):
    def __init__(
            self,
            master: Misc | None = None,
            output_frame: LogTextPanel = None,
            *args,
            **kwargs
            ) -> None:
        super().__init__(
            master,
            *args,
            **kwargs
            )
        self.output_frame = output_frame

        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(9, weight=1)

        self.accountButton = ttk.Button(self, text="Google", width=5, command=self.print_log)
        self.accountButton.grid(column=10, row=0)

    def print_log(self):
        self.output_frame.print("Test working the buttom\n")