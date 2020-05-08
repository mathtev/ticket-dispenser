Opis zadania
? Automat przechowuje informacje o monetach/banknotach znajduj�cych si� w
nim (1, 2, 5, 10, 20, 50gr, 1, 2, 5, 10, 20, 50z�) [dziedziczenie: mo�na napisa�
uniwersaln� klas� PrzechowywaczMonet po kt�rej dziedziczy� b�dzie automat]
? Okno z list� bilet�w w r�nych cenach (jako przyciski). Wymagane bilety:
20-minutowy, 40-minutowy, 60-minutowy w wariantach normalnym i ulgowym.
? Mo�liwo�� wybrania wi�cej ni� jednego rodzaju biletu. Mo�liwo��
wprowadzenia liczby bilet�w.
? Po wybraniu biletu pojawia si� okno z list� monet (przyciski) oraz
mo�liwo�ci� dodania kolejnego biletu lub liczby bilet�w.
? Interfejs ma dodatkowo zawiera� pole na wyb�r liczby wrzucanych
monet (domy�lnie jedna).
? Po wrzuceniu monet, kt�rych warto�� jest wi�ksza lub r�wna cenie
wybranych bilet�w, automat sprawdza czy mo�e wyda� reszt�.
? Brak reszty/mo�e wyda�: wyskakuje okienko z informacj� o zakupach, wydaje
reszt� (dolicza wrzucone monety, odlicza wydane jako reszta), wraca do
wyboru bilet�w.
? Nie mo�e wyda�: wyskakuje okienko z napisem "Tylko odliczona kwota"
oraz zwraca w�o�one monety.
Testy
1. Bilet kupiony za odliczon� kwot� - oczekiwany brak reszty.
2. Bilet kupiony p�ac�c wi�cej - oczekiwana reszta.
3. Bilet kupiony p�ac�c wi�cej, automat nie ma jak wyda� reszty - oczekiwana
informacja o b��dzie oraz zwr�cenie takiej samej liczby monet o tych
samych nomina�ach, co wrzucone.
4. Zakup biletu p�ac�c po 1gr - suma stu monet 1gr ma by� r�wna 1z� (dla float�w
suma sto razy 0.01+0.01+...+0.01 nie b�dzie r�wna 1.0). P�atno�ci mo�na dokona�
za pomoc� p�tli for w interpreterze.
5. Zakup dw�ch r�nych bilet�w naraz - cena powinna by� sum�.
6. Dodanie biletu, wrzucenie kilku monet, dodanie drugiego biletu, wrzucenie
pozosta�ych monet, zakup za odliczon� kwot� - oczekiwany brak reszty
(wrzucone monety nie zeruj� si� po dodaniu biletu).
7. Pr�ba wrzucenia ujemnej oraz nieca�kowitej liczby monet (oczekiwany komunikat
o b��dzie).