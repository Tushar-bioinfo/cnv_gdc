from pathlib import Path
import pandas as pd

base_dir = Path().cwd()
bams_dir = base_dir /"bams"
manifest = base_dir /"raw_manifest.txt"

df = pd.read_csv(manifest,sep="\t")
all_files = set(df['filename'].to_list())

files_done = set([(i.name).replace("sliced_","") for i in bams_dir.glob('*.bam')])

files_missing = all_files - files_done

print("Total files left",len(files_missing))

new_df = pd.merge(df,pd.DataFrame({'filename':list(files_missing)}),on='filename')
print(new_df.head())
new_df.to_csv(base_dir /"manifest.txt",sep="\t",index=False)
