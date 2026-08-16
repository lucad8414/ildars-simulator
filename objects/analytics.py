def shredded(w: str) -> str:
    """
    """
    if w == "": return w

    while True:
        flag = True
        prev = ""
        for i, c in enumerate(w):
            if prev == c:
                w = w[:i-1] + w[i+1:]
                flag = False
                break
            prev = c

        if flag:
            break
    return w


def matchings(p1: tuple[str, str], p2: tuple[str, str]) -> bool:
    """
    Erkennt, ob p2 aus p1 durch Anfügen derselben Wand an beide Pfade entsteht.
    Bsp: p1 = ('', '1') und p2 = ('2', '12') -> beide wurden rechts um '2' erweitert (oder links).
    """
    Iw1, Iw2 = p1
    Iv1, Iv2 = p2
    
    w1 = Iw1[1:]
    w2 = Iw2[1:]
    v1 = Iv1[1:]
    v2 = Iv2[1:]

    s1 = w1[::-1] + v1
    s2 = w1[::-1] + v2

    if shredded(w2 + s1) == v2:
        return True

    if shredded(w2 + s2) == v1:
        return True

    return False


def split_dictionary_with_flags(data: dict):

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    clear = {}
    rest = {}
    logs = {}

    for key, value in data.items():

        flags = [""] * len(value)

        for i in range(len(value)):
            for j in range(len(value)):

                if i == j: continue

                matches = matchings(value[i], value[j])

                if matches:
                    append_for_i = ""
                    append_for_j = ""
                    if j > 9:
                        append_for_i = alphabet[j-10]
                    else:
                        append_for_i = str(j)

                    if i > 9:
                        append_for_j = alphabet[i-10]
                    else:
                        append_for_j = str(i)

                    flags[i] += append_for_i
                    flags[j] += append_for_j

        clear[key] = []
        rest[key] = []

        ff = []
        for flag in flags:
            ff.append("".join(dict.fromkeys(flag)))

        logs[key] = ff
        for ind, flag in enumerate(flags):
            if flag != "":
                clear[key].append(value[ind])
            else:
                rest[key].append(value[ind])

    
    return clear, rest, logs


if __name__ == "__main__":
    test = [('I2', 'I32121'), ('I32312', 'I1')]
    for i in range(len(test)):
        for j in range(len(test)):
            if i == j: continue
            print(test[i],test[j], matchings(test[i],test[j]))
    