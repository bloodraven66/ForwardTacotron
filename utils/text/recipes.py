from utils.files import get_files
from pathlib import Path
from typing import Union
import re

def ljspeech(path: Union[str, Path]):
    csv_file = get_files(path, extension='.txt')
    print(len(csv_file), csv_file[0])
    # assert len(csv_file) == 1

    text_dict = {}
    for i in range(len(csv_file)):
        with open(csv_file[i], encoding='utf-8') as f :
            for line in f :
                split = line.split('\t')
                
                if len(split)>1:
                    for i in range(len(split)):
                        split[i] = re.sub('\t', '', split[i])
                        split[i] = re.sub('\n', '', split[i])
                        split[i] = re.sub('\x00', '', split[i])
                    text_dict[split[0]] = split[-1]
            
    return text_dict