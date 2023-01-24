import os
manifest:str = "/Users/osn/Code_Library/RNA_Project/data/metadata/Manifest.csv"
metadata_dir:str = "/Users/osn/Code_Library/RNA_Project/data/metadata"
output_dir:str = "/Users/osn/Code_Library/RNA_Project/output"
os.system(f"""qiime tools import \
        --type 'SampleData[PairedEndSequencesWithQuality]' \
        --input-path {manifest} \
        --output-path {output_dir}/demux/sequences.qza \
        --input-format 'PairedEndFastqManifestPhred33'

        qiime demux summarize \
                --i-data {output_dir}/demux/sequences.qza \
                --o-visualization {output_dir}/demux/qualities.qzv
        """)
os.system(f"""qiime tools import \
                --type 'SampleData[PairedEndSequencesWithQuality]' \
                --input-path {manifest} \
                --output-path {output_dir}/demux/sequences.qza \
                --input-format 'PairedEndFastqManifestPhred33'

        qiime demux summarize \
                --i-data {output_dir}/demux/sequences.qza 
                --o-visualization {output_dir}/demux/qualities.qzv
        """)


def denoise_paired(output_dir:str, trunc_len_f:int, trunc_len_r:int,\
                        trim_left_f:int = 0, trim_left_r:int =0) -> None:

                
        os.system(f"""qiime dada2 denoise-paired \
                        --i-demultiplexed-seqs {output_dir}/demux/sequences.qza \
                        --p-trunc-len-f {trunc_len_f} \
                        --p-trunc-len-r {trunc_len_r} \
                        --p-trim-left-f {trim_left_f} \
                        --p-trim-left-r {trim_left_r} \
                        --p-n-threads 0 \
                        --o-table {output_dir}/dada2/table.qza \
                        --o-representative-sequences {output_dir}/dada2/representative_sequences.qza \
                        --o-denoising-stats {output_dir}/dada2/denoising_stats.qza \
                        --verbose""") 
denoise_paired(output_dir= output_dir,trunc_len_f=240,trim_left_f=6,\
                trim_left_r=6,trunc_len_r=280)

os.system(f"""qiime metadata tabulate \
                --m-input-file {output_dir}/dada2/denoising_stats.qza \
                --o-visualization {output_dir}/dada2/denoising-stats.qzv""")

os.system(f"""qiime phylogeny align-to-tree-mafft-fasttree \
                        --i-sequences {output_dir}/dada2/representative_sequences.qza \
                        --output-dir tree 

                qiime empress tree-plot \
                        --i-tree {output_dir}/tree/rooted_tree.qza \
                        --o-visualization {output_dir}/tree/empress.qzv""")

os.system(f"""qiime diversity core-metrics-phylogenetic \
                        --i-table {output_dir}/dada2/table.qza \
                        --i-phylogeny {output_dir}/tree/rooted_tree.qza \
                        --p-sampling-depth 10000 \
                        --m-metadata-file {metadata_dir}/metadata.tsv \
                        --output-dir diversity""")

os.system(f"""qiime diversity alpha-group-significance \
                        --i-alpha-diversity {output_dir}/diversity/shannon_vector.qza \
                        --m-metadata-file {metadata_dir}/metadata.tsv \
                        --o-visualization {output_dir}/diversity/alpha_groups.qzv""")

os.system(f"""qiime diversity adonis \
                        --i-distance-matrix {output_dir}/diversity/weighted_unifrac_distance_matrix.qza \
                        --m-metadata-file {metadata_dir}/metadata.tsv \
                        --p-formula "Remarks" \
                        --p-n-jobs 2 \
                        --o-visualization {output_dir}/diversity/permanova.qzv """)