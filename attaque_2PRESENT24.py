from chiffrement_dechifrement import chiffrement_present, dechiffrement_present

m1, c1 = int("36ca6c", 16), int("0ded87", 16)
m2, c2 = int("36ca6c", 16), int("0ded87", 16)


def attaque_milieu(m1, c1, m2, c2):
    cle1 = cle_candidate(m1, c1)
    print("check, premiere attaque fini")
    cle2 = cle_candidate(m2, c2)
    return tri_cle(cle1, cle2)


def cle_candidate(m, c):
    present24_atta_m = {}
    present24_atta_c = {}
    for i in range(2**24):
        present24_atta_c[chiffrement_present(m, i)] = i
        present24_atta_c[dechiffrement_present(c, i)] = i
    print("check, creation 2 premierre table")
    return [(present24_atta_m[i], present24_atta_c[j]) for i, j in tri_cle(present24_atta_m.keys(), present24_atta_c.keys)]


def tri_cle(m_crypt, c_decrypt):
    result = []
    for i, j in (m_crypt.sort(), c_decrypt.sort()):
        if i == j:
            result.append((i, j))
    return result


for i, j in attaque_milieu(m1, c1, m2, c2):
    print("k1 = " + format(i, 'x') + ", " + "k2 = " + format(j, 'x'))
