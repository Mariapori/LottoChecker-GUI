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
        self.WKNUM = int(week.replace("W",""))
        self.numerot = numerot
        # build ui
        self.vuosiviikkovar = tk.StringVar()
        self.vuosiviikkovar.set(week + ' / ' + str(year))

        self.txt1var = tk.StringVar()
        self.txt1var.set(txtNumerot)

        self.txtplusvar = tk.StringVar()
        self.txtlisavar = tk.StringVar()
        if len(data) > 0:
            self.txtplusvar.set('Plus: ' + data[0]['results'][0]['tertiary'][0])
            self.txtlisavar.set('Lisänumero: ' + data[0]['results'][0]['secondary'][0])
        else:
            self.txtplusvar.set('Plus: ')
            self.txtlisavar.set('Lisänumero: ')

        self.frame1 = tk.Frame(master, container='false')
        self.labelframe1 = tk.LabelFrame(self.frame1)
        self.txtVuosiViikko = tk.Label(self.labelframe1)
        self.txtVuosiViikko.configure(background='#ff0000', textvariable=self.vuosiviikkovar)
        self.txtVuosiViikko.pack(side='top')
        self.txt1 = tk.Label(self.labelframe1)
        self.txt1.configure(background='#ff0000', textvariable=self.txt1var)
        self.txt1.pack(side='top')

        self.txtPlus = tk.Label(self.labelframe1)
        if len(data) > 0:
            self.txtPlus.configure(background='#ff0000', textvariable=self.txtplusvar)
            self.txtPlus.pack(side='top')
            self.txtLisa = tk.Label(self.labelframe1)
            self.txtLisa.configure(background='#ff0000', textvariable=self.txtlisavar)
            self.txtLisa.pack(side='top')
        else:
            self.txtPlus.configure(background='#ff0000', textvariable=self.txtplusvar)
            self.txtPlus.pack(side='top')
            self.txtLisa = tk.Label(self.labelframe1)
            self.txtLisa.configure(background='#ff0000', textvariable=self.txtlisavar)
            self.txtLisa.pack(side='top')

        self.btnEdellinenwk = tk.Button(self.labelframe1)
        self.btnEdellinenwk.configure(background='#ff0000', text='<')
        self.btnEdellinenwk.configure(command=self.edellinenwk)
        self.btnEdellinenwk.place(anchor='nw', relwidth='0.14', relx='0.0', rely='0.0', x='0', y='0')
        self.btnSeuraavawk = tk.Button(self.labelframe1)
        self.btnSeuraavawk.configure(background='#ff0000', text='>')
        self.btnSeuraavawk.configure(command=self.seuraavawk)
        self.btnSeuraavawk.place(anchor='nw', relwidth='0.14', relx='0.86', rely='0.0', x='0', y='0')
        self.btnTarkista = tk.Button(self.labelframe1)
        self.btnTarkista.configure(background='#8d2010', foreground='#ffffff', text='Tarkista listasta')
        self.btnTarkista.configure(command=self.Tarkista)
        self.btnTarkista.pack(side='top')
        self.labelframe1.configure(background='#ff0000', font='TkHeadingFont', foreground='#000000', height='200')
        self.labelframe1.configure(text='Lottonumerot', width='500')
        self.labelframe1.pack(fill='both', side='top')
        self.frame1.configure(background='#ff0000', height='200', width='500')
        self.frame1.pack(expand='true', fill='both', side='top')
        self.var = tk.StringVar()
        self.asd = tk.Message(master,textvariable=self.var,aspect=400)
        # Main widget
        self.mainwindow = self.frame1
    
    def edellinenwk(self):
        if self.asd is not None:
            self.asd.destroy()
            self.asd = tk.Message(self.mainwindow,textvariable=self.var,aspect=400)
            
        veikatut = []
        txtNumerot = ''
        numerot = []
        year = datetime.date.today().year

        if self.WKNUM is None:
            wknumber = datetime.date.today().isocalendar()[1]
            week = wknumber - 1
            self.WKNUM = week
        else:
            week = self.WKNUM - 1
            self.WKNUM = week

        thisweekandyear = str(year) + '-W' + str(week)
        jsondata = requests.get('https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/' + thisweekandyear)
        data = json.loads(jsondata.content)

        if len(data) > 0:
            for item in data[0]['results'][0]['primary']:
                numerot.append(item)
        else:
            txtNumerot = 'Lottoa ei ole arvottu'

        for numero in numerot:
            txtNumerot = txtNumerot + ' ' + numero
        self.numerot = numerot
        self.vuosiviikkovar.set('W' + str(week) + ' / ' + str(year))
        self.txt1var.set(txtNumerot)

        if len(data) > 0:
            self.txtlisavar.set('Lisänumero: ' + data[0]['results'][0]['secondary'][0])
            self.txtplusvar.set('Plus: ' + data[0]['results'][0]['tertiary'][0])
        else:
            self.txtlisavar.set('Lisänumero: ')
            self.txtplusvar.set('Plus: ')

    def seuraavawk(self):
        if self.asd is not None:
            self.asd.destroy()
            self.asd = tk.Message(self.mainwindow,textvariable=self.var,aspect=400)

        veikatut = []
        txtNumerot = ''
        numerot = []
        year = datetime.date.today().year

        if self.WKNUM is None:
            wknumber = datetime.date.today().isocalendar()[1]
            week = wknumber + 1
            self.WKNUM = week
        else:
            week = self.WKNUM + 1
            self.WKNUM = week
        

        thisweekandyear = str(year) + '-W' + str(week)
        jsondata = requests.get('https://www.veikkaus.fi/api/draw-results/v1/games/LOTTO/draws/by-week/' + thisweekandyear)
        data = json.loads(jsondata.content)

        if len(data) > 0:
            for item in data[0]['results'][0]['primary']:
                numerot.append(item)
        else:
            txtNumerot = 'Lottoa ei ole arvottu'

        for numero in numerot:
            txtNumerot = txtNumerot + ' ' + numero
        self.numerot = numerot
        self.vuosiviikkovar.set('W' + str(week) + ' / ' + str(year))
        self.txt1var.set(txtNumerot)

        if len(data) > 0:
            self.txtlisavar.set('Lisänumero: ' + data[0]['results'][0]['secondary'][0])
            self.txtplusvar.set('Plus: ' + data[0]['results'][0]['tertiary'][0])
        else:
            self.txtlisavar.set('Lisänumero: ')
            self.txtplusvar.set('Plus: ')

    def Tarkista(self):
        if self.asd is not None:
            self.asd.destroy()
            self.asd = tk.Message(self.mainwindow,textvariable=self.var,aspect=400)
        try:
            osumat = 0
            polku = tkFiledialog.askopenfilename()
            tiedosto = open(polku,"r")
            lines = tiedosto.readlines()
            wk = "W" + str(self.WKNUM)
            for line in lines:
                if line.startswith(wk):
                    veikatut.append(line.split(" "))

            if len(veikatut) > 0:
                for veikkaus in veikatut:
                    for i in range(len(veikkaus)):
                        if veikkaus[i] in self.numerot:
                            osumat = osumat + 1

            self.var.set("Osumia: " + str(osumat))
        except:
            self.var.set("Tiedostoa ei voitu lukea..")
        self.asd.pack(expand=1,anchor="n",pady=10)
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Lottonumerot')
    root.geometry('500x180')
    app = LottoApp(root)
    app.run()
