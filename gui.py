import pickle
from pathlib import Path
from tkinter import *

SETTING_FILE = "setting.conf"


class MainWindow(Tk):
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

        self.show_label = Label(self, text="")
        self.show_label.pack()

        self.after(100, self.__show_point_xy)
    
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

    def __show_point_xy(self):
        self.show_label['text'] = f'x: {self.winfo_x()}, y: {self.winfo_y()}, width: {self.winfo_width()}, height: {self.winfo_height()}'
        self.after(100, self.__show_point_xy)


