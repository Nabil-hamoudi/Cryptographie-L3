# afin de gagner des performance on passe les chaine hexadecimale en int en base decimal
# pour eviter de perdre des performances
BOITE_S = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
TABLE_PERMUTATION = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17, 23]
TOURS = 10


def init_sous_cle_cadencement(cle):
    """
    Prend une cle de 24 bit en entree
    et initialise la premiere sous cle a
    partir de la cle maitre
    """
    cle = format(cle, 'b')
    cle = ('0' * (24 - len(cle))) + cle + (56 * '0')
    print(format(int(cle, 2), 'x'))
    return int(cle[40:64], 2), cle


def sous_cles_suivante(cle, nombre_tour):
    """
    fait un nouveau tour de cle
    """
    # 1er etape
    cle = cle[61:] + cle[:61]
    print(format(int(cle, 2), 'x'))
    # 2eme etape
    substi = BOITE_S[int(cle[:4], 2)]
    substi = format(substi, 'b')
    cle = ('0' * (4 - len(substi))) + substi + cle[4:]
    print(format(int(cle, 2), 'x'))
    # 3eme etape
    xor_number = format(int(cle[60:65], 2) ^ nombre_tour, 'b')
    xor_number = ('0' * (5 - len(xor_number))) + xor_number
    cle = cle[:60] + xor_number + cle[65:]
    print(format(int(cle, 2), 'x'))
    return int(cle[40:64], 2), cle


def chiffrement_present(message, cle):
    """
    Prend en entree le message et les 11 sous_cles
    issue de la cle K a partir de la fonction de
    la fonction de cadencement de cle et ressors le message
    crypte
    """
    sous_cle, cle = init_sous_cle_cadencement(cle)
    for i in range(1, TOURS+1):
        print("")
        sous_cle, cle = sous_cles_suivante(cle, i)
#        print(format(message, 'x'), format(sous_cle, 'x'))
        message ^= sous_cle
        message = substitution(message)
        message = permutation(message)
    sous_cle, cle = sous_cles_suivante(cle, TOURS+1)
#    print(format(message, 'x'), format(sous_cle, 'x'))
    message ^= sous_cle

    # ici le message retournee est le message crypté
    return message


def substitution(message):
    """
    prend en entree le message en chiffrage
    et ressors la substitution en fonction
    de la constante BOITE_S
    """
    hexa = format(message, "x")
    hexa = ('0' * (6 - len(hexa))) + hexa
    message = 0
    for i in hexa:
        message *= 16
        message += BOITE_S[int(i, 16)]
    return message


def permutation(message):
    """
    prend en entree le message en chiffrage
    et ressors la permutation en fonction
    de la constante TABLE_PERMUTATION
    """
    bina = format(message, 'b')
    bina = '0' * (24 - len(bina)) + bina
    message = ["" for _ in range(24)]
    for i in range(24):
        message[TABLE_PERMUTATION[i]] = bina[i]
    result = ""
    for i in message:
        result += i
    return int(result, 2)


print(format(chiffrement_present(0000, 0000), 'x'))
