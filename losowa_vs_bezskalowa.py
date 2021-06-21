from funkcje import *

# Aby uruchomić ten skrypt wybierz 'shell' w  prawym dolnym rogu i wpisz 'python losowa_vs_bezskalowa.py'.
# Zapoznaj się ponadto z 'funkcje.py'.

generuj_graf_barabasi(plik_wyjsciowy="wejscie/barabasi.csv", n=1000, sredni_stopien=6)
generuj_graf_erdos(plik_wyjsciowy="wejscie/erdos.csv", n=1000, sredni_stopien=6)

konfiguracja = [
  ["wejscie/barabasi.csv", "wyjscie/barabasi_wynik.csv", "barabasi"],
  ["wejscie/erdos.csv", "wyjscie/erdos_wynik.csv", "erdos"]
]

for symulacja in konfiguracja:
  print(symulacja)
  wrapper_symulacji(gamma=0.1, beta=0.02, poczatkowa_liczba_chorych=10, koniec_symulacji=400, liczba_symulacji=100, plik_wejsciowy=symulacja[0], plik_wyjsciowy=symulacja[1])
  rysuj_wykresy_chorych(symulacja[2], "1000 wezlow, sredni stopien: 10")