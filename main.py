import random
import time
from funkcje import *

def wrapper_symulacji(gamma=0.1, beta=0.02, koniec_symulacji=400, liczba_symulacji=100, plik_wejsciowy="krawedzie.csv", plik_wyjsciowy="wyjscie.csv"):

  graf = wczytaj_graf(plik_wejsciowy)
  liczba_wezlow = len(graf.keys())

  def symuluj(koniec_symulacji):
    indeksy_chorych = random.sample(range(0, liczba_wezlow), 10)
    stary_stan = {i: (stan_chory if(i in indeksy_chorych) else stan_zdrowy) for i in range(0, liczba_wezlow)}
    
    kroki = [stary_stan]
    chorzy = []
    ozdrowiali = []
    
    for t in range(0, koniec_symulacji):
      nowy_stan = {}
      nowy_stan["numer"] = t
      for wezel in graf:
        if(stary_stan[wezel] == stan_chory):
          if(random.random() < gamma):
            nowy_stan[wezel] = stan_ozdrowialy
          else:
            nowy_stan[wezel] = stan_chory
        elif(stary_stan[wezel] == stan_zdrowy):
          # chorzy_sasiedzi = [sasiad for sasiad in graf[wezel] if stary_stan[sasiad] == stan_chory]
          # liczba_chorych_sasiadow = len(chorzy_sasiedzi)
          # prog = (1-(1-beta)**liczba_chorych_sasiadow)
          # if(random.random() < prog):
          #   nowy_stan[wezel] = stan_chory
          # else:
          #   nowy_stan[wezel] = stan_zdrowy
          for sasiad in graf[wezel]:
            if(stary_stan[sasiad] == stan_chory and random.random() < beta):
              nowy_stan[wezel] = stan_chory
          if wezel not in nowy_stan:
            nowy_stan[wezel] = stan_zdrowy
        elif(stary_stan[wezel] == stan_ozdrowialy):
            nowy_stan[wezel] = stan_ozdrowialy
        else:
          raise Exception("cos poszlo bardzo zle")
      chore_osoby_t = [wezel for wezel in nowy_stan if nowy_stan[wezel] == stan_chory]
      liczba_chorych_t = len(chore_osoby_t)
      ozdrowiale_osoby_t = [wezel for wezel in nowy_stan if nowy_stan[wezel] == stan_ozdrowialy]
      liczba_ozdrowialych_t = len(ozdrowiale_osoby_t)
      # print("S:I:R (t=" + str(t) + "): " + str(100-liczba_chorych_t-liczba_ozdrowialych_t) + ":" + str(liczba_chorych_t) + ":" + str(liczba_ozdrowialych_t))
      
      kroki = kroki + [nowy_stan]
      chorzy = chorzy + [liczba_chorych_t]
      ozdrowiali = ozdrowiali + [liczba_ozdrowialych_t]
      stary_stan = nowy_stan

    return {
      "chorzy": chorzy,
      "ozdrowiali": ozdrowiali,
      "kroki": kroki
    }
  
  wynik = {
    "chorzy": [],
    "ozdrowiali": [],
    "iteracje": [],
    "nr_symulacji": []
  }

  for i in range(0, liczba_symulacji):
    start = time.time()
    symulacja = symuluj(koniec_symulacji)
    end = time.time()
    print("czas wykonania symulacji "+ str(i)+": " + str(end-start) + "s")
    wynik["chorzy"] = wynik["chorzy"] + symulacja["chorzy"]
    wynik["ozdrowiali"] = wynik["ozdrowiali"] + symulacja["ozdrowiali"]
    wynik["iteracje"] = wynik["iteracje"] + [j for j in range(0, koniec_symulacji)]
    wynik["nr_symulacji"] = wynik["nr_symulacji"] + [i for j in range(0, koniec_symulacji)]

  with open(plik_wyjsciowy, 'w') as plik:
    plik.write("chorzy,ozdrowiali,iteracje,nr_symulacji\n")
    tekst=""
    for i in range(0, koniec_symulacji * liczba_symulacji):
      tekst = tekst + str(wynik["chorzy"][i])
      tekst = tekst + "," + str(wynik["ozdrowiali"][i])
      tekst = tekst + "," + str(wynik["iteracje"][i])
      tekst = tekst + "," + str(wynik["nr_symulacji"][i]) + '\n'
    plik.write(tekst)

konfiguracja = [
  ["wejscie/barabasi.csv", "wyjscie/barabasi_wynik.csv", "barabasi"],
  ["wejscie/erdos.csv", "wyjscie/erdos_wynik.csv", "erdos"]
]

for symulacja in konfiguracja:
  print(symulacja)
  wrapper_symulacji(plik_wejsciowy=symulacja[0], plik_wyjsciowy=symulacja[1])
  rysuj_wykresy_chorych(symulacja[2], "1000 wezlow, sredni stopien: 10")