from optimisation3_mise_en_commun import chiffrement_present, dechiffrement_present
import time

m1, c1 = int("36ca6c", 16), int("0ded87", 16)
m2, c2 = int("a92a08", 16), int("d68fb5", 16)


def attaque_milieu(m1, c1, m2, c2):
    """
    initialise l'attaque par milieu
    dans un premier temp cherche les cles
    candidate entre le message clair m1
    et crypte c1 et ensuite compare
    k1 et k2 cle sur m2 et c2 pour ressortir
    la ou les possible bonnes cle
    """
    cle1 = cle_candidate(m1, c1)
    print(cle1[:25])
    print("check, cle candidate")
    result = []
    for i, j in cle1:
        present24_atta_m = chiffrement_present(m2, i)
        present24_atta_c = dechiffrement_present(c2, j)
        if present24_atta_m == present24_atta_c:
            result.append((i, j))
    return result


def cle_candidate(m, c):
    """
    cherche les cle candidate entre un message
    clair m et un crypte c et ensuite les compare
    pour les trouver via la fonction tri_cle et
    ressors la liste de couple k1 et k2 de cle
    """
    present24_atta_liste_m = []
    present24_atta_liste_c = []
    for i in range(2**24):
        present24_atta_liste_m.append((chiffrement_present(m, i), i))
        present24_atta_liste_c.append((dechiffrement_present(c, i), i))

    print("check, creation 2 premiere table")
    return tri_cle(present24_atta_liste_m, present24_atta_liste_c)


def tri_cle(m_crypt, c_decrypt):
    """
    prend en entrer 2 liste de tuple
    (message, cle) les tri puis les compare
    pour ressortir les couple k1 et k2 cle
    possible
    """
    result = []
    m_crypt = sorted(m_crypt)
    c_decrypt = sorted(c_decrypt)
    for i in range(2**24):
        if m_crypt[i][0] == c_decrypt[i][0]:
            result.append((m_crypt[i][1], c_decrypt[i][1]))
    return result

def testtest():
    start = time.time()
    for i, j in attaque_milieu(m1, c1, m2, c2):
        print("k1 = " + format(i, 'x') + ", " + "k2 = " + format(j, 'x'))
    print(time.time()-start)

testtest()

