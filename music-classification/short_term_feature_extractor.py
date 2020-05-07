# Imports
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import ShortTermFeatures
from pathlib import Path
import csv
import pandas as pd


# Reads wav file
def read_audio_file(wav_file):
    [Fs, x] = audioBasicIO.read_audio_file(wav_file)
    return Fs, x


# Extracts all the features of the wav song
def feature_extraction(signal, sampling_rate, window, step, deltas=True):
    F, f_names = ShortTermFeatures.feature_extraction(signal, sampling_rate, window, step, deltas)
    return F, f_names


# Extracts short term features, and their names, from all features
def extract_short_term_features(features, features_names, variant):
    short_features = []
    short_features_names = []
    for x in range(0, 34):
        # Creates new array of only short term features and respective names
        short_features.append(features[x])
        short_features_names.append(features_names[x])

    if variant is False:
        # Flattens 2d list into 1d list
        short_features = [i for num in short_features for i in num]

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

