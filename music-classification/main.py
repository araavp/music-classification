# Imports
import pathlib
from pathlib import Path
import os
import short_term_feature_extractor as stfe
import convert_mp3_to_wav as convert

# Declare variables
first_time = True
## If you want first_variant keep True, if you want second variant, make False
first_variant = True
## File path to folder where the audio files are located
file_path = "test_audio"


# Converts all mp3 files to wav files
convert.convert_dir_mp3_to_wav(file_path, 16000, 1)

# Loops through file with audio
for file in pathlib.Path(file_path).iterdir():
    # Finds the type of file
    file_type = os.path.splitext(str(file))[-1].lower()

    # Only processes if it is a .wav file
    if file_type == ".wav":
        # Reads audio file
        [Fs, x] = stfe.read_audio_file(file)

        # Default csv file name for second variant
        csv_name = "audio_st_features.csv"

        # Extracts features
        if first_variant:
            F, f_names = stfe.feature_extraction(x, Fs, 0.500 * Fs, 0.500 * Fs)
            # Creates individual csv file
            csv_name = (Path(file).stem + "_st_features.csv")
        else:
            F, f_names = stfe.feature_extraction(x, Fs, 45.0 * Fs, 45.0 * Fs)

        # Extracts short term features
        short_term_features, short_term_features_names = stfe.extract_short_term_features(F, f_names)

        if first_variant:
            # Flips rows and cols
            short_term_features = [[short_term_features[j][i] for j in range(len(short_term_features))] for i in range(len(short_term_features[0]))]
            # Adds windows to short_term_features
            window = 0
            # Determines each window's length
            window_length = (45 / len(F[0]))

            # Adds windows in rows
            for i in range(len(short_term_features)):
                short_term_features[i].insert(0, window)
                window += window_length

        # Creates csv file
        stfe.create_csv(csv_name, file, short_term_features_names, short_term_features, first_variant, first_time)

        # Signals that next loop is not the first one - helps with editing csv file
        if first_variant is False:
            first_time = False

    # Runs else if file is not type .wav
    else:
        # Get rid of this if you want to keep the original mp3 files
        os.remove(str(file))
