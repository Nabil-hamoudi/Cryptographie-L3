from chiffrement_dechifrement import chiffrement_present, dechiffrement_present

m1, c1 = int("36ca6c", 16), int("0ded87", 16)
m2, c2 = int("a92a08", 16), int("d68fb5", 16)


def attaque_milieu(m1, c1, m2, c2):
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
    present24_atta_liste_m = []
    present24_atta_liste_c = []
    for i in range(2**24):
        present24_atta_liste_m.append((chiffrement_present(m, i), i))
        present24_atta_liste_c.append((dechiffrement_present(c, i), i))

    print("check, creation 2 premiere table")
    return tri_cle(present24_atta_liste_m, present24_atta_liste_c)


def tri_cle(m_crypt, c_decrypt):
    result = []
    m_crypt = sorted(m_crypt)
    c_decrypt = sorted(c_decrypt)
    for i in range(2**24):
        if m_crypt[i][0] == c_decrypt[i][0]:
            result.append((m_crypt[i][1], c_decrypt[i][1]))
    return result


for i, j in attaque_milieu(m1, c1, m2, c2):
    print("k1 = " + format(i, 'x') + ", " + "k2 = " + format(j, 'x'))
