def shredded(w: str) -> str:
    """
    Takes a string, representing a reflection history and performs all the cancellation.
    So if the same mirror is there back to back, then remove both, because it doesnt change
    the image point.
    """
    if w == "": return w

    while True:
        flag = True
        prev = ""
        for i, c in enumerate(w):
            # same mirror back to back
            if prev == c:
                # remove the mirrors
                w = w[:i-1] + w[i+1:]
                # can't end the loop here, because new cancelation could have been created.
                flag = False
                break
            prev = c

        # if we went through the string and no cancellation appeared, then we can return the string.
        if flag:
            break
    return w

# ----------------------------------------------------------------------------

def matchings(p1: tuple[str, str], p2: tuple[str, str]) -> bool:
    """
    Checks whether p1 is reducable to p2 with some mirror sequence s.
    """
    Iw1, Iw2 = p1
    Iv1, Iv2 = p2

    # remove the I
    w1 = Iw1[1:]
    w2 = Iw2[1:]
    v1 = Iv1[1:]
    v2 = Iv2[1:]

    # created the two possible mirror sequences with inversing w1, so we have
    # w1 + w1^-1, then adds either v1 or v2, so the entire result is v1 or v2
    s1 = w1[::-1] + v1
    s2 = w1[::-1] + v2

    # checks if this sequence also works for w2
    # if anyone does, these are equal distance point pairs, if none does, then tey are not.
    if shredded(w2 + s1) == v2:
        return True

    if shredded(w2 + s2) == v1:
        return True

    return False

# ----------------------------------------------------------------------------

def split_dictionary_with_flags(data: dict):
    """
    Works entirely on filtered data. So demands a structure:
    {
    distance (float) : list of pairs with key's distance (list(tuple(string, string)))
    }

    Also wants the data to have filtered out all the length one lists, because they can't have
    any group.
    """

    # alphabet for labeling in a group of 10 < size < 37
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    # Output initialisation
    clear = {}
    rest = {}
    logs = {}

    # go through the data
    for key, value in data.items():

        # make an empty flag entry for each point pair in the iteration.
        flags = [""] * len(value)

        # compare each point paire with each other:
        for i in range(len(value)): 
            for j in range(len(value)):

                if i == j: continue

                # boolean, if they are reducable to each other, through some reflection sequence s
                matches = matchings(value[i], value[j])

                # add label, so we later now, that these two are in a group
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

        # format the falgs, filter out the doubles.
        ff = []
        for flag in flags:
            ff.append("".join(dict.fromkeys(flag)))

        # split all the grouped once with those who are groupless:
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
    