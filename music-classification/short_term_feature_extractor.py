# Imports
from pyAudioAnalysis import audioBasicIO, MidTermFeatures, ShortTermFeatures
from pathlib import Path
import csv
import pandas as pd
import numpy as np

# Reads wav file
def read_audio_file(wav_file):
    [Fs, x] = audioBasicIO.read_audio_file(wav_file)
    return Fs, x


# Extracts all the features of the wav song
def feature_extraction(signal, sampling_rate, mid_window, mid_step, short_window, short_step):
    G, F, f_names = MidTermFeatures.mid_feature_extraction(signal, sampling_rate, mid_window, mid_step, short_window, short_step)
    return G, F, f_names


# Extracts short term features, and their names, from all features
def extract_short_term_features(features, features_names, variant):
    short_features_temp = []
    short_features = []
    short_features_names = []
    for x in range(0, 34):
        # Creates new array of only short term features and respective names
        short_features_temp.append(features[x])
        short_features_names.append(features_names[x])

    if variant:
        short_features = short_features_temp
    else:
        # Takes average of the window features to create one number for each feature, for each song
        for x in range(len(short_features_temp)):
            total = 0
            for y in range(len(short_features_temp[0])):
                total += short_features_temp[x][y]
            short_features.append(total / len(short_features_temp[x]))

    return short_features, short_features_names


# Creates csv file for short term features
def create_csv(csv_file_name, file_audio_name, short_features_names, short_features, variant, first_time):
    # Adds feature names to array
    short_features_names.insert(0, "Short Term Feature Names: ")
    if variant is False:
        # Adds name of each audio file
        short_features.insert(0, Path(file_audio_name).stem)
    if first_time:
        # Writes a file with the name
        with open(csv_file_name, 'w') as myFile:
            file_writer = csv.writer(myFile)
            # Adds feature names as first row
            file_writer.writerow(short_features_names)
            if variant:
                for i in range(len(short_features)):
                    file_writer.writerow(short_features[i])
            else:
                file_writer.writerow(short_features)
    else:
        with open(csv_file_name, 'a') as myFile:
            file_writer = csv.writer(myFile)
            if variant:
                for i in range(len(short_features)):
                    file_writer.writerow(short_features[i])
            else:
                file_writer.writerow(short_features)

    read_file = pd.read_csv(csv_file_name)
    read_file.to_csv(csv_file_name, index=False)

