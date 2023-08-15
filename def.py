from corrector import ScRNNChecker
checker = ScRNNChecker()
a=checker.correct_string(" airplane apart i don 't think i 've ever laughed at a film so much in all my life")
print(a)

# from corrector import ScRNNChecker
# f1 = open('C:/Users/liche/Desktop/AG/clean_1000.txt','r',encoding="utf_8")
# f2 = open('C:/Users/liche/Desktop/AG/clean_1000_sc.txt','w',encoding="utf_8")
# for line in f1:
#     line = line.strip()
#     checker = ScRNNChecker()
#     a=checker.correct_string(line)
#     f2.writelines(''.join(a)+'\n')


# from spellchecker import SpellChecker
# f1 = open('C:/Users/liche/Desktop/data/1000_all30_.txt','r',encoding="utf_16")
# f2 = open('C:/Users/liche/Desktop/data/sc-1.txt','w',encoding="utf_8")
# for line in f1:
#     line = line.strip()
#     spell = SpellChecker(distance=1)
#     misspelled=line.split()
#     # print(misspelled)
#     b = []
#     for word in misspelled:
#         a=spell.correction(word)
#         # print(a)
#         b.append(a)
#     # print(b)
#     f2.writelines(' '.join(b)+'\n')






