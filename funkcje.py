import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import csv
import random
import time

stan_zdrowy = "Zdrowy"
stan_chory = "Chory"
stan_ozdrowialy = "Ozdrowialy"

def symuluj(koniec_symulacji, graf, gamma, beta):
  liczba_wezlow = len(graf.keys())
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

def wrapper_symulacji(gamma=0.1, beta=0.02, koniec_symulacji=400, liczba_symulacji=100, plik_wejsciowy="krawedzie.csv", plik_wyjsciowy="wyjscie.csv"):

  graf = wczytaj_graf(plik_wejsciowy)

  wynik = {
    "chorzy": [],
    "ozdrowiali": [],
    "iteracje": [],
    "nr_symulacji": []
  }

  for i in range(0, liczba_symulacji):
    start = time.time()
    symulacja = symuluj(koniec_symulacji, graf, gamma, beta)
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

def wczytaj_graf(krawedzie):
  with open(krawedzie, newline='') as plik:
    reader = csv.reader(plik, delimiter=',')
    graf = {}
    for tekst in reader:
      poczatek = int(tekst[0])
      koniec = int(tekst[1])
      if(poczatek not in graf):
        graf[poczatek] = [koniec]
      else:
        graf[poczatek] = graf[poczatek] + [koniec]
      if(koniec not in graf):
        graf[koniec] = [poczatek]
      else:
        graf[koniec] = graf[koniec] + [poczatek]

  return graf

def konwertuj_do_networkX(graf):
  G = nx.DiGraph()
  wezly = graf.keys()
  krawedzie = [(zrodlo, cel) for (zrodlo, cele) in graf.items() for cel in cele]
  for w in wezly:
    G.add_node(w)
  for e in krawedzie:
    G.add_edge(e[0], e[1])
  return G

def rysuj_graf(self, G):
  pos = nx.spectral_layout(G)
  nx.draw_networkx(G, pos)
  plt.show()

def konwertuj_slownik_do_networkX(graf = {'1': ['1']}):
  G = nx.DiGraph()
  wezly_zrodla = set(graf.keys())
  wezly_cele = set([w for lista in list(graf.values()) for w in lista]) # flattening
  if(not set.issubset(wezly_zrodla, wezly_cele)):
    raise Exception("Wezly docelowe nie sa podzbiorem wszystkich wezlow")
  for zrodlo in wezly_zrodla:
    G.add_node(zrodlo)
  for zrodlo in wezly_zrodla:
    for cel in graf[zrodlo]:
      G.add_edge(zrodlo, cel)
  return G
  
def animuj(graf, kroki, plik_wyjsciowy):
  print(len(kroki))
  print("Konwertuje do networkX")
  G = konwertuj_do_networkX(graf)
  print("Obliczam pozycje")
  position = nx.spring_layout(G, iterations=10)
  figure, ax = plt.subplots(figsize=(10,8))
  def rysuj_krok(krok):
    ax.clear()
    # krok = k.copy()
    # print(krok)
    numer = krok["numer"]
    kolory = []
    wezly_id = []
    for wezel in graf:
      if(wezel != "numer"):
        wezly_id = wezly_id + [wezel]
        if(krok[wezel] == stan_chory):
          kolory = kolory + ["red"]
        elif(krok[wezel] == stan_zdrowy):
          kolory = kolory + ["green"]
        elif(krok[wezel] == stan_ozdrowialy):
          kolory = kolory + ["blue"]
        else:
          raise Exception("cos poszlo bardzo zle")
    ax.set_title(f"numer kroku: {numer}\n")
    nx.draw_networkx(G, position, nodelist=wezly_id, node_color=kolory)
    plt.savefig("gify/" + plik_wyjsciowy)
  
  # print("Rysuje animacje")
  # for krok in kroki:
  #   rysuj_krok(krok)
  ani = animation.FuncAnimation(figure, rysuj_krok, kroki, repeat=False)
  ani.save('./symulacja.gif', writer='imagemagick')
  #plt.show()

def generuj_graf_erdos(plik_wyjsciowy="wejscie/erdos.csv", n=100, sredni_stopien=10):
  p = float(sredni_stopien)/n
  graf = nx.gnp_random_graph(n,p)
  while(not nx.is_connected(graf)):
    graf = nx.gnp_random_graph(n,p)
  with open(plik_wyjsciowy, 'w') as plik:
    nx.write_edgelist(graf, plik_wyjsciowy, delimiter=',', data=False)
  stopnie = [graf.degree(wezel) for wezel in graf.nodes()]
  plt.hist(stopnie, bins=int(math.sqrt(len(stopnie))))
  plt.title("histogram rozkladu stopni wierzcholkow\nmodel Erdosa-Renyi, l. wezlow=" + str(n) + ", sr. stopien=" + str(sredni_stopien))
  plt.xlabel("stopnie wierzcholkow")
  plt.ylabel("czestosc")
  plt.savefig("wejscie/erdos_histogram.png")
  plt.clf()

def generuj_graf_barabasi(plik_wyjsciowy="wejscie/barabasi.csv", n=100, sredni_stopien=10):
  m = sredni_stopien // 2
  graf = nx.barabasi_albert_graph(n, m)
  while(not nx.is_connected(graf)):
    graf = nx.barabasi_albert_graph(n, m)
  with open(plik_wyjsciowy, 'w') as plik:
    nx.write_edgelist(graf, plik_wyjsciowy, delimiter=',', data=False)
  stopnie = [graf.degree(wezel) for wezel in graf.nodes()]
  plt.hist(stopnie, bins=int(math.sqrt(len(stopnie))))
  plt.title("histogram rozkladu stopni wierzcholkow\nmodel Barabasiego-Alberta, l. wezlow=" + str(n) + ", sr. stopien=" + str(sredni_stopien))
  plt.xlabel("stopnie wierzcholkow")
  plt.ylabel("czestosc")
  plt.savefig("wejscie/barabasi_histogram.png")
  plt.clf()

def generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.1):
  m = sredni_stopien // 2
  graf = nx.watts_strogatz_graph(n, sredni_stopien, polaczenia_dalekie)
  while(not nx.is_connected(graf)):
    graf = nx.watts_strogatz_graph(n, sredni_stopien, polaczenia_dalekie)
  with open(plik_wyjsciowy, 'w') as plik:
    nx.write_edgelist(graf, plik_wyjsciowy, delimiter=',', data=False)
  stopnie = [graf.degree(wezel) for wezel in graf.nodes()]
  plt.hist(stopnie, bins=int(math.sqrt(len(stopnie))))
  plt.title("histogram rozkladu stopni wierzcholkow\nmodel Wattsa-Strogatza, l. wezlow=" + str(n) + ", sr. stopien=" + str(sredni_stopien))
  plt.xlabel("stopnie wierzcholkow")
  plt.ylabel("czestosc")
  plt.savefig("wejscie/WattsStrogatz_histogram.png")
  plt.clf()

def rysuj_wykresy_chorych(nazwa, opis):
    plik = "wyjscie/" + nazwa + "_wynik.csv"
    dane = pd.read_csv(plik, delimiter=",")
    dane_zgroupowane = dane.groupby("nr_symulacji")
    dane_zgroupowane["chorzy"].value_counts()
    fig1, ax1 = plt.subplots(figsize=(8,6))
    ax1.set_title(nazwa + ": chorzy\n" + opis)
    for grupa in dane_zgroupowane.groups:
      symulacja = dane_zgroupowane.get_group(grupa)
      symulacja.plot(x="iteracje", y="chorzy", legend=False, ax=ax1, alpha=0.1, color="black")
    # df1.plot(kind="kde", ax=ax)
    ax1.set_ylabel("chorzy")
    plt.savefig(plik + "-chorzy.png")
    fig2, ax2 = plt.subplots(figsize=(8,6))
    ax2.set_title(nazwa + ": chorzy + ozdrowiali\n" + opis)
    for grupa in dane_zgroupowane.groups:
      symulacja = dane_zgroupowane.get_group(grupa)
      symulacja["chorzy + ozdrowiali"] = symulacja["chorzy"] + symulacja["ozdrowiali"]
      symulacja.plot(x="iteracje", y="chorzy + ozdrowiali", legend=False, ax=ax2, alpha=0.1, color="black")
    # df1.plot(kind="kde", ax=ax)
    ax2.set_ylabel("chorzy + ozdrowiali")
    plt.savefig(plik + "-chorzy_i_ozdrowiali.png")