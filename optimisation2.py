import time
# mask pour 24 bit 0xffffff
# mask pour 80 bit 0xffffffffffffffffffff

BOITE_S_DECALE =  [0xc0000000000000000000, 0x50000000000000000000, 0x60000000000000000000, 0xb0000000000000000000, 0x90000000000000000000, 0x0, 0xa0000000000000000000,
                   0xd0000000000000000000, 0x30000000000000000000, 0xe0000000000000000000, 0xf0000000000000000000, 0x80000000000000000000, 0x40000000000000000000, 
                   0x70000000000000000000, 0x10000000000000000000, 0x20000000000000000000
                   ]
REVERSE_BOITE_S_DECALE = [0x50000000000000000000, 0xe0000000000000000000, 0xf0000000000000000000, 0x80000000000000000000, 0xc0000000000000000000, 0x10000000000000000000,
                          0x20000000000000000000, 0xd0000000000000000000, 0xb0000000000000000000, 0x40000000000000000000, 0x60000000000000000000, 0x30000000000000000000, 0x0, 
                          0x70000000000000000000, 0x90000000000000000000, 0xa0000000000000000000
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
    sous_cles = [0 for _ in range(0, 11)]
    sous_cles[0], cle = 0, cle << 56

    for i in range(1, 11):
        sous_cles[i], cle = sous_cles_suivante(cle, i, BOITE_S_DECALE)

    message_crypte ^= sous_cles.pop(-1)
    for _ in range(10):
        message_crypte = inverse_permutation(message_crypte)
        message_crypte = substitution(message_crypte, REVERSE_BOITE_S)
        message_crypte ^= sous_cles.pop(-1)

    return message_crypte


def chiffrement_present(message, cle):
    """
    Prend en entree le message et la cle de cryptage
    issue de la cle K a partir de la fonction de
    la fonction de cadencement de cle et ressors le message
    crypte
    """
    sous_cle, cle = 0, cle << 56
    for i in range(1, 11):
        message ^= sous_cle
        message = substitution(message, BOITE_S)
        message = permutation(message)
        sous_cle, cle = sous_cles_suivante(cle, i, BOITE_S_DECALE)
    message ^= sous_cle

    # ici le message retournee est le message crypté
    return message



def sous_cles_suivante(cle, nombre_tour, boite_s):
    """
    fait un nouveau tour de cle
    """
    # 1er etape
    cle = Rotation_Gauche(cle, 61, 80)
    # 2eme etape
    cle = BOITE_S_DECALE[cle >> 76] | (cle & 0xfffffffffffffffffff)
    # 3eme etape
    cle ^= nombre_tour << 15
    return (cle >> 16) & 0xffffff, cle



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


def Rotation_Gauche(nombre, decalage, taille):
    mask_taille_limite = (1 << taille) - 1
    return ((nombre << decalage) & mask_taille_limite) | (nombre >> (taille - decalage))


def testtest():
    start = time.time()
    for _ in range(2):
        for _ in range(10):
            for i in range(1<<24):
                chiffrement_present(0, i)
                dechiffrement_present(0, i)
    print(time.time()-start)

testtest()


#print(format(chiffrement_present(int("f955b9", 16), int("d1bd2d", 16)), 'x'))
#print(format(dechiffrement_present(int("47a929", 16), int("d1bd2d", 16)), 'x'))
