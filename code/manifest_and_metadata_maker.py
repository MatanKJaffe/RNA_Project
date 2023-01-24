#!/usr/bin/env python3

import argparse
import glob
import os
import send2trash
import pandas as pd
import csv


class FormatError(Exception):
    '''Formating of file is incompatioble with this program.'''
    pass

class Fasta_File_Meta:

    '''A class used to store metadata for fasta files, for importing into qiime2.'''

    def __init__(self, file_path) -> None:
        self.absolute_path = file_path

        path,file_name   = os.path.split(file_path)
        self.filename = file_name

        try:
            file_parts = file_name.split(".")
            if file_parts[1][0] == "R":
                self.format = "Basic"
            else:
                raise ValueError
            self.sample_id = file_parts[0]
        except ValueError:
            file_parts = file_name.split("_")
            if file_parts[1][0] == "S":
                self.format = "Illumina"
                self.sample_id = file_parts[0]
            else:
                self.format = "Unknown"
        
        
        if self.format == "Basic":
            if file_parts[1] == "R1":
                self.direction = "forward"
            else:
                if file_parts[1] == "R2":
                    self.direction = "reverse"
                else:
                    raise FormatError("Files do not follow Illumina or Basic filename conventions.")
        if self.format == "Illumina":
            if file_parts[3] == "R1":
                self.direction = "forward"
            else:
                if file_parts[3] == "R2":
                    self.direction = "reverse"
                else:
                    raise FormatError("Files do not follow Illumina or Basic filename conventions.")
        if self.format == "Unknown":
            raise FormatError("Files do not follow Illumina or Basic filename conventions.")

#Global functions
def delete_file(file_in):
    file_exists = os.path.isfile(file_in)
    if file_exists == True:
        send2trash.send2trash(file_in)

def save_manifest_file(fasta_list,folder):
    writer_name = f"{folder}/metadata/Manifest.csv"
    delete_file(writer_name)
    writer = open(writer_name, "w")
    header = "sample-id,absolute-filepath,direction\n"
    writer.write(header)
    for fasta in fasta_list:
        line =  str(fasta.sample_id) + "," + str(fasta.absolute_path) + "," + str(fasta.direction) + "\n"
        writer.write(line)
    writer.close()

def assign_fasta_2_class(file_paths):
    fasta_meta_list = []
    for path in file_paths:
        info = Fasta_File_Meta(path)
        fasta_meta_list.append(info)
    return fasta_meta_list

def get_file_list(directory):
    dir_abs = os.path.abspath(directory)
    print("Making manifest file for fastq.gz files in " + dir_abs + "/*.fastq.gz")
    file_paths_rel = glob.glob(dir_abs + "/*.fastq.gz")
    file_paths_abs = []
    for path in file_paths_rel:
        path_abs = os.path.abspath(path)
        file_paths_abs.append(path_abs)
    return file_paths_abs

def get_args():
    parser = argparse.ArgumentParser(description='''Script to make a Manifest.csv file for importing fastq.gz files into a qiime 2 environment.''')
    parser.add_argument("--input_dir", help="Essential: Input directory for samples.", required=True)
    args = parser.parse_args()
    return args

def get_all_folders(directory:str) -> list:
    all_folders = []
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            all_folders.append(os.path.join(root, name))
    return all_folders

def make_manifest(data_directory):
    # options = get_args()
    
    all_folders =get_all_folders(data_directory)
    full_fasta_class_list = []
    for folder in all_folders:
        file_paths = get_file_list(folder)
        
        fasta_class_list = assign_fasta_2_class(file_paths)
        full_fasta_class_list.extend(fasta_class_list)
    save_manifest_file(full_fasta_class_list,data_directory)

def make_metadata(data_directory):
    manifest = pd.read_csv(f"{data_directory}/metadata/Manifest.csv")
    sample_names = manifest["sample-id"]
    manifest["sample_names"] = list(["".join(list_obj[1:]) for list_obj in sample_names.str.split("-")])

    sample_names = list(set(["".join(list_obj[1:]) for list_obj in sample_names.str.split("-")]))
    metadata = pd.read_excel(f"{data_directory}/metadata/metadata.xlsx")
    metadata = metadata.loc[metadata["Sample Name"].isin(sample_names)].reset_index(drop = True)
    name_id_match = manifest[["sample-id", "sample_names"]].drop_duplicates().reset_index(drop = True)
    metadata["sample-id"] = [name_id_match.loc[name_id_match["sample_names"] == sample,"sample-id"].values[0] for sample in metadata["Sample Name"]]
    metadata[['sample-id','Sample Name', 'gDNA or PCR product',
       'If PCR, does it contain CS1/CS2 linkers?',
       'Primer set used or to be used ', 'Expected amplicon size',
       'PCR cycles', 'Volume( ul) ', 'Source', 'Remarks']].to_csv(f"{data_directory}/metadata/metadata.csv", index = False)
    csv_to_tsv(f"{data_directory}/metadata/metadata")
    
def csv_to_tsv(file) -> None:
    csv.writer(open(f'{file}.tsv', 'w+'),
            delimiter='\t').writerows(csv.reader(open(f"{file}.csv")))
    
if __name__ == "__main__":
    data_directory:str = "/Users/osn/Code_Library/RNA_Project/data"
    make_manifest(data_directory)
    make_metadata(data_directory)
