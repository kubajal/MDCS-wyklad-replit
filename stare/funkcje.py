import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
import matplotlib.animation as animation
from networkx import exception

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
  
def animuj(graf, kroki):
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
        if(krok[wezel] == Status.Chory):
          kolory = kolory + ["red"]
        elif(krok[wezel] == Status.Zdrowy):
          kolory = kolory + ["green"]
        elif(krok[wezel] == Status.Ozdrowialy):
          kolory = kolory + ["blue"]
        else:
          raise Exception("cos poszlo bardzo zle")
    ax.set_title(f"numer kroku: {numer}\n")
    nx.draw_networkx(G, position, nodelist=wezly_id, node_color=kolory)
    # plt.show()
  
  print("Rysuje animacje")
  # for krok in kroki:
  #   rysuj_krok(krok)
  ani = animation.FuncAnimation(figure, rysuj_krok, kroki, repeat=False)
  ani.save('./symulacja.gif', writer='imagemagick')
  #plt.show()