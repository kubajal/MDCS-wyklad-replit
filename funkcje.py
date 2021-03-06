import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import csv
import random
import time

# Funkcja wykonująca symulację rozchodzenia się epidemii na podanym grafie.
# dlugosc_symulacji - ile kroków ma mieć symulacja
# graf - słownik reprezentujący graf
# gamma i beta - współczynniki rozchodzenia się epidemii
# poczatkowa_liczba_chorych - ile wierzchołków w grafie ma być na początek zakażonych
def symuluj(dlugosc_symulacji, graf, gamma, beta, poczatkowa_liczba_chorych=1):

  # obliczamy ile jest wierzchołków w grafie
  liczba_wezlow = len(graf.keys())

  # losujemy numery chorych wierzchołków (będzie ich tyle ile wynosi poczatkowa_liczba_chorych)
  indeksy_chorych = random.sample(range(0, liczba_wezlow), poczatkowa_liczba_chorych)

  # będziemy przechowywać stan symulacji jako słownik węzeł->status (czyli każdy węzeł jest na razie albo 'chory' albo 'zdrowy')
  stan_poczatkowy = {i: ("Chory" if(i in indeksy_chorych) else "Zdrowy") for i in range(0, liczba_wezlow)}
  
  # dodatkowo zapisujemy numer kroku symmulacji
  stan_poczatkowy['numer'] = 0

  # dodajemy stan_poczatkowy do listy krokow symulacji
  kroki = [stan_poczatkowy]
  chorzy = []
  ozdrowiali = []
  
  # zaczynamy symulację...
  stary_stan = stan_poczatkowy
  for t in range(0, dlugosc_symulacji):
    
    # przygotowujemy słownik do przechowywania stanu wszystkich wierzchołków na koniec kroku symulacji
    nowy_stan = {}
    nowy_stan["numer"] = t

    # przechodzimy przez wszystkie węzły i obliczamy ich stan na koniec kroku symulacji
    for wezel in graf:

      # jeśli węzeł jest chory...
      if stary_stan[wezel] == "Chory":
        if random.random() < gamma:
          nowy_stan[wezel] = "Ozdrowialy"
        else:
          nowy_stan[wezel] = "Chory"

      # jeśli węzeł jest zdrowy...      
      elif stary_stan[wezel] == "Zdrowy":
        for sasiad in graf[wezel]:
          if stary_stan[sasiad] == "Chory" and random.random() < beta:
            nowy_stan[wezel] = "Chory"
        if wezel not in nowy_stan:
          nowy_stan[wezel] = "zdrowy"
      
      # jeśli węzel jest ozdrowiały
      elif stary_stan[wezel] == "Ozdrowialy":
          nowy_stan[wezel] = "Ozdrowialy"
      
      # nie ma więcej stanów niż 'chory', 'zdrowy' i 'ozdrowialy', więc jeśli tu doszliśmy to coś poszło źle
      else:
        raise Exception("cos poszlo bardzo zle")
    
    # wybieramy osoby chore na koniec kroku symulacji
    chore_osoby_t = [wezel for wezel in nowy_stan if nowy_stan[wezel] == "Chory"]
    
    # obliczamy liczbę chorych na koniec kroku symulacji
    liczba_chorych_t = len(chore_osoby_t)

    # wybieramy osoby ozdrowiale na koniec kroku symulacji
    ozdrowiale_osoby_t = [wezel for wezel in nowy_stan if nowy_stan[wezel] == "Ozdrowialy"]

    # obliczamy liczbę ozdrowiałych na koniec kroku symulacji
    liczba_ozdrowialych_t = len(ozdrowiale_osoby_t)
    
    # zapisujemy stan, liczbę chorych i liczbę ozdrowiałych do odpowiednich tablic, które zwrócimy na koniec symulacji
    kroki = kroki + [nowy_stan]
    chorzy = chorzy + [liczba_chorych_t]
    ozdrowiali = ozdrowiali + [liczba_ozdrowialych_t]
    stary_stan = nowy_stan

  # zwracmy wynik symulacji jako słownik, pod odpowiednimi kluczami są tablice z uzyskanymi w każdym kroku liczbami chorych, liczbami zdrowych i stanami wierzchołków
  return {
    "chorzy": chorzy,
    "ozdrowiali": ozdrowiali,
    "kroki": kroki
  }

# Funkcja do wykonania podanej liczby symulacji na grafie.
# gamma i beta - parametry rozchodzenia się symulacji
# poczatkowa_liczba_chorych - ile wierzchołków ma być zakażonych na początku symulacji
# dlugosc_symulacji - ile kroków ma mieć symulacja
# liczba_symulacji - ile przeprowadzić symulacji (im więcej tym dokładniejsze wyniki uzyskamy, ale symulowanie będzie dłużej trwało)
# plik_wejsciowy i plik_wyjsciowy - nazwy odpowiednich plików CSV (każda linia zawiera jedną krawędź)
def wrapper_symulacji(gamma=0.1, beta=0.02, poczatkowa_liczba_chorych=1, dlugosc_symulacji=400, liczba_symulacji=100, plik_wejsciowy="krawedzie.csv", plik_wyjsciowy="wyjscie.csv"):

  # wczytujemy graf z pliku CSV
  graf = wczytaj_graf(plik_wejsciowy)

  # przygotowujemy słownik do wyjścia
  wynik = {
    "chorzy": [],
    "ozdrowiali": [],
    "iteracje": [],
    "nr_symulacji": []
  }

  # pętla do wywoływania symulacji
  for i in range(0, liczba_symulacji):

    # zapisujemy czas rozpoczęcia symulacji
    start = time.time()

    # wykonujemy symulację
    symulacja = symuluj(dlugosc_symulacji, graf, gamma, beta, poczatkowa_liczba_chorych)
    
    # zapisujemy czas zakończenia symulacji
    end = time.time()

    print("czas wykonania symulacji "+ str(i)+": " + str(end-start) + "s")

    # łączymy słownik, który uzyskaliśmy na wyjściu funkcji symuluj() ze słownikiem, do którego zbiorczo zapisujemy wszystkie wyniki
    wynik["chorzy"] = wynik["chorzy"] + symulacja["chorzy"]
    wynik["ozdrowiali"] = wynik["ozdrowiali"] + symulacja["ozdrowiali"]
    wynik["iteracje"] = wynik["iteracje"] + [j for j in range(0, dlugosc_symulacji)]
    wynik["nr_symulacji"] = wynik["nr_symulacji"] + [i for j in range(0, dlugosc_symulacji)]

  # wynik wszystkich symulacji zapisujemy do plik_wyjsciowy w formacie CSV (w każdym wierszu podajemy:
  # - liczbę chorych
  # - liczbę ozdrowiałych
  # - numer kroku (iteracji)
  # - numer symulacji
  with open(plik_wyjsciowy, 'w') as plik:
    plik.write("chorzy,ozdrowiali,iteracje,nr_symulacji\n")
    tekst=""
    for i in range(0, dlugosc_symulacji * liczba_symulacji):
      tekst = tekst + str(wynik["chorzy"][i])
      tekst = tekst + "," + str(wynik["ozdrowiali"][i])
      tekst = tekst + "," + str(wynik["iteracje"][i])
      tekst = tekst + "," + str(wynik["nr_symulacji"][i]) + '\n'
    plik.write(tekst)

# Funkcja pomocnicza do wczytywania grafu z pliku CSV (w każdym wierszu jest jedna krawędź)
def wczytaj_graf(krawedzie):
  with open(krawedzie, newline='') as plik:
    reader = csv.reader(plik, delimiter=',')
    graf = {}
    for tekst in reader:
      poczatek_krawedzi = int(tekst[0])
      koniec_krawedzzi = int(tekst[1])
      if(poczatek_krawedzi not in graf):
        graf[poczatek_krawedzi] = [koniec_krawedzzi]
      else:
        graf[poczatek_krawedzi] = graf[poczatek_krawedzi] + [koniec_krawedzzi]
      if(koniec_krawedzzi not in graf):
        graf[koniec_krawedzzi] = [poczatek_krawedzi]
      else:
        graf[koniec_krawedzzi] = graf[koniec_krawedzzi] + [poczatek_krawedzi]

  return graf

# Funkcja pomocnicza potrzebna do rysowania grafu. Nie musisz wiedzieć co ona robi.
def konwertuj_do_networkX(graf):
  G = nx.DiGraph()
  stopnie = [[wezel, len(graf[wezel])] for wezel in graf]
  def klucz(element):
    [x, y] = element
    return y
  posortowane = sorted(stopnie, key=klucz)
  wezly = [wezel for [wezel, stopien] in posortowane]
  krawedzie = [(zrodlo, cel) for (zrodlo, cele) in graf.items() for cel in cele]
  for w in wezly:
    G.add_node(w)
  for e in krawedzie:
    G.add_edge(e[0], e[1])
  return G

# Funkcja pomocnicza potrzebna do rysowania grafu. Nie musisz wiedzieć co ona robi.
def rysuj_graf(self, G):
  pos = nx.spectral_layout(G)
  nx.draw_networkx(G, pos)
  plt.show()

# Funkcja pomocnicza potrzebna do rysowania grafu. Nie musisz wiedzieć co ona robi.
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
  
# Funkcja pomocnicza potrzebna do rysowania plików GIF. Nie musisz wiedzieć co ona robi.
def animuj(graf, wynik_symulacji, plik_wyjsciowy):
  n = 10
  # wybierz co n-ta klatke symulacji
  # aby szybciej generowal sie GIF
  kroki = wynik_symulacji["kroki"][1::n]
  gamma = wynik_symulacji["gamma"]
  nazwa = wynik_symulacji["nazwa"]
  beta = wynik_symulacji["beta"]
  
  print("Konwertuje do networkX")
  G = konwertuj_do_networkX(graf)
  print("Obliczam pozycje")
  position = nx.circular_layout(G, scale=10)
  figure, ax = plt.subplots(figsize=(10,8))
  def rysuj_krok(krok):
    ax.clear()
    numer = krok["numer"]
    kolory = []
    wezly_id = []
    for wezel in graf:
      if(wezel != "numer"):
        wezly_id = wezly_id + [wezel]
        if(krok[wezel] == "Chory"):
          kolory = kolory + ["red"]
        elif(krok[wezel] == "Zdrowy"):
          kolory = kolory + ["green"]
        elif(krok[wezel] == "Ozdrowaly"):
          kolory = kolory + ["blue"]
        else:
          raise Exception("cos poszlo bardzo zle")
    nx.draw_networkx(G, position, nodelist=wezly_id, node_color=kolory)
    chorzy = wynik_symulacji["chorzy"][numer]
    ozdrowiali = wynik_symulacji["ozdrowiali"][numer]
    ax.set_title(f"{nazwa}, gamma: {gamma}, beta={beta}\nnumer kroku: {numer}, chorzy: {chorzy}, ozdrowiali: {ozdrowiali}")
  print("Przygotowuje animacje")
  ani = animation.FuncAnimation(figure, rysuj_krok, kroki, interval=1000, repeat=False)
  print("Zapisuje do gify/" + plik_wyjsciowy + " skonczone")
  ani.save('gify/' + plik_wyjsciowy)
  print("Zapisywanie do gify/" + plik_wyjsciowy + " skonczone")

# Funkcja pomocnicza do generowania grafu losowego w modelu Erdosa. Nie musisz wiedzieć co ona robi.
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

# Funkcja pomocnicza do generowania grafu bezskalowego w modelu Barabasiego. Nie musisz wiedzieć co ona robi.
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

# Funkcja pomocnicza do generowania grafu typu 'mały świat' w modelu Wattsa-Strogatza. Nie musisz wiedzieć co ona robi.
def generuj_graf_Watts_Strogatz(plik_wyjsciowy="wejscie/WattsStrogatz.csv", n=100, sredni_stopien=10, polaczenia_dalekie=0.1):
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

# Funkcja pomocnicza do rysowania wykresu chorych. Nie musisz wiedzieć co ona robi.
def rysuj_wykresy_chorych(nazwa, opis):
    plik = "wyjscie/" + nazwa + "_wynik.csv"
    dane = pd.read_csv(plik, delimiter=",")
    dane_zgroupowane = dane.groupby("nr_symulacji")
    dane_zgroupowane["chorzy"].value_counts()
    plt.rcParams['font.size'] = '16'
    fig1, ax1 = plt.subplots(figsize=(8,6))
    ax1.set_title(nazwa + ": chorzy\n" + opis)
    for grupa in dane_zgroupowane.groups:
      symulacja = dane_zgroupowane.get_group(grupa)
      symulacja.plot(x="iteracje", y="chorzy", legend=False, ax=ax1, alpha=0.1, color="black")
    # df1.plot(kind="kde", ax=ax)
    ax1.set_ylabel("liczba chorych")
    plt.savefig(plik + "-chorzy.png")
    fig2, ax2 = plt.subplots(figsize=(8,6))
    ax2.set_title(nazwa + ": ozdrowiali\n" + opis)
    for grupa in dane_zgroupowane.groups:
      symulacja = dane_zgroupowane.get_group(grupa)
      symulacja.plot(x="iteracje", y="ozdrowiali", legend=False, ax=ax2, alpha=0.1, color="black")
    # df1.plot(kind="kde", ax=ax)
    ax2.set_ylabel("liczba ozdrowiałych")
    plt.savefig(plik + "-ozdrowiali.png")