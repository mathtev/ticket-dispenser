from decimal import Decimal, ROUND_HALF_UP
import csv

GROSZ = Decimal('.01')
LISTA_NOMINALOW = ['0.01', '0.02', '0.05', '0.1', '0.2', '0.5', '1', '2', '5','10','20','50']
OBSLUGIWANE_NOMINALY = tuple(map(Decimal, LISTA_NOMINALOW))


class Error(Exception): 
    pass
  

class NieznanaWalutaException(Error):
    def __init__(self, msg):
        
        self.msg = msg 

class ListaMonetException(Error):
    def __init__(self, msg):
        self.msg = msg
    lista_monet = []

class ZlyNominalException(ListaMonetException):
    def __init__(self, msg):
        self.msg = msg

class ZlyFormatPlikuException(ListaMonetException):
    def __init__(self, msg):
        self.msg = msg


class Moneta:
    
    def __init__(self, nominal, waluta):

        nominal = Decimal(str(nominal))

        try:
            if nominal not in OBSLUGIWANE_NOMINALY:
                raise(ZlyNominalException("Zły nominał"))
            
        except ZlyNominalException as err:
            print(err.msg)
            raise

        else:
            self._nominal = nominal
            self.waluta = waluta

    @property
    def nominal(self):
        return self._nominal.quantize(GROSZ, ROUND_HALF_UP)

    @nominal.setter
    def nominal(self, n):
        self._nominal = Decimal(str(n))

    def __str__(self):
        return 'Moneta o wartości: {}, waluts: {}'.format(self.nominal, self.waluta)

    def __repr__(self):
        return 'Moneta({}, {})'.format(self.nominal, self.waluta)

class PrzechowywaczMonet:
    def __init__(self, obslugiwane_monety):
        self._obslugiwane_monety = obslugiwane_monety
        self._monety = []

    def dodajMonete(self, m):
        if isinstance(m,Moneta):
            self._monety.append(m)
        else:
            print('Przesłany obiekt nie jest monetą')

    def sumaMonet(self):
        suma = Decimal('0')
        for m in self._monety:
            suma += m.nominal
        return suma

    def zwrocMonete(self, nom):

        nom = Decimal(str(nom))
        zwrotna = None

        for m in self._monety:
            if m.nominal == nom:
                zwrotna = m
                self._monety.remove(m)
           
        return zwrotna


class Automat(PrzechowywaczMonet):

    obslugiwana_waluta = 'PLN'
    ceny_biletow = tuple(map(Decimal, ['2.40','3.70','4.20','1.70','2.20','2.50']))
    
    def __init__(self, obslugiwane_monety):
        super().__init__(obslugiwane_monety)
        self.do_zaplaty = Decimal('0')
        self.wartosc_wrzuconych = Decimal('0')

    def reset(self):
        self.do_zaplaty = Decimal('0')
        self._monety.clear()

    def dodajMonete(self, m):
        if isinstance(m,Moneta): 
            try:
                if m.waluta != self.obslugiwana_waluta:
                    raise(NieznanaWalutaException("Nieznana waluta"))
            except NieznanaWalutaException as err:
                print(err.msg)
                raise
            else:
                self._monety.append(m)
        else:
            print('Przesłany obiekt nie jest monetą')

        
    def wczytaj_monety(self, waluta):
        wczytane_monety = []

        try:
            file = open('lista.csv', 'r')    
            reader = csv.reader(file)
            
            for row in reader:

                try:
                    if len(row) != 2:
                        raise(ZlyFormatPlikuException("Zła iczba kolumn w pliku"))
                except ZlyFormatPlikuException as err:
                    print(err.msg)
                    raise err
                else:
                    nom = row[0]
                    n = row[1]

                try:
                    if Decimal(nom) not in self._obslugiwane_monety:
                        raise(ZlyNominalException("Nieobsługiwany nominał"))
                except ZlyNominalException as err:
                    print(err.msg)
                    raise err
                else:
                    for i in range(int(n)):
                        m = Moneta(nom,waluta)
                        wczytane_monety.append(m)

        except ListaMonetException as err:
            print('błąd wczytywania')
            wczytane_monety.clear()
        else:
            print('Sukces! Monety zostały wczytane')
            wczytane_monety = sorted(wczytane_monety, key=lambda x: x.nominal)
            for m in wczytane_monety:
                self.dodajMonete(m)
        finally:
            file.close()
                


