# Opis zadania

○ Automat przechowuje informacje o monetach/banknotach znajdujących się w
nim (1, 2, 5, 10, 20, 50gr, 1, 2, 5, 10, 20, 50zł) [dziedziczenie: można napisać
uniwersalną klasę PrzechowywaczMonet po której dziedziczyć będzie automat]

○ Okno z listą biletów w różnych cenach (jako przyciski). Wymagane bilety:
20-minutowy, 40-minutowy, 60-minutowy w wariantach normalnym i ulgowym.

○ Możliwość wybrania więcej niż jednego rodzaju biletu. Możliwość
wprowadzenia liczby biletów.

○ Po wybraniu biletu pojawia się okno z listą monet (przyciski) oraz
możliwością dodania kolejnego biletu lub liczby biletów.

○ Interfejs ma dodatkowo zawierać pole na wybór liczby wrzucanych
monet (domyślnie jedna).

○ Po wrzuceniu monet, których wartość jest większa lub równa cenie
wybranych biletów, automat sprawdza czy może wydać resztę.

■ Brak reszty/może wydać: wyskakuje okienko z informacją o zakupach, wydaje
resztę (dolicza wrzucone monety, odlicza wydane jako reszta), wraca do
wyboru biletów.

■ Nie może wydać: wyskakuje okienko z napisem "Tylko odliczona kwota"
oraz zwraca włożone monety.

# Testy

1. Bilet kupiony za odliczoną kwotę - oczekiwany brak reszty.

2. Bilet kupiony płacąc więcej - oczekiwana reszta.

3. Bilet kupiony płacąc więcej, automat nie ma jak wydać reszty - oczekiwana
informacja o błędzie oraz zwrócenie takiej samej liczby monet o tych
samych nominałach, co wrzucone.

4. Zakup biletu płacąc po 1gr - suma stu monet 1gr ma być równa 1zł (dla floatów
suma sto razy 0.01+0.01+...+0.01 nie będzie równa 1.0). Płatności można dokonać
za pomocą pętli for w interpreterze.

5. Zakup dwóch różnych biletów naraz - cena powinna być sumą.

6. Dodanie biletu, wrzucenie kilku monet, dodanie drugiego biletu, wrzucenie
pozostałych monet, zakup za odliczoną kwotę - oczekiwany brak reszty
(wrzucone monety nie zerują się po dodaniu biletu).

7. Próba wrzucenia ujemnej oraz niecałkowitej liczby monet (oczekiwany komunikat
o błędzie).

https://github.com/mathtev/ticket-dispenser
