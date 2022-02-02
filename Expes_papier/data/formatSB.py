from speechbrain.utils.edit_distance import wer_details_by_utterance as wer_details
from speechbrain.dataio.wer import print_alignments

import argparse
parser = argparse.ArgumentParser(description="Transform output file to a Speechbrain output")
parser.add_argument("namef", type=str, help="Path to a Kaldi test file output")
args = parser.parse_args()

ref = dict()
hyp = dict()
with open(args.namef + "/refhyp.txt", "r", encoding="utf8") as file:
    i = 0
    for ligne in file:
        ligne = ligne.split("\t")
        ref[i] = ligne[0].split(" ")
        hyp[i] = ligne[1].split(" ")
        i += 1


d = wer_details(ref, hyp, compute_alignments=True)
print_alignments(d, open(args.namef + "/" + args.namef + ".txt", "w", encoding="utf8"))
