from qiime2 import Artifact
demultiplexed_sequences = Artifact.import_data('SampleData[PairedEndSequencesWithQuality]',
                                "/home/geox-dev/Documents/RNA_Project/data/Manifest.csv",
                                view_type='PairedEndFastqManifestPhred33')

import qiime2.plugins.demux.actions as demux_actions
demultiplexed_sequences_summ_viz, = demux_actions.summarize(
    data=demultiplexed_sequences,)

demultiplexed_sequences_summ_viz.save("demultiplexed_sequences_summ_viz")
demultiplexed_sequences.save("demultiplexed_sequences")

import qiime2.plugins.dada2.actions as dada2_actions
feature_table_0, asv_sequences_0, dada2_stats = dada2_actions.denoise_paired(
    demultiplexed_seqs=demultiplexed_sequences,
    trunc_len_f=240,
    trim_left_f=6,
    trim_left_r=6,
    trunc_len_r=280,)

feature_table_0.save("feature_table_0")
asv_sequences_0.save("asv_sequences_0")
dada2_stats.save("dada2_stats")

import qiime2.plugins.feature_table.actions as feature_table_actions
asv_sequences_0_summ_viz, = feature_table_actions.tabulate_seqs(
    data=asv_sequences_0)

!qiime metadata tabulate \
    --m-input-file dada2_stats.qza \
    --o-visualization dada2_stats.qzv
    
from qiime2.plugins.phylogeny.pipelines import align_to_tree_mafft_fasttree
alignment, masked_alignment, tree, rooted_tree = align_to_tree_mafft_fasttree(asv_sequences_0)
alignment.save("alignment")
masked_alignment.save("masked_alignment")
tree.save("tree")
rooted_tree.save("rooted_tree")

from qiime2 import Metadata
sample_metadata_md = Metadata.load("/home/geox-dev/Documents/RNA_Project/data/metadata.tsv")

from qiime2.plugins.feature_table.methods import filter_features
feature_table_0 = filter_features(feature_table_0, metadata = sample_metadata_md)

from qiime2.plugins.diversity.pipelines import core_metrics_phylogenetic
rarefied_table , faith_pd_vector, observed_features_vector,\
shannon_vector, evenness_vector, unweighted_unifrac_distance_matrix,\
weighted_unifrac_distance_matrix, jaccard_distance_matrix,\
bray_curtis_distance_matrix ,unweighted_unifrac_pcoa_results,\
weighted_unifrac_pcoa_results, jaccard_pcoa_results,\
bray_curtis_pcoa_results ,unweighted_unifrac_emperor,\
weighted_unifrac_emperor, jaccard_emperor,\
bray_curtis_emperor= core_metrics_phylogenetic(table = feature_table_0,
                          phylogeny = rooted_tree,
                          sampling_depth = 10000,
                          metadata = sample_metadata_md )

!qiime feature-table filter-samples \
  --i-table /home/geox-dev/Documents/RNA_Project/code/feature_table_0.qza \
  --m-metadata-file  /home/geox-dev/Documents/RNA_Project/data/metadata.tsv \
  --o-filtered-table filtered-table.qza
  
!qiime diversity core-metrics-phylogenetic \
    --i-table /home/geox-dev/Documents/RNA_Project/code/filtered-table.qza\
    --i-phylogeny /home/geox-dev/Documents/RNA_Project/code/rooted_tree.qza \
    --p-sampling-depth 1000 \
    --m-metadata-file /home/geox-dev/Documents/RNA_Project/data/metadata.tsv \
    --output-dir diverstiy \
    --verbose \
    --p-n-jobs-or-threads auto \
    --p-with-replacement \
    # --o-rarefied-table diverstiy\
    # --o-faith-pd-vector diverstiy \
    # --o-observed-features-vector diverstiy \
    # --o-shannon-vector diverstiy \
    # --o-evenness-vector diverstiy \
    # --o-unweighted-unifrac-distance-matrix diverstiy \
    # --o-weighted-unifrac-distance-matrix diverstiy \
    # --o-jaccard-distance-matrix diverstiy \
    # --o-bray-curtis-distance-matrix diverstiy \
    # --o-unweighted-unifrac-pcoa-results diverstiy \
    # --o-weighted-unifrac-pcoa-results diverstiy \
    # --o-jaccard-pcoa-results diverstiy \
    # --o-bray-curtis-pcoa-results diverstiy \
    # --o-unweighted-unifrac-emperor diverstiy \
    # --o-weighted-unifrac-emperor diverstiy \
    # --o-jaccard-emperor diverstiy \
    # --o-bray-curtis-emperor diverstiy \
    # --o-jaccard-emperor /home/geox-dev/Documents/RNA_Project/code/diverstiy/\
    # --o-bray-curtis-emperor /home/geox-dev/Documents/RNA_Project/code/diverstiy/

!qiime diversity alpha-group-significance \
    --i-alpha-diversity /home/geox-dev/Documents/RNA_Project/output/diverstiy/shannon_vector.qza \
    --m-metadata-file /home/geox-dev/Documents/RNA_Project/data/metadata/metadata.tsv\
    --o-visualization /home/geox-dev/Documents/RNA_Project/output/diverstiy/alpha_groups.qzv
    
    
!qiime diversity adonis \
    --i-distance-matrix /home/geox-dev/Documents/RNA_Project/output/diverstiy/weighted_unifrac_distance_matrix.qza \
    --m-metadata-file /home/geox-dev/Documents/RNA_Project//home/geox-dev/Documents/RNA_Project/data/metadata/metadata.tsv \
    --p-formula "Remarks" \
    --p-n-jobs 5 \
    --o-visualization /home/geox-dev/Documents/RNA_Project/output/diverstiy/permanova.qzv
    
    