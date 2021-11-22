


L'évaluateur :
Il s'agit de regarder le PER (POS Error Rate) entre la phrase transcrite et la phrase de référence.

- En fait, il ne s'agit pas uniquement de faire ça mais aussi de calculer le nombre d'erreur
qu'il y a par POS : (càd WER_adj = (S_adj + I_adj + D_adj) / Nbr_adj
Et il faut tenir compte des <eps> qui peuvent se situer à n'importe quel endroit de la phrase.



J'ai supprimé quelques lignes du fichier wer_test.txt qui pose problème à cause d'un caractère bugué


Pré-requis:
 - Flair (pip install flair)
 - jiwer (pip install jiwer)
