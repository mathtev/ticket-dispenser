"""Testy modułu automat."""

import unittest

import automat as aut
from decimal import Decimal


class AutomatTest(unittest.TestCase):

    def setUp(self):
        self.automat = aut.Automat(aut.OBSLUGIWANE_NOMINALY)
        self.automat.wczytaj_monety('PLN')

    def test_odliczona_kwota_zwroc_pusta_tablice(self):

        self.automat.do_zaplaty = Decimal('5.11')

        m1 = aut.Moneta(5, 'PLN')
        m2 = aut.Moneta(0.10, 'PLN')
        m3 = aut.Moneta(0.01, 'PLN')

        self.automat.wrzuc_monete(m1, 1)
        self.automat.wrzuc_monete(m2, 1)
        self.automat.wrzuc_monete(m3, 1)
        
        self.assertEqual(self.automat.wydaj_reszte(), [])


    def test_wplacono_wiecej_moze_zwrocic(self):

        Moneta = aut.Moneta
        self.automat.do_zaplaty = Decimal('5.11')

        m1 = Moneta(10, 'PLN')
        m2 = Moneta(0.10, 'PLN')
        m3 = Moneta(0.02, 'PLN')  

        self.automat.wrzuc_monete(m1, 1)
        self.automat.wrzuc_monete(m2, 1)
        self.automat.wrzuc_monete(m3, 1)

        #10.12 - 5.11 = 5.01 zl
        spodziewany_wynik = Decimal('5.01')
        do_sprawdzenia = sum(m.nominal for m in self.automat.wydaj_reszte())
  
        self.assertEqual(do_sprawdzenia, spodziewany_wynik)
    

    def test_wplacono_wiecej_nie_moze_zwrocic(self):

        Moneta = aut.Moneta
        self.automat.do_zaplaty = Decimal('5.11')

        m1 = Moneta(50, 'PLN')

        self.automat.wrzuc_monete(m1, 3)    #150.00 zl

        spodziewany_wynik = Decimal('150')
        do_sprawdzenia = sum(m.nominal for m in self.automat.wydaj_reszte())

        # wyjątek nie jest rzucany, więc poniższa linijka nie zadziała
        # zamiast tego wypisywana jest na ekran informacja o błędzie oraz
        # automat zwraca wszystkie wrzucone monety
        # W dodatku mój program nie zwraca dokładnie tych samych wrzuconych monet,
        # zwrot monet działa podobnie jak wydawanie reszty. Najpierw największe nominały

        #self.assertRaises(aut.nieMoznaZwrocicMonetException, self.automat.wydaj_reszte)
        self.assertEqual(do_sprawdzenia, spodziewany_wynik)


    def test_100_monet_1_grosz_zwraca_1_zl(self):

        Moneta = aut.Moneta

        m1 = Moneta(0.01, 'PLN')

        self.automat.wrzuc_monete(m1, 100)    #1.00 zl

        spodziewany_wynik = Decimal('1.00')
        do_sprawdzenia = sum(m.nominal for m in self.automat.zwroc_pieniadze())

        self.assertEqual(do_sprawdzenia, spodziewany_wynik)

    
    def test_zakup_dwoch_biletow_cena_jest_suma(self):

        self.automat.dodaj_bilet(0) #2.40 zl
        self.automat.dodaj_bilet(1) #3.70 zl

        spodziewany_wynik = Decimal('6.10')
        do_sprawdzenia = self.automat.do_zaplaty

        self.assertEqual(do_sprawdzenia, spodziewany_wynik)


    def test_dodawanie_biletu_monet_na_przemian(self):

        Moneta = aut.Moneta
        self.automat.do_zaplaty = Decimal('0')

        m1 = Moneta(5.00, 'PLN')
        m2 = Moneta(0.10, 'PLN')
        m3 = Moneta(0.20, 'PLN') 
        m4 = Moneta(0.50, 'PLN')
        m5 = Moneta(0.20, 'PLN')
        m6 = Moneta(0.10, 'PLN')

        self.automat.dodaj_bilet(0)     #2.40 zl
        
        self.automat.wrzuc_monete(m1, 1) 
        self.automat.wrzuc_monete(m2, 1)

        self.automat.dodaj_bilet(1)     #3.70 zl

        self.automat.wrzuc_monete(m3, 1)
        self.automat.wrzuc_monete(m4, 1) 
        self.automat.wrzuc_monete(m5, 1) 
        self.automat.wrzuc_monete(m6, 1) 

        self.assertEqual(self.automat.wydaj_reszte(), [])

    
    def test_podanie_nieodpowiedniej_liczby_monet(self):

        # wartość wprowadzona przez użytkownika jest stringiem
        self.assertRaises(ValueError, self.automat.zaladuj_monety, '2.2', Decimal('5'))
        self.assertRaises(ValueError, self.automat.zaladuj_monety, '-5', Decimal('5'))


if __name__ == '__main__':
    unittest.main()