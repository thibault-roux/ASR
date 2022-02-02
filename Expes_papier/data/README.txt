Indices:
KD = Kaldi
SP = Ancien Speechbrain
SB = Speechbrain
KD_wR = Kaldi model with language model Rescoring
KD_woR = Kaldi model without language model Rescoring
KDW_wR = Kaldi model with LMR with wav2vec input
KDW_woR = Kaldi model with LMR without wav2vec input

Code:
- kd2ref-hyp.py
	-> args : KD_woR ou KD_wR ou KDW_wor ou KW_wR
	-> fichier qui transforme un output kaldi en fichier ref avec hypothèse
- formatSB.py
	-> args : KD_woR ou KD_wR ou KDW_wor ou KW_wR









