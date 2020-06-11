import automat as aut
from decimal import Decimal, ROUND_HALF_UP
import tkinter as tk
from tkinter import font  as tkfont



IMG_NAMES = (   '1 grosz', '2 grosze', '5 groszy', '10 groszy', '20 groszy',
                '50 groszy', '1 zl', '2 zl', '5 zl', '10 zl', '20 zl', '50 zl')
IMG_PATH = './images/'
IMG_EXT = '.png'


class Application(tk.Tk):
    """Inicjalizuje działanie aplikacji.

    Attributes:
        photos: list, zdjęcia monet oraz banknotów
        automat: aut.Automat, dostarcza logikę do działania aplikacji
        main_font: tkfont.Font, czcionka używana w aplikacji
        container: tk.Frame, kontener, w którym umieszczone zostaną wszystkie okna
        frames: dict, każdej nazwie strony przyporządkowuje jej instancję
    """

    def __init__(self, automat, *args, **kwargs):
        """Konstruktor dla Application.

        Tworzy wszystkie strony oraz kontener, w którym będą one umieszczone. Ustawia 
        i konfiguruje domyślne wartości, umieszcza kontener oraz strony na ekranie.

        Args:
            automat: aut.Automat, dostarcza logikę do działania aplikacji
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        tk.Tk.__init__(self, *args, **kwargs)

        self.photos = []
        self.automat = automat
        self.main_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.create_frames()
        self.show_frame("MainWindow")

    def create_frames(self):
        """zainicjalizuj wszystkie strony i umieść je jedna na drugiej"""
        for F in (MainWindow, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # umieść wszystkie strony w tym samym miejscu
            # widoczna będzie ta strona, która jest na wierzchu
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Umieść daną stronę na wierzchu stosu, tak aby była widoczna

        Args:
            page_name: str, nazwa strony
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def reset_all(self):
        """TODO zresetuj wszystkie strony"""
        pass

    def update_frame(self, page_name):
        """Uaktualnij daną stronę
        
        Args:
            page_name: str, nazwa strony
        """
        
        frame = self.frames[page_name]
        frame.update()


class MainWindow(tk.Frame):
    """Okno startowe z wyborem biletów.

    Attributes:
        controller: Application, odpowiada argumentowi dostarczonemu w konstruktorze,
            instancja klasy bazowej
        automat: aut.Automat, dziedziczony z klasy bazowej, logika działania aplikacji
        plus_minus_font: tkfont.Font, czcionka dla przycisków plus i minus
        lb_wybrane_bilety: list, zawiera etykiety, przyporządkowujące każdemu
            biletowi ich liczbę wybraną przez użytkownika
        lb_do_zaplaty: tk.Label, określa kwotę do zapłaty
    """

    def __init__(self, parent, controller):
        """Konstruktor dla MainWindow.

        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.

        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """

        tk.Frame.__init__(self, parent)
        self.controller = controller
        automat = controller.automat

        self.plus_minus_font = tkfont.Font(family='Helvetica', size=24, weight="bold")

        lb_bilety = []
        nazwy_biletow = [   "20-minutowy\nNormalny\t\t2.40 zł",
                            "40-minutowy\nNormalny\t\t3.70 zł",
                            "60-minutowy\nNormalny\t\t4.20 zł",
                            "20-minutowy\nUlgowy\t\t\t1.70 zł",
                            "40-minutowy\nUlgowy\t\t\t2.20 zł",
                            "60-minutowy\nUlgowy\t\t\t2.50 zł"]

        #liczba wybranych biletów dla każdego typu biletu
        automat.wybrane_bilety = [0]*automat.liczba_biletow
        self.lb_wybrane_bilety = []

        self.lb_do_zaplaty = tk.Label(self, text="Do zapłaty: %.2f" % automat.do_zaplaty, 
                                    font=controller.main_font)
        self.lb_do_zaplaty.grid(row=7, column=2, columnspan=3)

        plus_btns = []
        minus_btns = []

        for i in range(automat.liczba_biletow):
            lb_bilet = tk.Label(self, width=27, text=nazwy_biletow[i],
                                font=controller.main_font, fg="white", bg="blue",
                                borderwidth=4, relief="groove", padx=5, pady=10,
                                justify=tk.LEFT, anchor="w")
            lb_bilet.grid(row=i, column=0)
            lb_bilety.append(lb_bilet)


        def update_price():
            """Uaktualnij cenę pokazywaną na etykiecie"""
            self.lb_do_zaplaty.config(text="Do zapłaty: %.2f" % automat.do_zaplaty)

        def plus_pressed(idx):
            """Obsługa naciśnięcia przycisku plus
            
            Args:
                idx: int, numer w tablicy plus_btns
            """
            if minus_btns[idx]["state"] == "disabled":
                minus_btns[idx]["state"] = "normal"
            automat.dodaj_bilet(idx)
            update_price()
            controller.update_frame("PageOne")
            self.lb_wybrane_bilety[idx].config(text="%i" % automat.wybrane_bilety[idx])

        def minus_pressed(idx):
            """Obsługa naciśnięcia przycisku minus
        
            Args:
                idx: int, numer w tablicy minus_btns
            """
            if automat.wybrane_bilety[idx] > 0:
                automat.usun_bilet(idx)
                update_price()
                controller.update_frame("PageOne")
                self.lb_wybrane_bilety[idx].config(text="%i" % automat.wybrane_bilety[idx])
            if automat.wybrane_bilety[idx] == 0:
                minus_btns[idx]["state"] = "disabled"

        for i in range(automat.liczba_biletow):
            liczba = tk.Label(self, text="%i" % automat.wybrane_bilety[i], font=controller.main_font)
            liczba.grid(row=i, column=3)
            self.lb_wybrane_bilety.append(liczba)

        for i in range(automat.liczba_biletow):
            plus = tk.Button(self, text='+', pady=10, padx=20, font=self.plus_minus_font,
                             command=lambda idx=i: plus_pressed(idx))
            minus = tk.Button(self, text='–', pady=10, padx=20, font=self.plus_minus_font,
                              command=lambda idx=i: minus_pressed(idx))
            plus.grid(row=i, column=2, padx=30, sticky="we")
            minus.grid(row=i, column=4, padx=30, sticky="we")
            plus_btns.append(plus)
            minus_btns.append(minus)
            minus["state"] = "disabled"


        button1 = tk.Button(self, text="Kupuję i płacę", width=20, font=controller.main_font, 
                            bg="green", fg="white", 
                            command=lambda: controller.show_frame("PageOne"))
        #button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        
        button1.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        #button2.grid(row=1,column=2)
    
    def update(self):
        """TODO: Uaktualnij dane na stronie"""
        pass

    def reset(self):
        """TODO: Zresetuj stronę do stanu początkowego"""
        pass


class PageOne(tk.Frame):
    """Okno wrzucania monet.

    Attributes:
        controller: Application, odpowiada argumentowi dostarczonemu w konstruktorze,
            instancja klasy bazowej
        automat: aut.Automat, dziedziczony z klasy bazowej, logika działania aplikacji
        entry_label_font: tkfont.Font, czcionka dla pola tekstowego
        zaplac_btn: tk.Button, przycisk, do dokonywania płatności
        lb_do_zaplaty: tk.Label, etykieta określająca kwotę do zapłaty
    """

    def __init__(self, parent, controller):
        """Konstruktor dla PageOne.

        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.

        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        automat = controller.automat
        self.controller = controller
        self.entry_label_font = tkfont.Font(family='Helvetica', size=12, weight='bold')

        def coin_btn_pressed(idx):
            """Obsługa naciśnięcia przycisku monety
        
            Args:
                idx: int, numer w tablicy coin_btns
            """
            form_var.set(1)
            nonlocal wybrany_nominal
            wybrany_nominal = automat.obslugiwane_monety[idx]
            entry_label.configure(text=f'Wprowadź liczbę nominałów {wybrany_nominal:.2f} zł')

        def submit_pressed():
            """Obsługa naciśnięcia przycisku submit_btn"""
            wprowadzona_liczba = entry.get()
            automat.zaladuj_monety(wprowadzona_liczba, wybrany_nominal)

            zwrot_btn["state"] = "normal"
            if automat.wartosc_wrzuconych >= automat.do_zaplaty:
                self.zaplac_btn["state"] = "normal"
            lb_wartosc_wrzuconych.config(text=f'Wrzucono: {automat.wartosc_wrzuconych:.2f}')
        
        def zaplac_pressed():
            """Obsługa naciśnięcia przycisku zaplac_btn"""
            print(f'Automat zwrócił następujące monety:\n{automat.wydaj_reszte()}')
            controller.show_frame("PageTwo")

        def zwrot_pressed():
            """Obsługa naciśnięcia przycisku zwrot_btn"""
            print(f'Automat zwrócił:\n{automat.zwroc_pieniadze()}')
            lb_wartosc_wrzuconych.config(text=f'Wrzucono: {automat.wartosc_wrzuconych:.2f}')
            self.update()
            print(automat.suma_monet())

        wybrany_nominal = 0
        coin_btns = []
        form_var = tk.IntVar()
        entry = tk.Entry(self, text=form_var)
        entry_label = tk.Label(self, font=self.entry_label_font)
        submit_btn = tk.Button(self, text='Potwierdź', font=self.entry_label_font, 
                               command=submit_pressed)
        self.zaplac_btn = tk.Button(self, text='Zapłać', font=controller.main_font, state="disabled", 
                               command=zaplac_pressed)
        zwrot_btn = tk.Button(self, text='Zwróć pieniądze', font=controller.main_font, state="disabled",
                              command=zwrot_pressed)
        self.lb_do_zaplaty = tk.Label(self, text=f'Do zapłaty: {automat.do_zaplaty:.2f}',
                                 font=controller.main_font)
        lb_wartosc_wrzuconych = tk.Label(self, text=f'Wrzucono: {automat.wartosc_wrzuconych:.2f}', 
                                         font=controller.main_font)
        back_btn = tk.Button(self, text="Wróć do wyboru biletów", font=controller.main_font,
                             command=lambda: controller.show_frame("MainWindow"))
        

        entry.grid(row=3, column=4, columnspan=2, pady=50)
        submit_btn.grid(row=3, column=6, columnspan=3, sticky="w")
        self.zaplac_btn.grid(row=6, column=6, columnspan=3, sticky="w")
        zwrot_btn.grid(row=7, column=6, columnspan=4, sticky="w")
        entry_label.grid(row=3, column=0, columnspan=5, sticky="w")
        self.lb_do_zaplaty.grid(row=4, column=6, columnspan=4, sticky="e")
        lb_wartosc_wrzuconych.grid(row=5, column=6, columnspan=4, sticky="e")
        back_btn.grid(row=0, column=0, columnspan=5, pady=(0, 20))
                   
        for i in range(len(IMG_NAMES)):
            b=tk.Button(self, command=lambda idx=i: coin_btn_pressed(idx))
            img_name = IMG_PATH + IMG_NAMES[i] + IMG_EXT
            controller.photos.append(tk.PhotoImage(file=img_name))
            b.config(image=controller.photos[i])
            coin_btns.append(b)

        for i, b in enumerate(coin_btns[:-3]):
            b.grid(row=1, column=i, pady=5)
        for i, b in enumerate(coin_btns[-3:]):
            b.grid(row=2, column=i*2, columnspan=3, pady=5, sticky="w")
    
    def update(self):
        """Uaktualnij dane na stronie"""
        automat = self.controller.automat
        self.lb_do_zaplaty.config(text=f'Do zapłaty: {automat.do_zaplaty:.2f}')
        if automat.wartosc_wrzuconych < automat.do_zaplaty:
            self.zaplac_btn["state"] = "disabled"

    def reset(self):
        """TODO: Zresetuj stronę do stanu początkowego"""
        pass

        
class PageTwo(tk.Frame):
    """Okno ekranu końcowego.

    Attributes:
        controller: Application, odpowiada argumentowi dostarczonemu w konstruktorze,
            instancja klasy bazowej
        automat: aut.Automat, dziedziczony z klasy bazowej, logika działania aplikacji
    """

    def __init__(self, parent, controller):
        """Konstruktor dla PageTwo.

        Tworzy przyciski i etykiety, rozmieszcza elementy na stronie.

        Args:
            parent: tk.Frame, kontener będący rodzicem strony.
            controller: Application, instancja klasy bazowej
        """
        tk.Frame.__init__(self, parent)
        automat = controller.automat
        self.controller = controller

        def btn_pressed():
            controller.destroy()

        label = tk.Label(self, text="Dziękujemy", font=controller.main_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Wyjdź z aplikacji", font=controller.main_font,
                           command=btn_pressed)
        button.pack()

    def update(self):
        """TODO: Uaktualnij dane na stronie"""
        pass

    def reset(self):
        """TODO: Zresetuj stronę do stanu początkowego"""
        pass

def main():
    """Uruchamia aplikację, ustawia niezbędne elementy"""
    automat = aut.Automat(aut.OBSLUGIWANE_NOMINALY)
    automat.wczytaj_monety('PLN')

    app = Application(automat)
    app.mainloop()


if __name__ == "__main__":

    main()

    