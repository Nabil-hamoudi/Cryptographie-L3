from sys import argv
from optimisation3_mise_en_commun import *
import time


#Génère les listes Lm et Lc à partir d'un couple clair chiffré
#Les listes ont pour indice le message ou le chiffré
#Les listes ont pour valeur une liste de clés qui génère ce message ou chiffré
def generation_listes(clair,chiffre):
    start = time.time()
    lm, lc = [[] for x in range(1<<24)], [[] for x in range(1<<24)]
    print("Listes Lm et Lc allouees en "+"%.2f" % (time.time()-start)+"s, generation des listes ...")
    start = time.time()
    for cle in range(1<<24):
        sous_cles = sous_cles_generation(cle, BOITE_S_DECALE)
    
        for i in sous_cles:
            clair = substitution(clair, BOITE_S)
            clair = permutation(clair)
            clair ^= i
        lm[clair].append(cle)
    
        for i in sous_cles[::-1]:
            chiffre ^= i
            chiffre = inverse_permutation(chiffre)
            chiffre = substitution(chiffre, REVERSE_BOITE_S)
        lc[chiffre].append(cle)

    print("Listes generees en "+"%.2f" % (time.time()-start)+"s")
    return [lm,lc]

def trouver_collision(lmlc):
	collisions = []
	for i in range(1<<24):
		if (lmlc[0][i] !=[]) and (lmlc[1][i] != []) :
			collisions.append((lmlc[0][i],lmlc[1][i]))
	return collisions


def tests_cle(clair2, chiffre2, collisions):
	print("Tests des cles sur le second couple")
	start = time.time()
	resultats = []
	for couple in collisions:
		for k1 in couple[0]:
			for k2 in couple[1]:
					if chiffrement_present(chiffrement_present(clair2,k1),k2) == chiffre2:
						resultats.append([k1,k2])
						#print(str(hex(k1))+" "+str(hex(k2)))
	print("Tests effectues en "+"%.2f" % (time.time()-start)+"s")
	return resultats

def attaque(couple1, couple2):
	collisions = trouver_collision(generation_listes(couple1[0],couple1[1]))
	return tests_cle(couple2[0], couple2[1], collisions)



########## CLI #########
if (len(argv)>5) and (argv[1] == "attaque"):
	couple1 = [int(argv[2], 16), int(argv[3], 16)]
	couple2 = [int(argv[4], 16), int(argv[5], 16)]
	cles = attaque(couple1, couple2)
	for couple in cles:
		print(str(hex(couple[0]))+" "+str(hex(couple[1])))

