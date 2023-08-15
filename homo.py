import numpy as np
from PIL import Image,ImageDraw,ImageFont
import csv
import os 
import homoglyphs as hg

# os.environ["CUDA_VISIBLE_DEVICES"] = "2"
class dataset:
    def __init__(self, filename, line=3):
        self.output = []
        self.content = []
        self.columns = line  # 2
        self.loadcsv(filename)

    def loadcsv(self, filename, line=3):
        reader = csv.reader(open(filename, "rt", encoding = 'utf-8'))
        count = 0
        for row in reader:
            # print(row[0])
            if self.columns==2:
                if int(row[0]) == 2:
                    self.output.append(2)
                    self.content.append((row[1].lower()))
                else:
                    self.output.append(1)
                    self.content.append((row[1].lower()))


def homoglyph(filename):
    fr = open(filename, 'r', encoding='utf-16')
    dict_homo = {}
    for lines in fr:
        if len(lines.strip()) != 0:
            if lines.strip()[0] != '/':
                chinese = lines.strip().split('	')
                dict_homo[chinese[0]] = chinese[1]
    return dict_homo

def generate_imgs(char,i):
    img = Image.new('F', (50,50))
    dimg = ImageDraw.Draw(img)
    dimg.text((14,5),char,fill="white",font=ImageFont.truetype("Arial.ttf",40))
    img1 = img.convert("L")
    img1 = img1.resize((28,28))
    # img.show()
    # img1 = img.convert("L")
    # img1 = img1.resize((28,28))
    # img1.save("imgs/"+ str(i) + ".png" )
    return(img1)
# generate_imgs("ë",'_')

####generate ACSII images
# ff = open('fuhao.txt', 'r', encoding='utf-16')
# i = 1
# for item in ff:
#     ch = item.strip()
#     generate_imgs(ch,i)
#     i = i+1

#####homotxt to dict
def process(word):
    word = word.replace("：",":")
    word = word.replace("，",",")
    word = word.replace("。",".")
    word = word.replace("’","'")
    word = word.replace("‘","'")
    word = word.replace("“","\"")
    word = word.replace("？","?")
    word = word.replace("！","!")
    word = word.replace('\\n',"")
    word = word.replace("\\","")
    return word


def homo_clean(word):
    word = process(word)
    for m in range(len(word)):
        uni = word[m].encode('unicode_escape').decode()#change to unicode
        # print(uni)
        if uni[2:].upper() in kk:
            us = kk[uni[2:].upper()]
            rechar = us
            s = m
            word = word[:s] + rechar + word[s + 1:]
        elif len(uni) > 2:
            homoglyphs = hg.Homoglyphs(languages={'en'}, strategy=hg.STRATEGY_LOAD, ascii_strategy=hg.STRATEGY_REMOVE, ascii_range=range(ord('a'), ord('z')),)
            rechar=homoglyphs.to_ascii(word[m])
            if rechar :
                s = m
                # print(rechar)
                word = word[:s] + rechar[0] + word[s+1:]
    # print(word)
    return word

#####transform char by txt
def trans(word):
    for m in range(len(word)):
        for k, v in hm.items():
            v.replace(" ", "")
            if word[m] in v:
                s = m
                reletter = k
                word = word[:s] + reletter + word[s+1:]
    return word

def process(word):
    word = word.replace("：",":")
    word = word.replace("，",",")
    word = word.replace("。",".")
    word = word.replace("’","'")
    word = word.replace("‘","'")
    word = word.replace("“","\"")
    word = word.replace("？","?")
    word = word.replace("！","!")
    word = word.replace('\\n',"")
    word = word.replace("\\","")
    return word

def kuang(filename):
    fr = open(filename, 'r', encoding='utf-16')
    dict_kuang = {}
    for lines in fr:
        if len(lines.strip()) != 0:
            if lines.strip()[0] != '/':
                chinese = lines.strip().split('\t')
                dict_kuang[chinese[0]] = chinese[1]
    return dict_kuang
kk = kuang("kuang_char.txt")

if __name__ == '__main__':
#####rewrite by simi
    result = "result/adv_1000_choose_homo.txt"
    # result = "result/0.txt"
    fw = open(result, 'a', encoding="utf-16")

    # res = dataset("test-ICES-0.3.CSV",2)
    # print(res.output[:5])
    # print(res.content[:5])
    # pos_ = res.content
    # label = res.output
    pos_ = read_txt('data/adv_1000_choose.txt')
    # print(pos_)
    name = 1
    for i in range(len(pos_)):
        sentence = []
        a = pos_[i]
        a = homo_clean(a,name)
        # name = name+100
        # for j in a.split():
        #     sentence.append(spell.correction(j))
        # s = " ".join(sentence)
        print(a)
        # # fw.writelines(str(pos_[i])+","+ s)
        fw.writelines(a)
        fw.writelines(('\n'))