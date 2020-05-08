Opis zadania
? Automat przechowuje informacje o monetach/banknotach znajduj¹cych siê w
nim (1, 2, 5, 10, 20, 50gr, 1, 2, 5, 10, 20, 50z³) [dziedziczenie: mo¿na napisaæ
uniwersaln¹ klasê PrzechowywaczMonet po której dziedziczyæ bêdzie automat]
? Okno z list¹ biletów w ró¿nych cenach (jako przyciski). Wymagane bilety:
20-minutowy, 40-minutowy, 60-minutowy w wariantach normalnym i ulgowym.
? Mo¿liwoœæ wybrania wiêcej ni¿ jednego rodzaju biletu. Mo¿liwoœæ
wprowadzenia liczby biletów.
? Po wybraniu biletu pojawia siê okno z list¹ monet (przyciski) oraz
mo¿liwoœci¹ dodania kolejnego biletu lub liczby biletów.
? Interfejs ma dodatkowo zawieraæ pole na wybór liczby wrzucanych
monet (domyœlnie jedna).
? Po wrzuceniu monet, których wartoœæ jest wiêksza lub równa cenie
wybranych biletów, automat sprawdza czy mo¿e wydaæ resztê.
? Brak reszty/mo¿e wydaæ: wyskakuje okienko z informacj¹ o zakupach, wydaje
resztê (dolicza wrzucone monety, odlicza wydane jako reszta), wraca do
wyboru biletów.
? Nie mo¿e wydaæ: wyskakuje okienko z napisem "Tylko odliczona kwota"
oraz zwraca w³o¿one monety.
Testy
1. Bilet kupiony za odliczon¹ kwotê - oczekiwany brak reszty.
2. Bilet kupiony p³ac¹c wiêcej - oczekiwana reszta.
3. Bilet kupiony p³ac¹c wiêcej, automat nie ma jak wydaæ reszty - oczekiwana
informacja o b³êdzie oraz zwrócenie takiej samej liczby monet o tych
samych nomina³ach, co wrzucone.
4. Zakup biletu p³ac¹c po 1gr - suma stu monet 1gr ma byæ równa 1z³ (dla floatów
suma sto razy 0.01+0.01+...+0.01 nie bêdzie równa 1.0). P³atnoœci mo¿na dokonaæ
za pomoc¹ pêtli for w interpreterze.
5. Zakup dwóch ró¿nych biletów naraz - cena powinna byæ sum¹.
6. Dodanie biletu, wrzucenie kilku monet, dodanie drugiego biletu, wrzucenie
pozosta³ych monet, zakup za odliczon¹ kwotê - oczekiwany brak reszty
(wrzucone monety nie zeruj¹ siê po dodaniu biletu).
7. Próba wrzucenia ujemnej oraz nieca³kowitej liczby monet (oczekiwany komunikat
o b³êdzie).