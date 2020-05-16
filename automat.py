from decimal import Decimal, ROUND_HALF_UP

grosz = Decimal('.01')
lista_nominalow = ['0.01', '0.02', '0.05', '0.1', '0.2', '0.5', '1', '2', '5','10','20','50']
obslugiwane_nominaly = tuple(map(Decimal, lista_nominalow))


class Error(Exception): 
    pass
  
class NieznanaWalutaException(Error):
    
    def __init__(self, msg):
        
        self.msg = msg 

class ZlyNominalException(Error):
    
    def __init__(self, msg):
        
        self.msg = msg


class Moneta:
    
    def __init__(self, nominal, waluta):

        nominal = Decimal(str(nominal))

        try:
            if nominal not in obslugiwane_nominaly:
                raise(ZlyNominalException("Zły nominał"))
            
        except ZlyNominalException as err:
            print(err.msg)
            raise

        else:
            self._nominal = nominal
            self.waluta = waluta

    @property
    def nominal(self):
        return self._nominal.quantize(grosz, ROUND_HALF_UP)

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
        self.doZaplaty = Decimal('0')

    def reset(self):
        self.doZaplaty = Decimal('0')
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


moneta1 = Moneta(1, 'PLN')
moneta2 = Moneta(0.1, 'PLN')
moneta3 = Moneta(0.05, 'PLN')
automat = Automat(obslugiwane_nominaly)

automat.dodajMonete(moneta1)
automat.dodajMonete(moneta2)
automat.dodajMonete(moneta3)

print(moneta3.nominal)
moneta3.nominal = 0.2
print(moneta3.nominal)

