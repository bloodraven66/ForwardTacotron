from utils.files import get_files
from pathlib import Path
from typing import Union
import re

def ljspeech(path: Union[str, Path]):
    csv_file = get_files(path, extension='.txt')
    text_dict = {}
    clean_text = ['\t', '\n', '\x00']
    count_edge = 0
    first_case = 0
    lengthzero_underscore_reject = 0
    key_no_match = 0
    lengthzero_underscore_accept = 0
    zero_length = 0
    key_no_match_outlier = 0
    count = 0
    file_matching_counter = {}
    for i in range(len(csv_file)):
        with open(csv_file[i], encoding='utf-8') as f :
            for line in f :
                split = line.split('\t')
                #space between key and text
                if len(split)>1:
                    for i in range(len(split)):
                        for remove_word in clean_text:
                            if remove_word in split[i]:
                                split[i] = re.sub(remove_word, '', split[i])
                    text_dict[split[0]] = split[-1]
                    first_case += 1
                else:
                    # if count_edge < 10000:
                        if len(split)>1:
                            print('check length 1+')
                        split = split[0]
                        for remove_word in clean_text:
                            if remove_word in split:
                                split = re.sub(remove_word, '', split)

                        if len(split) > 0:
                            count += 1
                            #key in underscore
                            underscore_split = split.split('_')
                            if len(underscore_split)>2:
                                key_text_mix = underscore_split[2:][0]
                                current_key = ''
                                for ch in key_text_mix:
                                    if ch.isdigit():
                                        current_key += ch
                                    else:
                                        break

                                key = underscore_split[0] + '_' + underscore_split[1] + '_' + current_key
                                if len(key_text_mix[len(current_key):]) > 0:
                                    text_dict[key] = key_text_mix[len(current_key):]
                                    lengthzero_underscore_accept += 1
                                else:
                                    lengthzero_underscore_reject += 1
                            #key not corresponding to file names
                            else:
                                # if count_edge <10:
                                    key_from_file = str(csv_file[i]).split('/')[-1][:-4]
                                    if key_from_file in file_matching_counter:
                                        file_matching_counter[key_from_file] += 1
                                    else:
                                        file_matching_counter[key_from_file] = 1
                                    current_key = key_from_file + '_' +     str(file_matching_counter[key_from_file])
                                    # print(current_key, split, csv_file[i], key_from_file)
                                    # print(current_key, split.split('.'))
                                    if len(split.split('.')) == 2:
                                        text_dict[current_key] = split.split('.')[-1]
                                        key_no_match += 1
                                    else:
                                        key_no_match_outlier += 1
                        else:
                            zero_length += 1
    print('first_case:', first_case)
    print('key_no_match:', key_no_match)
    print('lengthzero_underscore_reject:',lengthzero_underscore_reject)
    print('lengthzero_underscore_accept:',lengthzero_underscore_accept)
    print('zero_length:', zero_length)
    print('key_no_match_outlier:',key_no_match_outlier)
    print('total:', first_case+key_no_match+lengthzero_underscore_reject+lengthzero_underscore_accept+key_no_match_outlier)
    return text_dict
