import csv
from decimal import Decimal, ROUND_HALF_UP

GROSZ = Decimal('.01')
LISTA_NOMINALOW = ['0.01', '0.02', '0.05', '0.1', '0.2', '0.5', '1', '2', '5','10','20','50']
OBSLUGIWANE_NOMINALY = tuple(map(Decimal, LISTA_NOMINALOW))


class Error(Exception): 
    """Klasa bazowa dla własnych wyjątków."""
    pass

class NieznanaWalutaException(Error):
    """Wyjątek, waluta jest nieznana.
    
    Attributes:
        msg: str, wiadomość o błędzie.
    """
    def __init__(self, msg):
        self.msg = msg 

class ListaMonetException(Error):
    """Wyjątek, złe działania na liście monet.
    
    Attributes:
        msg: str, wiadomość o błędzie.
    """
    def __init__(self, msg):
        self.msg = msg

class nieMoznaZwrocicMonetException(Error):
    """Wyjątek, nie można zwrócić monet.
    
    Attributes:
        msg: str, wiadomość o błędzie.
    """
    def __init__(self, msg):
        self.msg = msg 

class ZlyNominalException(ListaMonetException):
    """Wyjątek, zły nominał.
    
    Attributes:
        msg: str, wiadomość o błędzie.
    """
    def __init__(self, msg):
        self.msg = msg

class ZlyFormatPlikuException(ListaMonetException):
    """Wyjątek, zły format pliku.
    
    Attributes:
        msg: str, wiadomość o błędzie.
    """
    def __init__(self, msg):
        self.msg = msg


class Moneta:
    """Reprezentacja monety.

    Attributes:
        _nominal: Decimal, wartość monety.
        waluta: str, określa walutę.
    """
    def __init__(self, nominal, waluta):
        """Konstruktor dla Moneta."""
        nominal = Decimal(str(nominal))

        if nominal not in OBSLUGIWANE_NOMINALY:
            raise(ZlyNominalException(f'Zły nominał: {nominal}'))

        else:
            self._nominal = nominal
            self.waluta = waluta

    @property
    def nominal(self):
        """Odczytaj nominał."""
        return self._nominal.quantize(GROSZ, ROUND_HALF_UP)

    @nominal.setter
    def nominal(self, n):
        """Ustaw nominał.
        
        Args:
            n: Decimal, nowy nominał.
        """
        self._nominal = Decimal(str(n))

    def __str__(self):
        return f'Moneta o wartości: {self.nominal}, waluta: {self.waluta}'

    def __repr__(self):
        return f'Moneta({self.nominal}, {self.waluta})'

    def __eq__(self, o):
        return self.nominal == o.nominal and self.waluta == o.waluta


class PrzechowywaczMonet:
    """Służy do przechowywania monet.

    Attributes:
        obslugiwane_monety: tuple, określa jakie nominały są dozwolone.
        _monety: list, przechowywane monety.
    """
    def __init__(self, obslugiwane_monety):
        """Konstruktor dla PrzechowywaczMonet, ustawia domyślne wartości.
        
        Args:
            obslugiwane_monety: tuple, określa jakie nominały są dozwolone.
        """
        self.obslugiwane_monety = obslugiwane_monety
        self._monety = []

    def dodaj_monete(self, m):
        """Dodaje monetę do listy _monety.
        
        Args:
            m: Moneta, moneta do dodania.
        """
        if isinstance(m,Moneta):
            self._monety.append(m)
        else:
            print('Przesłany obiekt nie jest monetą')

    def suma_monet(self):
        """Sumuje wszystkie nominały w liście _monety.
        
        Returns:
            Suma monet w liście.
        """
        suma = Decimal('0')
        suma = sum(m.nominal for m in self._monety)
        return suma

    def zwroc_monete(self, nominal):
        """Zwraca z listy _monety monetę o określonym nominale.

        Args:
            nominal: Decimal, określa wartość szukanej monety.
        
        Returns:
            Obiekt monety, jeśli znaleziono szukany nominał w liście, inaczej None
        """
        nominal = Decimal(str(nominal))
        zwrotna = None
        for moneta in self._monety:
            if moneta.nominal == nominal:
                zwrotna = moneta
                self._monety.remove(moneta)
                break
        return zwrotna


class Automat(PrzechowywaczMonet):
    """Automat przechowywujący monety.

    Attributes:
        do_zaplaty: Decimal, kwota do zapłaty.
        wartosc_wrzuconych: Decimal, wartość monet wrzuconych przez użytkownika.
        liczba_biletow: int, liczba rodzai dostępnych biletów.
        wybrane_bilety: list, zawiera liczby int określające liczbę biletów, jakie
            zostały wybrane przez użytkownika, dla każdego rodzaju.
    """

    OBSLUGIWANA_WALUTA = 'PLN'
    CENY_BILETOW = tuple(map(Decimal, ['2.40','3.70','4.20','1.70','2.20','2.50']))
    
    def __init__(self, obslugiwane_monety):
        """Konstruktor dla Automat. Ustawia domyślne wartości atrybutów"""
        super().__init__(obslugiwane_monety)
        self.do_zaplaty = Decimal('0')
        self.wartosc_wrzuconych = Decimal('0')
        self.liczba_biletow = 6      #liczba rodzai biletów
        self.wybrane_bilety = [0]*self.liczba_biletow

    def reset(self):
        """Resetuje atrybuty do wartości domyślnych"""
        self.do_zaplaty = Decimal('0')
        self.wartosc_wrzuconych = Decimal('0')
        self._monety.clear()
        self.wybrane_bilety = [0]*self.liczba_biletow

    def dodaj_monete(self, moneta):
        """Dodaje monetę do listy _monety.
        
        Args:
            m: Moneta, moneta do dodania.
        
        Raises:
            NieznanaWalutaException jeśli waluta monety nie jest obsługiwana 
                przez automat.
        """
        if not isinstance(moneta, Moneta): 
            print('Przesłany obiekt nie jest monetą')
            return
        if moneta.waluta != self.OBSLUGIWANA_WALUTA:
            raise NieznanaWalutaException(f'Nieznana waluta: {moneta.waluta}')
        self._monety.append(moneta)

    def wrzuc_monete(self, moneta, liczba):
        """Dadaje monetę oraz zwiększa wartość wrzuconych o jej nominał
        
        Args:
            moneta: Moneta, moneta wrucona przez użytkownika.
            liczba: int, liczba wrzuconych monet o danym nominale.
        """
        for i in range(liczba):
            self.dodaj_monete(moneta)
        self.wartosc_wrzuconych += liczba*moneta.nominal

    def zaladuj_monety(self, liczba, nominal):
        """Załaduj wrzucone monety.
        
        Args:
            liczba: int, liczba wrzuconych monet o danym nominale.
            nominal: Decimal, określa wartość monety.

        Raises:
            ValueError: Jeśli wprowadzona wartość jest nieprawidłowa.
        """
        try:
            liczba = int(liczba)
            if liczba <= 0:
                raise ValueError('Wprowadzono złe dane')
        except ValueError as err:
            print(str(err))
            raise 
        else:
            moneta = Moneta(nominal, self.OBSLUGIWANA_WALUTA)
            self.wrzuc_monete(moneta, liczba)

    def wydaj_reszte(self):
        """Oblicz i wydaj resztę z wrzuconych monet.

        Returns:
            Lista zawierająca resztę z wrzuconych monet jeśli automat może wydać,
            inaczej lista monet, których wartość wynosi tyle co tych które zostały wrzucone.

        Raises:
            nieMoznaZwrocicMonetException: Jeśli automat nie może zwrócić.
        """
        
        do_wydania = Decimal(str(self.wartosc_wrzuconych - self.do_zaplaty))
        wydane_monety = []
        
        if do_wydania < 0:
            print('Wprowadzona kwota jest zbyt mała')
            return self.zwroc_pieniadze()
        elif do_wydania == 0:
            return wydane_monety
        elif self.suma_monet() < do_wydania:
            print('Automat nie może wydać reszty')
            return self.zwroc_pieniadze()
        else:
            for nominal in reversed(self.obslugiwane_monety):
                while do_wydania >= nominal:
                    zwrocona = self.zwroc_monete(nominal)
                    if zwrocona is None:
                        break
                    do_wydania -= zwrocona.nominal
                    wydane_monety.append(zwrocona)
                if do_wydania == 0:
                    break
        try:
            if do_wydania > 0:
                raise(nieMoznaZwrocicMonetException(f'Automat nie może wydać reszty '
                                                    f'{do_wydania}.'))
        except nieMoznaZwrocicMonetException as err:
            print(err.msg)
            for m in wydane_monety:
                self.dodaj_monete(m)
            wydane_monety.clear()
            return self.zwroc_pieniadze()
        return wydane_monety

    def zwroc_pieniadze(self):
        """Zwróć wszystkie monety

        Returns:
            Lista monet których wartość odpowiada wszystkim wrzuconym przez użytkownika

        Raises:
            nieMoznaZwrocicMonetException: Jeśli automat nie może zwrócić.
        """
        do_zwrotu = []
        for nominal in reversed(self.obslugiwane_monety):
            while self.wartosc_wrzuconych >= nominal:
                zwrocona = self.zwroc_monete(nominal)
                if zwrocona is None:
                    break
                self.wartosc_wrzuconych -= zwrocona.nominal
                do_zwrotu.append(zwrocona)
            if self.wartosc_wrzuconych == 0:
                break
        if self.wartosc_wrzuconych != 0:
            raise(nieMoznaZwrocicMonetException(f'Automat nie może zwrócić '
                                                f'{self.wartosc_wrzuconych}.'))
        return do_zwrotu

    def dodaj_bilet(self, idx):
        """Dodaj bilet do automatu

        Args: 
            idx: int, określa rodzaj wybranego biletu.
        """
        self.do_zaplaty += self.CENY_BILETOW[idx]
        self.wybrane_bilety[idx] += 1
        
    def usun_bilet(self, idx):
        """Usuń bilet do automatu

        Args: 
            idx: int, określa rodzaj biletu do usunięcia.
        """
        self.do_zaplaty -= self.CENY_BILETOW[idx]
        self.wybrane_bilety[idx] -= 1

    def wczytaj_monety(self, waluta):
        """Wczytaj monety z pliku

        Args:
            waluta: str, określa na jaką walutę ustawić wczytane monety.

        Raises:
            ListaMonetException: jeśli plik ma zły format lub wczytany 
                nominał jest nieprawidłowy.
        """

        wczytane_monety = []
        try:
            with open('lista.csv', 'r') as file:  
                reader = csv.reader(file)  
                for row in reader:
                    try:
                        if len(row) != 2:
                            raise(ZlyFormatPlikuException("Zła iczba kolumn w pliku"))
                    except ZlyFormatPlikuException as err:
                        print(err.msg)
                        raise err
                    else:
                        nominal = row[0]
                        liczba = int(row[1])
                    try:
                        if Decimal(nominal) not in self.obslugiwane_monety:
                            raise(ZlyNominalException("Nieobsługiwany nominał"))
                    except ZlyNominalException as err:
                        print(err.msg)
                        raise err
                    else:
                        monety = [Moneta(nominal, waluta) for x in range(liczba)]
                        for m in monety:
                            wczytane_monety.append(m)
        except ListaMonetException as err:
            print('błąd wczytywania')
            wczytane_monety.clear()
            raise
        else:
            print('Sukces! Monety zostały wczytane')
            #wczytane_monety = sorted(wczytane_monety, key=lambda x: x.nominal)
            for m in wczytane_monety:
                self.dodaj_monete(m)
                


