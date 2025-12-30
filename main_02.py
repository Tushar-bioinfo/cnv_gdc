import pandas as pd
from pathlib import Path
import subprocess
from computeratio import computeratio
from datetime import datetime as dt


### File Paths ###
base_dir = Path.cwd()
sample_file = base_dir/'sample_sheet.tsv'
bam_dir = base_dir/'bams'

### Functions ###
def get_counts(bam_path, flag_exclude=260):
    """
    Count alignments with samtools view -c.
    Returns 0 if BAM file is missing or samtools fails.
    """
    bam_path = Path(bam_path)

    if not bam_path.exists():
        print(f"WARNING: Missing BAM file → {bam_path}")
        return 0

    cmd = ["samtools", "view", "-c", "-F", str(flag_exclude), str(bam_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        print(f"WARNING: samtools error for {bam_path}: {res.stderr}")
        return 0

    out = res.stdout.strip()
    return int(out) if out else 0

print(f'{" Starting ":-^49}')
print(f'{dt.now().strftime(" %Y-%m-%d %H:%M:%S "):-^50}')

### Read File ###
df = pd.read_csv(sample_file, sep='\t')

### Cleaning up columns ###
df['Tumor Descriptor']= df['Tumor Descriptor'].apply(lambda x: str(x).split(',')[0])
df['Case ID'] = df['Case ID'].apply(lambda x: str(x).split(',')[0])
df['File Name'] = df['File Name'].apply(lambda x: "sliced_" + x)
df['Specimen Type']    =  df['Specimen Type'].apply(lambda x: str(x).split(',')[0])
### New "Full Path" column ###
df['full_path'] = bam_dir/df['File Name']

### Mask to filter to the Normal and Blood ### 
mask = (
    (df['Tissue Type'] == 'Normal') &
    (df['Specimen Type'] == 'Peripheral Blood NOS')
)

#mask = (
#    (df['Tissue Type'] == 'Normal') &
#    (df['Specimen Type'].isin([
#        'Peripheral Blood Components NOS',
#        'Peripheral Blood NOS'
#    ]))
#)
# make an independent copy so assignments are safe
df_normal = df.loc[mask, ['Case ID','Project ID','File Name','Sample ID','Tissue Type','Tumor Descriptor','Specimen Type','full_path']].copy()

#df_normal = df[(df['Tissue Type'] == 'Normal') & (df['Specimen Type'] == 'Peripheral Blood Components NOS')]
# df_normal.set_index('File Name', inplace=True)
# df_normal['full_path'] = bam_dir / df_normal.index

print(f'{" Calculating Normal Counts ":-^49}')
print(f'{dt.now().strftime(" %Y-%m-%d %H:%M:%S "):-^50}')
df_normal['normal_count'] = df_normal['full_path'].apply(lambda x: get_counts(x))
print(df_normal['normal_count'].head())


subset = df_normal[['Case ID','normal_count']]
df = pd.merge(df, subset, on='Case ID', how='left')

### Filter to Primary and Recurrence only ###
df = df[df['Tumor Descriptor'].isin(['Primary'])]          ## Change here for different analyses ###
# df = df[df['Tumor Descriptor'].isin(['Primary','Recurrence'])]          ## Change here for different analyses ###

print(f'{" Calculating Tumor Counts ":-^49}')
print(f'{dt.now().strftime(" %Y-%m-%d %H:%M:%S "):-^50}')
df['tumor_count'] = df['full_path'].apply(lambda x: get_counts(x))

### Ratio Calculation ###
print(f'{" Calculating Final Ratio ":-^49}')
print(f'{dt.now().strftime(" %Y-%m-%d %H:%M:%S "):-^50}')
df['Ratio(Tumor Count/Blood Count)'] = df.apply(lambda x: computeratio(x['tumor_count'], x['normal_count']), axis=1)
### Reodering columns ###
df = df[['File Name','Sample ID','Case ID','Tumor Descriptor','Project ID','tumor_count','normal_count','Ratio(Tumor Count/Blood Count)']]
### saving to csv ###
df.to_csv('./final.csv')
print(f'{" Finished ":=^100}')
print(f'{dt.now().strftime(" %Y-%m-%d %H:%M:%S "):-^50}')
