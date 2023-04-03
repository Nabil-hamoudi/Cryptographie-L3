import time
# mask pour 24 bit 0xffffff
# mask pour 80 bit 0xffffffffffffffffffff

BOITE_S_DECALE =  [0xc0000000000000000000, 0x50000000000000000000, 0x60000000000000000000, 0xb0000000000000000000, 0x90000000000000000000, 0x0, 0xa0000000000000000000,
                   0xd0000000000000000000, 0x30000000000000000000, 0xe0000000000000000000, 0xf0000000000000000000, 0x80000000000000000000, 0x40000000000000000000, 
                   0x70000000000000000000, 0x10000000000000000000, 0x20000000000000000000
                   ]
BOITE_S = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
REVERSE_BOITE_S = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]


def dechiffrement_present(message_crypte, cle):
    """
    Prend en entree le message crypte et les 11 sous_cles
    issue de la cle K a partir de la fonction de
    la fonction de cadencement de cle et ressors le message
    crypte
    """
    sous_cles = sous_cles_generation(cle, BOITE_S_DECALE)
    for i in sous_cles[::-1]:
        message_crypte ^= i
        message_crypte = inverse_permutation(message_crypte)
        message_crypte = substitution(message_crypte, REVERSE_BOITE_S)

    return message_crypte


def chiffrement_present(message, cle):
    """
    Prend en entree le message et la cle de cryptage
    issue de la cle K a partir de la fonction de
    la fonction de cadencement de cle et ressors le message
    crypte
    """
    for i in sous_cles_generation(cle, BOITE_S_DECALE):
        message = substitution(message, BOITE_S)
        message = permutation(message)
        message ^= i

    # ici le message retournee est le message crypté
    return message


def sous_cles_generation(cle, boite_s):
    """
    genere une liste des sous cle
    """
    cle <<= 56
    sous_cles = []
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        # 1er etape
        cle = (cle << 61) & 0xffffffffffffffffffff | cle >> 19
        # 2eme etape
        cle = boite_s[cle >> 76] + (cle & 0xfffffffffffffffffff)
        # 3eme etape
        cle ^= i << 15
        sous_cles.append((cle >> 16) & 0xffffff)
    return sous_cles


def substitution(entree, liste_substitution):
    """
    prend en entree le message en chiffrage
    et ressors la substitution en fonction
    de la constante BOITE_S
    """
    sortie = 0
    for i in [0, 4, 8, 12, 16, 20]:
        #les 4 derniers bits sont passés à sbox puis sont insérés à la sortie
        sortie += liste_substitution[entree & 0xf] << i
        entree = entree >> 4
    return sortie


def inverse_permutation(value):
    value = permutation_step(value, 0x00540540, 1)
    value = permutation_step(value, 0x00333000, 2)
    value = permutation_step(value, 0x00000c30, 16)
    value = permutation_step(value, 0x0409050a, 4)
    value = permutation_step(value, 0x00480084, 8)
    value = permutation_step(value, 0x00004812, 16)
    value = permutation_step(value, 0x00122112, 2)
    value = permutation_step(value, 0x00505050, 1)
    return value

def permutation(value):
    value = permutation_step(value, 0x00001100, 16)
    value = permutation_step(value, 0x000c080c, 4)
    value = permutation_step(value, 0x00220022, 2)
    value = permutation_step(value, 0x10144114, 1)
    value = permutation_step(value, 0x21121212, 2)
    value = permutation_step(value, 0x08090606, 4)
    value = permutation_step(value, 0x000c0030, 8)
    value = permutation_step(value, 0x00000c3c, 16)
    return value


def permutation_step(value, mask, shift):
    result = ((value >> shift) ^ value) & mask
    return (value ^ result) ^ (result << shift)


def testtest():
    start = time.time()
    for i in range(1<<21):
        chiffrement_present(i, i)
        dechiffrement_present(i, i)
    print(time.time()-start)

#testtest()


#print(format(chiffrement_present(int("f955b9", 16), int("d1bd2d", 16)), 'x'))
#print(format(dechiffrement_present(int("47a929", 16), int("d1bd2d", 16)), 'x'))
