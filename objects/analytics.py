import itertools
import networkx as nx


def extract_words(p1: str, p2: str) -> tuple[str, str]:
        w1 = p1[1:] if p1 != 'I' else ''
        w2 = p2[1:] if p2 != 'I' else ''
        return w1, w2

def is_mirrored(p1: tuple[str, str], p2: tuple[str, str]) -> bool:
    """
    Checks if on pair originates from the other pair beeing mirrored.
    """
    w1, w2 = p1
    v1, v2 = p2
    w = sorted([w1, w2])
    v = sorted([v1, v2])

    # check if it is even possible
    # ratio needs to match, it cant be that both words are the same length
    if len(w1) - len(w2) == len(v1) - len(v2):
        if w[1] > v[1]:
            if w[0] > v[0]:

                # If this runs through v[1] is a prefix of w[1]
                for i in range(len(v[1])):
                    if w[1][i] != v[1][i]:
                        return False

                suffix = w[1][len(v[1]):]

                # If this runs through v[1] is a prefix of w[1]
                for i in range(len(v[0])):
                    if w[0][i] != v[0][i]:
                        return False

                if suffix == w[0][len(v[0]):]:
                    return True
                return False
                
            else: return False

        if v[1] > w[1]:
            if v[0] > w[0]:
                # If this runs through v[1] is a prefix of w[1]
                for i in range(len(w[1])):
                    if v[1][i] != w[1][i]:
                        return False

                suffix = v[1][len(w[1]):]

                # If this runs through v[1] is a prefix of w[1]
                for i in range(len(w[0])):
                    if v[0][i] != w[0][i]:
                        return False

                if suffix == v[0][len(w[0]):]:
                    return True
                return False
            else: return False

        # some have equal distance
        return False

        
    else:
        return False
    


def check_pattern_between_pairs(p1: tuple[str, str], p2: tuple[str, str]) -> str | None:
    """
    Prüft, ob p2 durch Muster A, B oder C aus p1 erklärt werden kann
    ODER umgekehrt.
    """
    w1, w2 = p1
    v1, v2 = p2

    # Muster A (Präfix/Suffix): p2 aus p1 ODER p1 aus p2
    if is_mirrored(p1, p2) or is_mirrored(p2, p1):
        return 'A'

    # Muster B (Inversen-Symmetrie)
    w1_rev, w2_rev = w1[::-1], w2[::-1]
    if (v1 == w1_rev and v2 == w2_rev) or (v1 == w2_rev and v2 == w1_rev):
        return 'B'

    # Muster C (Relativ-Verschiebung)
    rel1 = tuple(sorted(['', w1[::-1] + w2]))
    rel2 = tuple(sorted(['', v1[::-1] + v2]))
    if rel1 == rel2 and rel1 != ('', ''):
        return 'C'

    return ""


def split_dictionary_with_flags(data: dict):

    # initialize the output dicts.
    dict_A = {}
    dict_B = {}
    dict_C = {}
    dict_Rest = {}

    # go through the data
    for dist, pairs in data.items():
        # if there is only one pair with this distance dont bother.
        # either due to geometry or due to not having high enough order of reflection
        if len(pairs) <= 1:
            dict_Rest[dist] = pairs
            continue

        
        # word_pairs = [(p1, p2) for p1, p2 in pairs]
        amount_pairs = len(pairs)
        flags = [""] * amount_pairs

        # 1. Jedes Paar mit jedem vergleichen
        for i in range(amount_pairs):
            for j in range(amount_pairs):

                # Dont need to compare to itself
                if i == j:
                    continue

                # check for each combination, if the get a pattern, so pattern is not None
                pattern = check_pattern_between_pairs(pairs[i], pairs[j])


                flags[i] += pattern
                flags[j] += pattern

        filtered_flags = []
        # Prepair flags
        for e in flags:
            new = "".join(dict.fromkeys(e))
            filtered_flags.append(new)


        # 2. Aufteilung anhand der Flags
        list_A, list_B, list_C, list_Rest = [], [], [], []


        for idx, flag in enumerate(filtered_flags):
            pair = pairs[idx]
            if flag == "":
                list_Rest.append(pair)
            else:
                for s in flag:
                    if s == 'A':
                        list_A.append(pair)
                    elif s == 'B':
                        list_B.append(pair)
                    elif s == 'C':
                        list_C.append(pair)
                                

        if list_A: dict_A[dist] = list_A
        if list_B: dict_B[dist] = list_B
        if list_C: dict_C[dist] = list_C
        if list_Rest: dict_Rest[dist] = list_Rest

    return dict_A, dict_B, dict_C, dict_Rest



# Wir gehen davon aus, dass deine Funktionen extract_words und 
# check_pattern_between_pairs hier verfügbar sind.

def analyze_distance_row(pairs_in_row: list[tuple[str, str]]):
    """
    Wandelt eine Liste von Punktpaaren (gleicher Abstand) in einen Graphen um
    und findet zusammenhängende Muster-Gruppen sowie isolierte Reste.
    """
    G = nx.Graph()
    
    # 1. Alle Knoten hinzufügen
    # Da Tupel aus Strings in Python hashbar sind, können sie direkt als Knoten dienen.
    G.add_nodes_from(pairs_in_row)
    
    # 2. Kanten ziehen (Jedes Paar mit jedem exakt einmal vergleichen)
    # itertools.combinations verhindert redundante Vergleiche (i mit j und j mit i)
    for p1, p2 in itertools.combinations(pairs_in_row, 2):
        
        # Wörter extrahieren (deine Hilfsfunktion)
        w1_tuple = extract_words(*p1)
        w2_tuple = extract_words(*p2)
        
        # Muster prüfen
        pattern = check_pattern_between_pairs(w1_tuple, w2_tuple)
        
        if pattern:
            # Kante hinzufügen und das gefundene Muster als Attribut speichern
            G.add_edge(p1, p2, pattern=pattern)
            
    # 3. Zusammenhangskomponenten extrahieren
    # Gibt eine Liste von Sets zurück. Jedes Set ist eine "Insel" im Graphen.
    components = list(nx.connected_components(G))
    
    return G, components

# --- Beispielhafte Auswertung ---

def evaluate_components(components):
    haupt_gruppen = []
    rest_gruppen = []
    isolierte_paare = []
    
    # Sortieren nach Größe (größte Gruppe zuerst), um die "Hauptgruppe" zu finden
    components_sorted = sorted(components, key=len, reverse=True)
    
    for i, comp in enumerate(components_sorted):
        if len(comp) > 2 and i == 0:
            # Die größte Gruppe ist meist das Fundament bekannter Muster
            haupt_gruppen.append(comp)
        elif len(comp) > 1:
            # Eine eigene kleine Insel (z.B. 2 Paare), die aber nicht zur Hauptgruppe gehört!
            # HOCHINTERESSANT: Hier könnte sich ein neues Muster (Muster D) verbergen,
            # das diese kleine Gruppe in sich selbst verbindet.
            rest_gruppen.append(comp)
        else:
            # Völlig isolierte Knoten (Größe 1)
            # Das sind geometrische Zufälle oder völlig neue Phänomene
            isolierte_paare.append(comp.pop())
            
    return haupt_gruppen, rest_gruppen, isolierte_paare
