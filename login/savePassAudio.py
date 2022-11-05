import argparse
import json
import sys
from argparse import RawTextHelpFormatter
from os.path import isdir

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

DEFAULT_CONFIG_FILE = "dejavu.cnf.SAMPLE"


def init(configpath):
    """
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting")
        sys.exit(1)

    # create a Dejavu instance
    return Dejavu(config)


if __name__ == '__main__':
    config_file = DEFAULT_CONFIG_FILE
    djv = init(config_file)
    directory = '../music_generator/'
    extension = 'wav'
    print(f"Fingerprinting all .{extension} files in the {directory} directory")
    djv.fingerprint_directory(directory, ["." + extension], 4)
 
            
            
            
