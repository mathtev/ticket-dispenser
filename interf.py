from Automat import *
import tkinter as tk
from tkinter import font  as tkfont


automat = Automat(obslugiwane_nominaly)


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

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

        self.main_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        
        label1 = tk.Label(self, width=27, text="20-minutowy\nNormalny\t\t2.40 zł", font=self.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
        label2 = tk.Label(self, width=27, text="40-minutowy\nNormalny\t\t3.70 zł", font=self.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
        label3 = tk.Label(self, width=27, text="60-minutowy\nNormalny\t\t4.20 zł", font=self.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
        label4 = tk.Label(self, width=27, text="20-minutowy\nUlgowy\t\t\t1.70 zł", font=self.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
        label5 = tk.Label(self, width=27, text="40-minutowy\nUlgowy\t\t\t2.20 zł", font=self.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
        label6 = tk.Label(self, width=27, text="60-minutowy\nUlgowy\t\t\t2.50 zł", font=self.main_font, fg="white", bg="blue", borderwidth=4, relief="groove", padx=5, pady=10, justify=tk.LEFT, anchor="w")
        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)
        label4.grid(row=3, column=0)
        label5.grid(row=4, column=0)
        label6.grid(row=5, column=0)

        lb = 6              #liczba rodzai biletów
        wybrane = [0]*lb    #liczba wybranych biletów dla każdego typu biletu
        lb_wybrane = []     #lista etykiet zawierających liczbę wybranych biletów

        lb_cena = tk.Label(self, text="Do zapłaty: %.2f" % automat.doZaplaty, font=self.main_font)
        lb_cena.grid(row = 7, column = 2)

        def update_price():
            lb_cena.config(text="Do zapłaty: %.2f" % automat.doZaplaty)

        def plus_pressed(idx):
            automat.doZaplaty += automat.ceny_biletow[idx]
            update_price()
            wybrane[idx] += 1
            lb_wybrane[idx].config(text="%i" % wybrane[idx])

        def minus_pressed(idx):
            if wybrane[idx] > 0:
                automat.doZaplaty -= automat.ceny_biletow[idx]
                update_price()
                wybrane[idx] -= 1
                lb_wybrane[idx].config(text="%i" % wybrane[idx])

        for i in range(lb):
            liczba = tk.Label(self, text="%i" % wybrane[i], font=self.main_font)
            liczba.grid(row = i, column = 3)
            lb_wybrane.append(liczba)

        for i in range(lb):
            plus = tk.Button(self, text = '+', command=lambda idx=i: plus_pressed(idx), pady=10, padx=10, font=self.main_font)
            minus = tk.Button(self, text = '-', command=lambda idx=i: minus_pressed(idx), pady=10, padx=10, font=self.main_font)

            plus.grid(row = i, column = 2,padx=30)
            minus.grid(row = i, column = 4,padx=30)


        button1 = tk.Button(self, text="Kupuję i płacę", command=lambda: controller.show_frame("PageOne"), width=20, font=self.main_font, bg="green", fg="white")
        #button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        
        button1.grid(row=6,column=0, columnspan=2, sticky="w")
        #button2.grid(row=1,column=2)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainWindow"))
        button.pack()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
    