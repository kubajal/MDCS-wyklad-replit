from funkcje import *

# Aby uruchomić ten skrypt wybierz 'shell' w  prawym dolnym rogu i wpisz 'python stworz_gify.py'.
# Zapoznaj się ponadto z 'funkcje.py'.

konfiguracja = [
  ["wejscie/barabasi_40.csv", "siec bezskalowa - 40 wezlow"],
  ["wejscie/erdos_40.csv", "siec losowa - 40 wezlow"]
]

for symulacja in konfiguracja:  
  print(symulacja)
  plik_wejsciowy=symulacja[0]
  nazwa=symulacja[1]
  graf = wczytaj_graf(plik_wejsciowy)
  gamma = 0.1
  beta = 0.03
  wynik = symuluj(50, graf, gamma=gamma, beta=beta, poczatkowa_liczba_chorych=4)
  wynik["gamma"] = gamma
  wynik["beta"] = beta
  wynik["nazwa"] = nazwa
  animuj(graf, wynik, plik_wyjsciowy=nazwa + ".gif")
  
  # rysuj_wykresy_chorych(symulacja[2], "100 wezlow, sredni stopien: 10")