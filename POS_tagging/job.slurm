#!/bin/bash
#SBATCH --job-name=POSanalysis
#SBATCH --time=10:00:00
#SBATCH --output=out/POS.txt

conda activate
python eval.py
