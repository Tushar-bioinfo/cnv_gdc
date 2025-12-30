#!/bin/bash
#SBATCH --job-name=GDC-SliceDownload
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --partition=rra
#SBATCH --qos=rra
#SBATCH --mem-per-cpu=2048
#SBATCH --output=./logs/out.GDC_SLICE.%j
#SBATCH --mail-type=ALL
#SBATCH --mail-user=st25@usf.edu
#SBATCH --array=0-394%10

# change this to your base path
basepath="/work/pi_gblanck/st25/my_work/cnv/tcga-cnv"

# include manifest file name as argument for working with clusters
# comment out if not working with clusters
#manifest=$1

# path to manifest, change this to your manifest location
# for small manifest files
PathToManifest="${basepath}/manifest.txt"

# for clusters
#PathToManifest="${basepath}/${manifest}"
#echo $PathToManifest

#path to download token, change this to your token location
Token="${basepath}/token.txt"

# change this path to the path you want the BAM files to go to
OutputFolder="${basepath}/bams"
mkdir -p $OutputFolder

mapfile -t myArray < $PathToManifest

NumberOfBams=$((${#myArray[@]} - 1))
echo "There are" $NumberOfBams "bam files"
echo "$InputString"
InputString=${myArray[$SLURM_ARRAY_TASK_ID]}
ID=$(cut -d',' -f1 <<< $InputString)
NAME=$(cut -d',' -f2 <<< $InputString)

echo "[$(date)] Working on -> $NAME "

APItext="https://api.gdc.cancer.gov/slicing/view/$ID?region=chr7:56064286-56080670" #Sumf2
token=$(<$Token)
curl --header "X-Auth-Token: $token" $APItext --output $OutputFolder/sliced_$NAME
