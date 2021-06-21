from funkcje import *

# Aby uruchomić ten skrypt wybierz 'shell' w  prawym dolnym rogu i wpisz 'python generuj_grafy.py'.
# Zapoznaj się ponadto z 'funkcje.py'.

generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_no_lockdown.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.1)
generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_lockdown.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.01)
generuj_graf_barabasi(plik_wyjsciowy="wejscie/barabasi_40.csv", n=40, sredni_stopien=4)
generuj_graf_erdos(plik_wyjsciowy="wejscie/erdos_40.csv", n=40, sredni_stopien=4)