import time

# afin de gagner des performance on passe les chaine hexadecimale en int en base decimal
# pour eviter de perdre des performances
BOITE_S = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
REVERSE_BOITE_S = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]
TABLE_PERMUTATION = [0, 6, 12, 18, 1, 7, 13, 19, 2, 8, 14, 20, 3, 9, 15, 21, 4, 10, 16, 22, 5, 11, 17, 23]
REVERSE_TABLE_PERMUTATION = [0, 4, 8, 12, 16, 20, 1, 5, 9, 13, 17, 21, 2, 6, 10, 14, 18, 22, 3, 7, 11, 15, 19, 23]
TOURS = 10
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
    resultat = 0
    for i in range(20, -1, -4):
        resultat <<= 4
        slic = message >> i
        message ^= slic << i
        resultat |= boite_s[slic]

    return resultat


def permutation(message, table_permutation):
    """
    prend en entree le message en chiffrage
    et ressors la permutation en fonction
    de la constante TABLE_PERMUTATION
    """
    result = 0
#    while 0 < message.bit_length():
#        result |= (message & 1) << table_permutation[message.bit_length()]
#        message >>= 1

    for i in range(message.bit_length()):
        result |= ((message >> i) & 1) << table_permutation[i]
    return result


def testtest():
    start = time.time()
    for _ in range(10):
        for i in range(1<<24):
            substitution(i, TABLE_PERMUTATION)
    print(time.time()-start)

#testtest()

print(format(chiffrement_present(int("f955b9", 16), int("d1bd2d", 16)), 'x'))
print(format(dechiffrement_present(int("47a929", 16), int("d1bd2d", 16)), 'x'))