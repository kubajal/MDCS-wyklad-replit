# Teoria grafów w walce z epidemią koronawirusa

Spis treści:

 - Kody źródłowe:
   - `funkcje.py`: wszystkie funkcje do generowania grafów, symulacji rozchodzenia się epidemii na wygenerowanych grafach, rysowania grafów i rysowania wykresów itp.
   - `losowa_vs_bezskalowa.py`: porównanie sieci losowej (tzw. _model Erdos'a_) i bezskalowej (tzw. _model Barabasi'ego_) - 100 symulacji dla sieci o 1000 wierzchołkach i 10 chorych osobach na początek
   - `male_swiaty.py`: porównanie 3 sieci typu 'mały świat' (tzw. _model Watts'a-Strogatz'a_) - 100 symulacji dla sieci o 1000 wierzcholkow i 10 chorych osobach na początek:
      - z 10% dalekich połączeń
     - z 1% dalekich połączeń
      - z 0% dalekich połączeń
   - `stworz_gify.py` - rysowanie GIFow z symulacjami dla sieci losowej i bezskalowej
 - foldery z plikami wejściowymi i wyjściowymi dla symulacji:
   - `wejscie/` - pliki CSV z listami krawędzi grafów generowane przez `generuj_grafy.py`:
      - graf bezskalowy (`barabasi_100.csv` i `barabasi_40.csv`)
      - graf losowy (`erdos_100.csv` i `erdos_40.csv`)
      - 'małe światy' (`WattsStrogatz_full_lockdown.csv`, `WattsStrogatz_half_lockdown.csv`, `WattsStrogatz_no_lockdown.csv`, `WattsStrogatz_lockdown.csv`)
      - pliki .png: _histogramy rozkładów stopni wierzchołków_ dla każdego generowanego grafu (nie musisz wiedzieć co to) 
   - `wyjscie/` - pliki generowane przez `losowa_vs_bezskalowa.py` i `male_swiaty.py`
      - wyniki symulacji (pliki .csv)
      - wykresy liczby chorych i ozdrowiałych (pliki .png)
   - `gify/` - folder z plikami GIF po symulacjach rozchodzenia się epidemii po grafie 