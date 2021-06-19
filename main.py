from funkcje import *

konfiguracja = [
  ["wejscie/barabasi.csv", "wyjscie/barabasi_wynik.csv", "barabasi"],
  ["wejscie/erdos.csv", "wyjscie/erdos_wynik.csv", "erdos"]
]

for symulacja in konfiguracja:
  print(symulacja)
  wrapper_symulacji(plik_wejsciowy=symulacja[0], plik_wyjsciowy=symulacja[1])
  rysuj_wykresy_chorych(symulacja[2], "1000 wezlow, sredni stopien: 10")