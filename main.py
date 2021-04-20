# -*- coding: utf-8 -*-

import time
from datetime import datetime
import tkinter as tk
import requests
from subprocess import call, check_output
from player import BluePlayer

print("Starting program")

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes("-fullscreen", True)
        self.grid_columnconfigure(0, weight=200)

        self.player = BluePlayer()
        self.player.start()

        """
        0 - weather
        1 - bluetooth
        """
        self.show = 0 #stav obrazovky
        self.countShow = 2 #pocet obrazovek
        self.showCounter = 0 #doba trvani obrazovky
        self.showFrequency = 1 #doba stridani obrazovek

        self.bg = "#000000"
        self.fg = "#eeeeee"
        self.configure(bg=self.bg)

        self.time = time.time() - 70

        self.clock = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 50), text="hodiny")
        self.clock.grid(row=0, column=0, sticky="W")

        self.temp = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 40), text="teplota")
        self.temp.grid(row=0, column=1, sticky="NE")

        self.date = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="datum")
        self.date.grid(row=1, column=0, sticky="W")

        self.song = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="song")
        self.song.grid(row=1, column=1, sticky="W")


        self.feelsLikeL = tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Pocitová teplota:")
        self.feelsLikeL.grid(sticky="W", column=0, row=2)
        self.feelsLike = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="pocitova")
        self.feelsLike.grid(row=2, column=1, sticky="W")

        self.pressureL = tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Tlak:")
        self.pressureL.grid(sticky="W", column=0, row=3)
        self.pressure = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="tlak")
        self.pressure.grid(row=3, column=1, sticky="W")

        self.humidityL = tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Vlhkost:")
        self.humidityL.grid(sticky="W", column=0, row=4)
        self.humidity = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="vlhkost")
        self.humidity.grid(row=4, column=1, sticky="W")

        self.windL = tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Rychlost větru:")
        self.windL.grid(sticky="W", column=0, row=5)
        self.wind = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="vitr")
        self.wind.grid(row=5, column=1, sticky="W")

        self.riseL = tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Východ Slunce:")
        self.riseL.grid(stick="W", column=0, row=6)
        self.rise = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="vychod")
        self.rise.grid(row=6, column=1, sticky="W")

        self.setL = tk.Label(self, font=("Arial", 15), bg=self.bg, fg=self.fg, text="Západ Slunce:")
        self.setL.grid(stick="W", column=0, row=7)
        self.set = tk.Label(self, bg=self.bg, fg=self.fg, font=("Arial", 20), text="zapad")
        self.set.grid(row=7, column=1, sticky="W")

        self.update_clock()

    def update_clock(self):
        now = datetime.now()

        self.clock.configure(text=now.strftime("%H:%M:%S"))
        self.date.configure(text=now.strftime("%d/%m/%Y"))

        self.setSongs()

        if (time.time() - self.time >= 2):
            self.time = time.time()
            weather = self.getWeather()
            self.temp.configure(text=str(weather["main"]["temp"]) + u"\N{DEGREE SIGN}C")

            self.showCounter += 1
            if (self.showCounter >= self.showFrequency):
                self.showCounter = 0
                self.show += 1
                if (self.show >= self.countShow):
                    self.show = 0

            self.setSongs()
            if (self.show == 0):
                self.setWeather(weather)

            elif (self.show == 1):
                self.setDevices()

        self.after(1000, self.update_clock)

    def setSongs(self):
        title, artist = self.player.showTrack()

        if (self.show == 0):
            self.song.configure(text=self.formatText(title, 12))

        elif (self.show == 1):
            self.song.configure(text="")
            self.feelsLikeL.configure(text=self.formatText(title, 20), font=("Arial", 30))
            self.pressureL.configure(text=artist, font=("Arial", 20))

            self.feelsLike.configure(text="")
            self.pressure.configure(text="")

    def setWeather(self, weather):
        self.feelsLike.configure(text=str(weather["main"]["feels_like"]) + u"\N{DEGREE SIGN}C", font=("Arial", 20))
        self.pressure.configure(text=str(weather["main"]["pressure"]) + " hPa", font=("Arial", 20))
        self.humidity.configure(text=str(weather["main"]["humidity"]) + " %", font=("Arial", 20))
        self.wind.configure(text=str(weather["wind"]["speed"]) + " m/s", font=("Arial", 20))
        self.rise.configure(text=str(datetime.utcfromtimestamp(weather["sys"]["sunrise"]).strftime("%H:%M:%S")), font=("Arial", 20))
        self.set.configure(text=str(datetime.utcfromtimestamp(weather["sys"]["sunset"]).strftime("%H:%M:%S")), font=("Arial", 20))

        self.feelsLikeL.configure(text="Pocitová teplota:", font=("Arial", 15))
        self.pressureL.configure(text="Tlak:", font=("Arial", 15))
        self.humidityL.configure(text="Vlhkost:", font=("Arial", 15))
        self.windL.configure(text="Rychlost větru:", font=("Arial", 15))
        self.riseL.configure(text="Východ Slunce:", font=("Arial", 15))
        self.setL.configure(text="Západ Slunce:", font=("Arial", 15))

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

    def setDevices(self):
        devices = self.getDevices()

        strDevices = []
        for d in range(0, 4):
            if (d < len(devices)):
                strDevices.append(devices[d])
            else:
                strDevices.append(("",""))

        self.humidity.configure(text=strDevices[0][1], font=("Arial", 10))
        self.wind.configure(text=strDevices[1][1], font=("Arial", 10))
        self.rise.configure(text=strDevices[2][1], font=("Arial", 10))
        self.set.configure(text=strDevices[3][1], font=("Arial", 10))

        self.humidityL.configure(text=strDevices[0][0], font=("Arial", 10))
        self.windL.configure(text=strDevices[1][0], font=("Arial", 10))
        self.riseL.configure(text=strDevices[2][0], font=("Arial", 10))
        self.setL.configure(text=strDevices[3][0], font=("Arial", 10))

    def getDevices(self):
        output = check_output(['hcitool', 'con']).decode("utf-8") 
        lines = output.split(">")

        devices = []
        for d in range(1, len(lines)):
            mac = lines[d].strip().split(" ")[1] #ziska mac adresu
            name = check_output(["hcitool", "name", mac]).decode("utf-8").rstrip() #ziska jmeno zarizeni
            devices.append((name, mac))

        return devices

    def formatText(self, text, length):
        if (len(text) >= length):
            return text[:length] + "..."
        else:
            return text

if __name__== "__main__":
    print("Creating window")
    app = SampleApp()
    app.mainloop()
    """try:
        print("Creating window")
        app = SampleApp()
        app.mainloop()
    except:
        print("Chyba :'(")"""
