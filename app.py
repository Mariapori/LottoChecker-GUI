import os
import tkinter as tk
from tkinter.constants import BOTH
import tkinter.ttk as ttk
import pygubu
import requests
import datetime
import json
import sys
import tkinter.filedialog as tkFiledialog

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, 'lotto.ui')

veikatut = []
txtNumerot = ''
numerot = []
year = datetime.date.today().year
week = 'W' + str(datetime.date.today().isocalendar()[1])

thisweekandyear = str(year) + '-' + week
jsondata = requests.get('https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/' + thisweekandyear)
data = json.loads(jsondata.content)

if len(data) > 0:
    for item in data[0]['results'][0]['primary']:
        numerot.append(item)
else:
    txtNumerot = 'Lottoa ei ole arvottu'

for numero in numerot:
    txtNumerot = txtNumerot + ' ' + numero


class LottoApp:
    def __init__(self, master=None):
        # build ui
        self.frame1 = tk.Frame(master, container='false')
        self.labelframe1 = tk.LabelFrame(self.frame1)
        self.txtVuosiViikko = tk.Label(self.labelframe1)
        self.txtVuosiViikko.configure(background='#ff0000', text=week + ' / ' + str(year))
        self.txtVuosiViikko.pack(side='top')
        self.txt1 = tk.Label(self.labelframe1)
        self.txt1.configure(background='#ff0000', text=txtNumerot)
        self.txt1.pack(side='top')

        self.txtPlus = tk.Label(self.labelframe1)
        if len(data) > 0:
            self.txtPlus.configure(background='#ff0000', text='Plus: ' + data[0]['results'][0]['tertiary'][0])
            self.txtPlus.pack(side='top')
            self.txtLisa = tk.Label(self.labelframe1)
            self.txtLisa.configure(background='#ff0000', text='Lisänumero: ' + data[0]['results'][0]['secondary'][0])
            self.txtLisa.pack(side='top')
        else:
            self.txtPlus.configure(background='#ff0000', text='Plus: ')
            self.txtPlus.pack(side='top')
            self.txtLisa = tk.Label(self.labelframe1)
            self.txtLisa.configure(background='#ff0000', text='Lisänumero: ')
            self.txtLisa.pack(side='top')

        self.btnTarkista = tk.Button(self.labelframe1)
        self.btnTarkista.configure(background='#8d2010', foreground='#ffffff', text='Tarkista listasta')
        self.btnTarkista.configure(command=self.Tarkista)
        self.btnTarkista.pack(side='top')
        self.labelframe1.configure(background='#ff0000', font='TkHeadingFont', foreground='#000000', height='200')
        self.labelframe1.configure(text='Lottonumerot', width='500')
        self.labelframe1.pack(fill='both', side='top')
        self.frame1.configure(background='#ff0000', height='200', width='500')
        self.frame1.pack(expand='true', fill='both', side='top')

        # Main widget
        self.mainwindow = self.frame1
    
    def Tarkista(self):
        osumat = 0
        polku = tkFiledialog.askopenfilename()
        tiedosto = open(polku,"r")
        lines = tiedosto.readlines()
        for line in lines:
            if line.startswith(week):
                veikatut.append(line.split(" "))

        if len(veikatut) > 0:
            for veikkaus in veikatut:
                for i in range(len(veikkaus)):
                    if veikkaus[i] in numerot:
                        osumat = osumat + 1

        asd = tk.Message(self.mainwindow,text='Osumia: ' + str(osumat),aspect=400)
        asd.pack(expand=1,anchor="n",pady=10)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Lottonumerot')
    root.geometry('500x180')
    app = LottoApp(root)
    app.run()
