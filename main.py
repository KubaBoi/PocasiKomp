# -*- coding: utf-8 -*-

import time
from datetime import datetime
import tkinter as tk

print("Starting program")

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes("-fullscreen", True)
        self.grid_columnconfigure(0, weight=200)

        self.bg = "#000000"
        self.fg = "#eeeeee"
        self.configure(bg=self.bg)

        self.time = datetime.strptime("24/12/20 21:00:00", "%d/%m/%y %H:%M:%S")

        tk.Label(self, bg=self.bg, fg= self.fg, font=("Arial", 20), text="Do zprovoznění dárku\nAge Of Empires II Definitive edition\nzbývá:").grid(row=0, column=0)

        self.clock = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 50), text="hodiny")
        self.clock.grid(row=1, column=0)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()

        remaining = str(self.time - now).split(".")[0]
        self.clock.configure(text="T - " + remaining)

        hour = int(now.strftime("%H"))
        if (hour >= 21):
                remaining = str(now - self.time).split(".")[0]
                self.clock.configure(text="T + " + remaining)
                tk.Label(self, font=("Arial", 20), fg="green", bg=self.bg, text="Aktivováno").grid(row=2, column=0)

        self.after(1000, self.update_clock)

if __name__== "__main__":
    print("Creating window")
    app = SampleApp()
    app.mainloop()
