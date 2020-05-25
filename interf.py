from decimal import Decimal, ROUND_HALF_UP
import Automat as aut
import tkinter as tk
from tkinter import font  as tkfont


#TODO
#Drugie okno z monetami i wpisywaniem ich liczby
#Wydawanie reszty z wrzuconych monet

IMG_NAMES = (   '1 grosz', '2 grosze', '5 groszy', '10 groszy', '20 groszy', 
                '50 groszy', '1 zl', '2 zl', '5 zl', '10 zl', '20 zl', '50 zl')
IMG_PATH = './images2/'
IMG_EXT = '.png'
photos = []

OBSLUGIWANE_NOMINALY = aut.OBSLUGIWANE_NOMINALY
automat = aut.Automat(OBSLUGIWANE_NOMINALY)

automat.wczytaj_monety('PLN')


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.main_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainWindow, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainWindow")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.plus_minus_font = tkfont.Font(family='Helvetica', size=24, weight="bold")

        liczba_biletow = 6      #liczba rodzai biletów

        lb_bilety = []
        nazwy_biletow = [   "20-minutowy\nNormalny\t\t2.40 zł",
                            "40-minutowy\nNormalny\t\t3.70 zł",
                            "60-minutowy\nNormalny\t\t4.20 zł",
                            "20-minutowy\nUlgowy\t\t\t1.70 zł",
                            "40-minutowy\nUlgowy\t\t\t2.20 zł",
                            "60-minutowy\nUlgowy\t\t\t2.50 zł"]

        wybrane_bilety = [0]*liczba_biletow    #liczba wybranych biletów dla każdego typu biletu
        lb_wybrane_bilety = []  

        lb_do_zaplaty = tk.Label(self, text="Do zapłaty: %.2f" % automat.do_zaplaty, font=controller.main_font)
        lb_do_zaplaty.grid(row = 7, column = 2, columnspan=3)

        plus_btns = []
        minus_btns = []
        

        for i in range(liczba_biletow):
            lb_bilet = tk.Label(self, width=27, text=nazwy_biletow[i], font=controller.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
            lb_bilet.grid(row=i, column=0)
            lb_bilety.append(lb_bilet)


        def update_price():
            lb_do_zaplaty.config(text="Do zapłaty: %.2f" % automat.do_zaplaty)

        def plus_pressed(idx):
            if minus_btns[idx]["state"] == "disabled":
                minus_btns[idx]["state"] = "normal"
            automat.do_zaplaty += automat.ceny_biletow[idx]
            update_price()
            wybrane_bilety[idx] += 1
            lb_wybrane_bilety[idx].config(text="%i" % wybrane_bilety[idx])

        def minus_pressed(idx):
            if wybrane_bilety[idx] > 0:
                automat.do_zaplaty -= automat.ceny_biletow[idx]
                update_price()
                wybrane_bilety[idx] -= 1
                lb_wybrane_bilety[idx].config(text="%i" % wybrane_bilety[idx])
            if wybrane_bilety[idx] == 0:
                minus_btns[idx]["state"] = "disabled"

        for i in range(liczba_biletow):
            liczba = tk.Label(self, text="%i" % wybrane_bilety[i], font=controller.main_font)
            liczba.grid(row = i, column = 3)
            lb_wybrane_bilety.append(liczba)

        for i in range(liczba_biletow):
            plus = tk.Button(self, text = '+', pady=10, padx=20, font=self.plus_minus_font, 
                                command=lambda idx=i: plus_pressed(idx))
            minus = tk.Button(self, text = '–', pady=10, padx=20, font=self.plus_minus_font,
                                command=lambda idx=i: minus_pressed(idx))
            plus.grid(row = i, column = 2,padx=30,sticky="we")
            minus.grid(row = i, column = 4,padx=30,sticky="we")
            plus_btns.append(plus)
            minus_btns.append(minus)
            minus["state"] = "disabled"


        button1 = tk.Button(self, text="Kupuję i płacę", command=lambda: controller.show_frame("PageOne"), width=20, font=controller.main_font, bg="green", fg="white")
        #button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        
        button1.grid(row=7,column=0, columnspan=2, padx=10, pady=10, sticky="w")
        #button2.grid(row=1,column=2)


class PageOne(tk.Frame):

   
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.entry_label_font = tkfont.Font(family='Helvetica', size=12, weight='bold')

        def coin_btn_pressed(idx):
            nonlocal current_val
            v.set(1)
            current_val = OBSLUGIWANE_NOMINALY[idx]
            entry_label.configure(text="Wprowadź liczbę nominałów %.2f zł" % current_val)


        def submit_pressed():
            try:
                val = int(entry.get())
            except ValueError:
                print("Wprowadzono złe dane")
            else:
                automat.wartosc_wrzuconych += val*current_val
                lb_wartosc_wrzuconych.config(text="Wrzucono: %.2f" % automat.wartosc_wrzuconych)

        coin_btns = []
        current_val = 0
        v = tk.IntVar()
        entry_label = tk.Label(self, font=self.entry_label_font)
        entry = tk.Entry(self, text=v)
        submit_btn = tk.Button(self, text='Potwierdź', font=self.entry_label_font, 
                                command=submit_pressed)
        lb_do_zaplaty = tk.Label(self, text="Do zapłaty: %.2f" % automat.do_zaplaty, font=controller.main_font)
        lb_wartosc_wrzuconych = tk.Label(self, text="Wrzucono: %.2f" % automat.wartosc_wrzuconych, font=controller.main_font)
        back_btn = tk.Button(self, text="Wróć do wyboru biletów", font=controller.main_font,
                    command=lambda: controller.show_frame("MainWindow"))
        

        entry.grid(row=3, column=4, columnspan=2, pady=50)
        submit_btn.grid(row=3, column=6, columnspan=3,sticky="w") 
        entry_label.grid(row=3,column=0,columnspan=4)
        lb_do_zaplaty.grid(row=4,column=6,columnspan=4,sticky="e")
        lb_wartosc_wrzuconych.grid(row=5,column=6,columnspan=4,sticky="e")
        back_btn.grid(row=0,column=0,columnspan=5, pady=(0, 20))
                   
        for i in range(len(IMG_NAMES)):
            b=tk.Button(self, command=lambda idx=i: coin_btn_pressed(idx))
            img_name = IMG_PATH + IMG_NAMES[i] + IMG_EXT
            photos.append(tk.PhotoImage(file=img_name))
            b.config(image=photos[i])
            coin_btns.append(b)

        for i, b in enumerate(coin_btns[:-3]):
            b.grid(row=1,column=i, pady=5)
        for i, b in enumerate(coin_btns[-3:]):
            b.grid(row=2,column=i*2,columnspan=3, pady=5, sticky="w")
    
        def update_price():
            '''Cena do zapłaty jest aktualizowana co 2 sekundy'''
            lb_do_zaplaty.config(text="Do zapłaty: %.2f" % automat.do_zaplaty)
            self.after(2000, update_price)
        update_price()
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.main_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
    