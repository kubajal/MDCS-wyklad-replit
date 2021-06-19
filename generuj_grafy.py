from funkcje import *

generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_no_lockdown.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.1)
generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz_lockdown.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.01)
generuj_graf_barabasi(plik_wyjsciowy="wejscie/barabasi_100.csv", n=100, sredni_stopien=8)
generuj_graf_erdos(plik_wyjsciowy="wejscie/erdos_100.csv", n=100, sredni_stopien=8)