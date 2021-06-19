import csv
import random
from funkcje import *

koniec_symulacji = 200

Zdrowy = "Zdrowy"
Chory = "Chory"
Ozdrowialy = "Ozdrowialy"

# graf wygenerowany przy pomocy PaRMAT: https://github.com/kubajal/PaRMAT
# power law itp.
with open('krawedzie.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  graf = {}
  for wiersz in reader:
    poczatek = int(wiersz[0])
    koniec = int(wiersz[1])
    if(poczatek not in graf):
      graf[poczatek] = [koniec]
    else:
      graf[poczatek] = graf[poczatek] + [koniec]
    if(koniec not in graf):
      graf[koniec] = [poczatek]
    else:
      graf[koniec] = graf[koniec] + [poczatek]

poczatkowy_stan = {}
with open('wezly.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  i = 0
  for wiersz in reader:
    if(wiersz[0] == "1"):
      poczatkowy_stan[i] = Zdrowy
    else:
      poczatkowy_stan[i] = Chory
    i = i + 1
poczatkowy_stan["numer"] = 0

# print(stary_stan)
# print("------")

liczba_wezlow = len(graf.keys())
# print("liczba_wezlow=" + str(liczba_wezlow))

gamma = 0.05
beta = 0.10
r = beta / gamma

stary_stan = poczatkowy_stan
kroki_symulacji = [stary_stan]

for t in range(1, koniec_symulacji):
  nowy_stan = stary_stan
  for wezel in graf:

    if(stary_stan[wezel] == "Chory"):
      if(random.random() < gamma):
        nowy_stan[wezel] = "Ozdrowialy"

    elif(stary_stan[wezel] == "Zdrowy"):
      for sasiad in graf[wezel]:
        if stary_stan[sasiad] == "Chory":
          if(random.random() < beta):
            nowy_stan[wezel] = "Chory"
  
  stary_stan = nowy_stan

  kroki_symulacji = kroki_symulacji + [nowy_stan]
  
  S = len([wezel for wezel in nowy_stan if nowy_stan[wezel] == "Zdrowy"])
  I = len([wezel for wezel in nowy_stan if nowy_stan[wezel] == "Chory"])
  R = len([wezel for wezel in nowy_stan if nowy_stan[wezel] == "Ozdrowialy"])
  print("S:I:R (t=" + str(t) + "): " + str(S) + ":" + str(I) + ":" + str(R))
  
# print(kroki_symulacji)
# animuj(graf, kroki_symulacji)
# print(kroki_symulacji)
# animuj(graf, kroki_symulacji)