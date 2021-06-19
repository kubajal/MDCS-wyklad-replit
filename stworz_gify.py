from funkcje import *

konfiguracja = [
  ["wejscie/barabasi_100.csv", "barabasi"],
  ["wejscie/erdos_100.csv", "erdos"]
]

for symulacja in konfiguracja:
  print(symulacja)
  plik_wejsciowy=symulacja[0]
  nazwa=symulacja[1]
  graf = wczytaj_graf(plik_wejsciowy)
  wynik = symuluj(200, graf, gamma=0.1, beta=0.02)
  kroki = wynik["kroki"]
  animuj(graf, kroki, plik_wyjsciowy=nazwa + ".gif")
  # rysuj_wykresy_chorych(symulacja[2], "100 wezlow, sredni stopien: 10")