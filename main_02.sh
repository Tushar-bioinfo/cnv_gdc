#!/bin/bash
#SBATCH --job-name=mos
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=150G
#SBATCH --ntasks=1
#SBATCH --partition=rra
#SBATCH --qos=rra
#SBATCH --output=/work/pi_gblanck/st25/my_work/cnv/tcga-cnv/logs/%A_%a.log

source /home/s/st25/miniconda3/etc/profile.d/conda.sh
conda activate sra

echo "[ $(date) Starting ...]"

python main_02.py

echo "[ $(date) Done ...]"
