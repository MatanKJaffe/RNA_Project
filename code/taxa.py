
def download_classifierS():
    os.system("""!wget https://data.qiime2.org/2021.8/common/gg-13-8-99-515-806-nb-F.qza
    !wget https://data.qiime2.org/2021.4/common/gg-13-8-99-nb-classifier.qza

    !wget https://data.qiime2.org/2021.4/common/silva-138-99-515-806-nb-classifier.qza
    !wget https://data.qiime2.org/2021.4/common/silva-138-99-nb-classifier.qza""")

gg_13_8_99_515_806_nb_classifier = "/home/geox-dev/Documents/RNA_Project/data/classifiers/gg-13-8-99-515-806-nb-classifier.qza"
gg_13_8_99_nb_classifier = "/home/geox-dev/Documents/RNA_Project/data/classifiers/gg-13-8-99-nb-classifier.qza"
silva_138_99_515_806_nb_classifier = "/home/geox-dev/Documents/RNA_Project/data/classifiers/silva-138-99-515-806-nb-classifier.qza"
silva_138_99_nb_classifier = "/home/geox-dev/Documents/RNA_Project/data/classifiers/silva-138-99-nb-classifier.qza"

classifier_dict = {"gg_13_8_99_515_806_nb_classifier":gg_13_8_99_515_806_nb_classifier,\
                    "gg_13_8_99_nb_classifier":gg_13_8_99_nb_classifier,\
                    "silva_138_99_515_806_nb_classifier":silva_138_99_515_806_nb_classifier,\
                    "silva_138_99_nb_classifier":silva_138_99_nb_classifier}


