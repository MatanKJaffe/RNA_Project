
# !wget https://data.qiime2.org/2021.8/common/gg-13-8-99-515-806-nb-F.qza
# !wget https://data.qiime2.org/2021.4/common/gg-13-8-99-nb-classifier.qza

# !wget https://data.qiime2.org/2021.4/common/silva-138-99-515-806-nb-classifier.qza
# !wget https://data.qiime2.org/2021.4/common/silva-138-99-nb-classifier.qza

gg_13_8_99_515_806_nb_classifier:str = "/Users/osn/Code_Library/RNA_Project/data/classifiers/gg-13-8-99-515-806-nb-classifier.qza"
gg_13_8_99_nb_classifier:str = "/Users/osn/Code_Library/RNA_Project/data/classifiers/gg-13-8-99-nb-classifier.qza"
silva_138_99_515_806_nb_classifier:str = "/Users/osn/Code_Library/RNA_Project/data/classifiers/silva-138-99-515-806-nb-classifier.qza"
silva_138_99_nb_classifier:str = "/Users/osn/Code_Library/RNA_Project/data/classifiers/silva-138-99-nb-classifier.qza"

manifest:str = "/Users/osn/Code_Library/RNA_Project/data/metadata/Manifest.csv"
metadata_dir:str = "/Users/osn/Code_Library/RNA_Project/data/metadata"
output_dir:str = "/Users/osn/Code_Library/RNA_Project/output"

classifier_dict:dict = {"gg_13_8_99_515_806_nb":gg_13_8_99_515_806_nb_classifier,\
                    "gg_13_8_99_nb":gg_13_8_99_nb_classifier,\
                    "silva_138_99_515_806_nb":silva_138_99_515_806_nb_classifier,\
                    "silva_138_99_nb":silva_138_99_nb_classifier}

import os
def run_taxa_analysis(classifier_file, classifier_name, output_dir, metadata_dir) -> None:
    os.system(f"""
                qiime feature-classifier classify-sklearn \
                    --i-reads {output_dir}/dada2/representative_sequences.qza \
                    --i-classifier {classifier_file} \
                    --p-n-jobs 2 \
                    --o-classification {output_dir}/taxa/{classifier_name}/taxa.qza

                qiime taxa barplot \
                    --i-table {output_dir}/dada2/table.qza \
                    --i-taxonomy {output_dir}/taxa/{classifier_name}/taxa.qza \
                    --m-metadata-file {metadata_dir}/metadata.tsv \
                    --o-visualization {output_dir}/taxa/{classifier_name}/taxa_barplot.qzv

                qiime taxa collapse \
                    --i-table {output_dir}/dada2/table.qza \
                    --i-taxonomy {output_dir}/taxa/{classifier_name}/taxa.qza \
                    --p-level 6 \
                    --o-collapsed-table {output_dir}/taxa/{classifier_name}/genus.qza

                qiime tools export \
                    --input-path {output_dir}/taxa/{classifier_name}/genus.qza \
                    --output-path {output_dir}/taxa/{classifier_name}/exported

                biom convert -i {output_dir}/taxa/{classifier_name}/exported/feature-table.biom \
                            -o {output_dir}/taxa/{classifier_name}/genus.tsv --to-tsv
                """)

for classifier_name, classifier_file  in  classifier_dict.items():
    run_taxa_analysis(classifier_file, classifier_name, output_dir, metadata_dir)