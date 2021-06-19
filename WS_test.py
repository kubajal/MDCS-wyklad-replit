from funkcje import *

generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_no_lockdown.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.1)
generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_lockdown.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0)

konfiguracja = [
  ["wejscie/WattsStrogatz_no_lockdown.csv", "wyjscie/WattsStrogatz_no_lockdown_wynik.csv", "WattsStrogatz_no_lockdown"],
  ["wejscie/WattsStrogatz_lockdown.csv", "wyjscie/WattsStrogatz_lockdown_wynik.csv", "WattsStrogatz_lockdown"]
]

for symulacja in konfiguracja:
  print(symulacja)
  wrapper_symulacji(plik_wejsciowy=symulacja[0], plik_wyjsciowy=symulacja[1])
  rysuj_wykresy_chorych(symulacja[2], "1000 wezlow, sredni stopien: 10")