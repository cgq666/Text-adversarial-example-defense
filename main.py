import numpy as np
from corrector import ScRNNChecker
import GoogleTranslator
import GoogleTranslator1
import homo
import enchant
import csv
import os 

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def read_txt(filename):
    pos = []
    with open(filename, 'r',encoding='utf-8') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
                pass
            pos.append(lines.strip())
    return pos

# def get_spell(line):
#     re = []
#     for word in line:
#         a = dic.check(word)
#         re.append(a)
#     return(re)

if __name__ == '__main__':

    # filename = "data1/clean_1000_homo.txt"
    # fw1 = open(filename, 'a', encoding="utf-16")

    # filename = "data1/clean_1000_homosc.txt"
    # fw2 = open(filename, 'a', encoding="utf-16")

    # filename = "data1/clean_1000_sc.txt"
    # fw3 = open(filename, 'a', encoding="utf-16")

    # filename = "data1/CNN/cnn_adv_1000_trans.txt"
    # fw4 = open(filename, 'a', encoding="utf-16")

    # filename = "data1/CNN/cnn_adv_1000_trans.txt"
    # fw5 = open(filename, 'a', encoding="utf-16")
    
    filename = "./data/ag/adv_def.txt"
    fw = open(filename, 'a', encoding="utf-16")

    text = read_txt('./data/ag/adv.txt')
    checker = ScRNNChecker()
    # translator = GoogleTranslator.GoogleTranslator()
    # translator1 = GoogleTranslator1.GoogleTranslator1()
    dic = enchant.Dict("en_US")
    count = 0
    for line in text:
        sentence = []
        text_homo = homo.homo_clean(line)
        text_homos = text_homo.split()
        re = []
        for word in text_homos:
            a = dic.check(word)
            re.append(a)
        # re = get_spell(text_homos)
        if False in re:
            text_homo_sc = checker.correct_string(text_homo)
            fw.write(text_homo_sc.strip() + "\n")
        else:
            text_homo_sc = text_homo
            fw.write(text_homo.strip() + "\n")
        # print(text_homo_sc)

        if len(text_homo_sc) > 1:
            count += 1
            print('\r' + str(count), end = '', flush = True)
            result, success = translator.translate(text_homo_sc)
            if success:
                result1 = translator1.translate(result)
                fw.write(result1.strip() + "\n")
                print(result1)
            else:
                fw.write(result.strip() + "\n")
                print(result)