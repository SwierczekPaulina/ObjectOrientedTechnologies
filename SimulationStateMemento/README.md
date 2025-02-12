# i - liczba osobników
# [0, 2.5] przedział prędkości (m/s)
# przestrzeń [(0,0), (0,m), (n,0), (n,m)] w metrach
# Koniec symulacji -> Wszyscy zakażeni LUB wszyscy odporni
# Każda sekunda symulacji to 25 iteracji

# Początkowa populacja:
# Osobnicy są losowo odporni na zakażenie LUB wrażliwi na zakażenie

# Warunki:
# Przekroczenie granicy -> 50% powrót z odwrotnym wektorem
#                       -> 50% opuszczenie obszaru
# Musimy zliczać ile osobników opóściło obszar, i wtedy odejmujemy
# z tej liczby 1 za każdym razem gdy 1 nowy wkracza w losowych punktach.
# (tworzenie nowego osobnika) z 10% szans bycia zakażonym -> [Posiada objawy lub nie!]
# Czyli nowy osobnik ma nowe cechy (osobnicy którzy opuścili obszar są usuwani 'del')

# def __init__(self, ..., p_zakazenia=0)
# Jeżeli jest zakażony (ten z 10% szans bycia zakażonym) to zawsze będzie
# wrażliwy na zakażenie!

# Zakażenie:
# Na koniec jednego cyklu (jedna iteracja) symulacji
# sprawdzamy którzy osobnicy mają w odległości <= 2m osobnika
# zakażonego jeśli mijają 3 cykle symulacji to jeżeli osobnik ma w otoczeniu
# osobnika z objawami to staje się zakażony
# Jeśli ma w otoczeniu osobnika bez objawów, to 1/2 szanse zakażenia przy każdej iteracji
# Jeśli ma w otoczeniu więcej niż jednego osobnika bez objawów, to kumulujemy P
# np. 2? -> 1/2 * 1/2 = 1/4 -> P = 1 - 1/4 -> 75%
# Jeśli osobnik będzie dalej zdrowy, to losujemy przy każdej iteracji od nowa.


# Stany:
# OZ    WZ
# ZD    ZD
#           ZA
#               PO
#               NPO

# OZ
# WZ : ZD ^ ZA

# ZD -> ZA -> PO  -> ZD (przy czym staje się odporny na zakażenie OZ)
# ZD -> ZA -> NPO -> ZD (przy czym staje się odporny na zakażenie OZ)



# Wzorzec FACTORY create_poczatkowy() - create_wkraczajacy()
