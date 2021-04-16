# -*- coding: utf-8 -*-

import time
from datetime import datetime
import tkinter as tk
import requests

print("Starting program")

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes("-fullscreen", True)
        self.grid_columnconfigure(0, weight=200)

        self.bg = "#000000"
        self.fg = "#eeeeee"
        self.configure(bg=self.bg)

        self.time = time.time() - 70

        self.clock = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 50), text="hodiny")
        self.clock.grid(row=0, column=0, sticky="W")

        self.date = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="datum")
        self.date.grid(row=1, column=0, sticky="W")

        self.temp = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 40), text="teplota")
        self.temp.grid(row=0, column=1, sticky="NE")


        tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Pocitová teplota:").grid(sticky="W", column=0, row=2)
        self.feelsLike = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="pocitova")
        self.feelsLike.grid(row=2, column=1, sticky="W")

        tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Tlak:").grid(sticky="W", column=0, row=3)
        self.pressure = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="tlak")
        self.pressure.grid(row=3, column=1, sticky="W")

        tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Vlhkost:").grid(sticky="W", column=0, row=4)
        self.humidity = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="vlhkost")
        self.humidity.grid(row=4, column=1, sticky="W")

        tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Rychlost větru:").grid(sticky="W", column=0, row=5)
        self.wind = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="vitr")
        self.wind.grid(row=5, column=1, sticky="W")

        tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Východ Slunce:").grid(stick="W", column=0, row=6)
        self.rise = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="vychod")
        self.rise.grid(row=6, column=1, sticky="W")

        tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Západ Slunce:").grid(stick="W", column=0, row=7)
        self.set = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="zapad")
        self.set.grid(row=7, column=1, sticky="W")

        self.update_clock()

    def update_clock(self):
        now = datetime.now()

        self.clock.configure(text=now.strftime("%H:%M:%S"))
        self.date.configure(text=now.strftime("%d/%m/%Y"))

        if (time.time() - self.time >= 20):
            self.time = time.time()
            weather = self.getWeather()
            self.temp.configure(text=str(weather["main"]["temp"]) + u"\N{DEGREE SIGN}C")
            self.feelsLike.configure(text=str(weather["main"]["feels_like"]) + u"\N{DEGREE SIGN}C")
            self.pressure.configure(text=str(weather["main"]["pressure"]) + " hPa")
            self.humidity.configure(text=str(weather["main"]["humidity"]) + " %")
            self.wind.configure(text=str(weather["wind"]["speed"]) + " m/s")
            self.rise.configure(text=str(datetime.utcfromtimestamp(weather["sys"]["sunrise"]).strftime("%H:%M:%S")))
            self.set.configure(text=str(datetime.utcfromtimestamp(weather["sys"]["sunset"]).strftime("%H:%M:%S")))

        self.after(1000, self.update_clock)

    def getWeather(self):
        URL = "http://api.openweathermap.org/data/2.5/weather"

        location = "Domazlice"
        key = "518877fa5da8c9993824911a1185bc60"
        units = "metric"
        PARAMS = {"q":location, "appid":key, "units":units}
        r = requests.get(url = URL, params = PARAMS)
        return r.json()

    def getForecast(self):
        URL = "https://api.openweathermap.org/data/2.5/onecall"

        key = "e1e389c3f68fc6dbed6ae9b3f2f77e64"
        units = "metric"
        exclude = "minutely,hourly"
        lon = "13.38"
        lat = "49.75"

        PARAMS = {"lon":lon, "lat":lat, "appid":key, "units":units, "exclude":exclude}

        r = requests.get(url = URL, params = PARAMS)
        data = r.json()

if __name__== "__main__":
    print("Creating window")
    app = SampleApp()
    app.mainloop()
