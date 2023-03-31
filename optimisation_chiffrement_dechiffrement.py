# afin de gagner des performance on passe les chaine hexadecimale en int en base decimal
# pour eviter de perdre des performances
BOITE_S = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
REVERSE_BOITE_S = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]
TABLE_PERMUTATION = [23, 17, 11, 5, 22, 16, 10, 4, 21, 15, 9, 3, 20, 14, 8, 2, 19, 13, 7, 1, 18, 12, 6, 0]
REVERSE_TABLE_PERMUTATION = [23, 19, 15, 11, 7, 3, 22, 18, 14, 10, 6, 2, 21, 17, 13, 9, 5, 1, 20, 16, 12, 8, 4, 0]
TOURS = 10

def init_sous_cle_cadencement(cle):
    """
    Prend une cle de 24 bit en entree
    et initialise la premiere sous cle a
    partir de la cle maitre
    """
    cle = format(cle, 'b')
    cle = ('0' * (24 - len(cle))) + cle + (56 * '0')
    return int(cle[40:64], 2), cle


def sous_cles_suivante(cle, nombre_tour, boite_s):
    """
    fait un nouveau tour de cle
    """
    # 1er etape
    cle = cle[61:] + cle[:61]
    # 2eme etape
    substi = boite_s[int(cle[:4], 2)]
    substi = format(substi, 'b')
    cle = ('0' * (4 - len(substi))) + substi + cle[4:]
    # 3eme etape
    xor_number = format(int(cle[60:65], 2) ^ nombre_tour, 'b')
    xor_number = ('0' * (5 - len(xor_number))) + xor_number
    cle = cle[:60] + xor_number + cle[65:]
    return int(cle[40:64], 2), cle


def chiffrement_present(message, cle):
    """
    Prend en entree le message et la cle de cryptage
    issue de la cle K a partir de la fonction de
    la fonction de cadencement de cle et ressors le message
    crypte
    """
    sous_cle, cle = init_sous_cle_cadencement(cle)
    for i in range(1, TOURS+1):
        message ^= sous_cle
        message = substitution(message, BOITE_S)
        message = permutation(message, TABLE_PERMUTATION)
        sous_cle, cle = sous_cles_suivante(cle, i, BOITE_S)
    message ^= sous_cle

    # ici le message retournee est le message crypté
    return message


def dechiffrement_present(message_crypte, cle):
    """
    Prend en entree le message crypte et les 11 sous_cles
    issue de la cle K a partir de la fonction de
    la fonction de cadencement de cle et ressors le message
    crypte
    """
    sous_cles = [0 for _ in range(0, TOURS+1)]
    sous_cles[0], cle = init_sous_cle_cadencement(cle)

    for i in range(1, TOURS+1):
        sous_cles[i], cle = sous_cles_suivante(cle, i, BOITE_S)

    message_crypte ^= sous_cles.pop(-1)
    for _ in range(TOURS):
        message_crypte = permutation(message_crypte, REVERSE_TABLE_PERMUTATION)
        message_crypte = substitution(message_crypte, REVERSE_BOITE_S)
        message_crypte ^= sous_cles.pop(-1)

    return message_crypte


def substitution(message, boite_s):
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
        message += boite_s[int(i, 16)]
    return message


def permutation(message, table_permutation):
    """
    prend en entree le message en chiffrage
    et ressors la permutation en fonction
    de la constante TABLE_PERMUTATION
    """
    result = 0
    bina = format(message, 'b')
    for i, j in enumerate(bina[::-1]):
        result += (2**table_permutation[i]) * int(j)
    return result

print(format(chiffrement_present(int("f955b9", 16), int("d1bd2d", 16)), 'x'))
print(format(dechiffrement_present(int("47a929", 16), int("d1bd2d", 16)), 'x'))