from funkcje import * 

# Aby uruchomić ten skrypt wybierz 'shell' w  prawym dolnym rogu i wpisz 'python male_swiaty.py'.
# Zapoznaj się ponadto z 'funkcje.py'.

generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_no_lockdown.csv", n=1000, sredni_stopien=10, polaczenia_dalekie=0.1)

generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_half_lockdown.csv", n=1000, sredni_stopien=10, polaczenia_dalekie=0.01)

generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_full_lockdown.csv", n=1000, sredni_stopien=10, polaczenia_dalekie=0)

konfiguracja = [
  ["wejscie/WattsStrogatz_no_lockdown.csv", "wyjscie/WattsStrogatz_no_lockdown_wynik.csv", "WattsStrogatz_no_lockdown"]#,
  ["wejscie/WattsStrogatz_half_lockdown.csv", "wyjscie/WattsStrogatz_half_lockdown_wynik.csv", "WattsStrogatz_half_lockdown"],
  ["wejscie/WattsStrogatz_full_lockdown.csv", "wyjscie/WattsStrogatz_full_lockdown_wynik.csv", "WattsStrogatz_full_lockdown"]
]

for symulacja in konfiguracja:
  print(symulacja)
  wrapper_symulacji(gamma=0.1, beta=0.02, poczatkowa_liczba_chorych=10, koniec_symulacji=400, liczba_symulacji=100, plik_wejsciowy=symulacja[0], plik_wyjsciowy=symulacja[1])
  rysuj_wykresy_chorych(symulacja[2], "1000 wezlow, sredni stopien: 10")