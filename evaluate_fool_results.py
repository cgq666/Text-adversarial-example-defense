from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import os
import argparse
from read_files import split_imdb_files, split_yahoo_files, split_agnews_files, split_sst_files,split_toxic_files,split_enron_files
from word_level_process import word_process, get_tokenizer, text_to_vector_for_all
from char_level_process import char_process, doc_process_for_all, get_embedding_dict
from neural_networks import word_cnn, char_cnn, bd_lstm, lstm
import spacy
import tensorflow as tf
from keras import backend as K
import numpy as np

os.environ["HDF5_USE_FILE_LOCKING"] = 'FALSE'
nlp = spacy.load('en_core_web_sm')

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
config.gpu_options.allow_growth = True
K.set_session(tf.compat.v1.Session(config=config))

parser = argparse.ArgumentParser(
    description='Evaluate fool accuracy for a text classifier.')
parser.add_argument('--clean_samples_cap',
                    help='Amount of clean(test) samples to fool',
                    type=int, default=10)
parser.add_argument('-m', '--model',
                    help='The model of text classifier',
                    choices=['word_cnn', 'char_cnn', 'word_lstm', 'word_bdlstm'],
                    default='word_cnn')
parser.add_argument('-d', '--dataset',
                    help='Data set',
                    choices=['imdb', 'agnews', 'yahoo', 'sst','toxic','enron'],
                    default='agnews')
parser.add_argument('-l', '--level',
                    help='The level of process dataset',
                    choices=['word', 'char'],
                    default='word')


def read_adversarial_file(adversarial_text_path):
    adversarial_text = list(open(adversarial_text_path, "r", encoding='latin-1').readlines())
    # remove sub_rate and NE_rate at the end of the text
    adversarial_text = [re.sub(' sub_rate.*', '', s) for s in adversarial_text]
    return adversarial_text


def get_mean_sub_rate(adversarial_text_path):
    adversarial_text = list(open(adversarial_text_path, "r", encoding='utf-16').readlines())
    all_sub_rate = []
    sub_rate_list = []
    for index, text in enumerate(adversarial_text):
        sub_rate = re.findall('\d+.\d+(?=; NE_rate)', text)
        if len(sub_rate) != 0:
            sub_rate = sub_rate[0]
            all_sub_rate.append(float(sub_rate))
            sub_rate_list.append((index, float(sub_rate)))
    mean_sub_rate = sum(all_sub_rate) / len(all_sub_rate)
    sub_rate_list.sort(key=lambda t: t[1], reverse=True)
    return mean_sub_rate


def get_mean_NE_rate(adversarial_text_path):
    adversarial_text = list(open(adversarial_text_path, "r", encoding='utf-16').readlines())
    all_NE_rate = []
    NE_rate_list = []
    for index, text in enumerate(adversarial_text):
        words = text.split(' ')
        NE_rate = float(words[-1].replace('\n', ''))
        all_NE_rate.append(NE_rate)
        NE_rate_list.append((index, NE_rate))
    mean_NE_rate = sum(all_NE_rate) / len(all_NE_rate)
    NE_rate_list.sort(key=lambda t: t[1], reverse=True)
    return mean_NE_rate


if __name__ == '__main__':
    args = parser.parse_args()
    clean_samples_cap = args.clean_samples_cap  # 1000

    # get tokenizer
    dataset = args.dataset
    tokenizer = get_tokenizer(dataset)

    # Read data set
    x_train = y_train = x_test = y_test = None
    test_texts = None
    first_get_dataset = False
    if dataset == 'imdb':
        train_texts, train_labels, test_texts, test_labels = split_imdb_files()
        if args.level == 'word':
            x_train, y_train, x_test, y_test = word_process(train_texts, train_labels, test_texts, test_labels, dataset)
        elif args.level == 'char':
            x_train, y_train, x_test, y_test = char_process(train_texts, train_labels, test_texts, test_labels, dataset)
    elif dataset == 'agnews':
        train_texts, train_labels, test_texts, test_labels = split_agnews_files()
        if args.level == 'word':
            x_train, y_train, x_test, y_test = word_process(train_texts, train_labels, test_texts, test_labels, dataset)
        elif args.level == 'char':
            x_train, y_train, x_test, y_test = char_process(train_texts, train_labels, test_texts, test_labels, dataset)
    elif dataset == 'yahoo':
        train_texts, train_labels, test_texts, test_labels = split_yahoo_files()
        if args.level == 'word':
            x_train, y_train, x_test, y_test = word_process(train_texts, train_labels, test_texts, test_labels, dataset)
        elif args.level == 'char':
            x_train, y_train, x_test, y_test = char_process(train_texts, train_labels, test_texts, test_labels, dataset)
    elif dataset == 'sst':
        train_texts,train_labels,test_texts,test_labels = split_sst_files()
        if args.level == 'word':
            x_train,y_train,x_test,y_test = word_process(train_texts, train_labels, test_texts, test_labels, dataset)
        elif args.level == 'char':
            x_train, y_train, x_test, y_test = char_process(train_texts, train_labels, test_texts, test_labels, dataset)
    elif dataset == 'toxic':
        train_texts, train_labels, test_texts, test_labels = split_toxic_files()
        if args.level == 'word':
            x_train, y_train, x_test, y_test = word_process(train_texts, train_labels, test_texts, test_labels,dataset)
        elif args.level == 'char':
            x_train, y_train, x_test, y_test = char_process(train_texts, train_labels, test_texts, test_labels,dataset)
    elif dataset == 'enron':
        train_texts, train_labels, test_texts, test_labels = split_enron_files()
        if args.level == 'word':
            x_train, y_train, x_test, y_test = word_process(train_texts, train_labels, test_texts, test_labels,dataset)
        elif args.level == 'char':
            x_train, y_train, x_test, y_test = char_process(train_texts, train_labels, test_texts, test_labels,dataset)
    # Select the model and load the trained weights
    
    model = None
    if args.model == "word_cnn":
        model = word_cnn(dataset)
    elif args.model == "word_bdlstm":
        model = bd_lstm(dataset)
    elif args.model == "char_cnn":
        model = char_cnn(dataset)
    elif args.model == "word_lstm":
        model = lstm(dataset)
    model_path = r'./runs/{}/{}.dat'.format(dataset, args.model)
    model.load_weights(model_path)
    print('model path:', model_path)

    #evaluate classification accuracy of model on clean samples

    print("clean samples labels:",test_labels)
    scores_origin = model.evaluate(x_test, y_test)
    pred_label = np.argmax(model.predict(x_test),axis=1)
    print("clean samples prelabels:",pred_label)
    print('clean samples origin test_loss: %f, accuracy: %f' % (scores_origin[0], scores_origin[1]))


    # evaluate classification accuracy of model on adversarial examples
    adv_text_path ='./data/ag/adv.txt'
    # print('adversarial file:', adv_text_path)
    adv_text = read_adversarial_file(adv_text_path)

    clean_def_text_path = './data/ag/clean_def.txt'
    clean_def_text = read_adversarial_file(clean_def_text_path)

    adv_def_text_path = './data/ag/adv_def.txt'
    adv_def_text = read_adversarial_file(adv_def_text_path)

    x_clean = None
    x_adv = None
    x_clean_def = None
    x_adv_def = None
    if args.level == 'word':
        # x_clean = text_to_vector_for_all(clean_text,tokenizer,dataset)
        x_adv = text_to_vector_for_all(adv_text, tokenizer, dataset)
        x_clean_def = text_to_vector_for_all(clean_def_text, tokenizer, dataset)
        x_adv_def = text_to_vector_for_all(adv_def_text, tokenizer, dataset)
    elif args.level == 'char':
        x_adv = doc_process_for_all(adv_text, get_embedding_dict(), dataset)
        x_clean_def = doc_process_for_all(clean_adv_text, get_embedding_dict(), dataset)
        x_adv_def = doc_process_for_all(adv_def_text, get_embedding_dict(), dataset)
    

    score_adv = model.evaluate(x_adv[:1000], y_test[:1000])
    adv_label = np.argmax(model.predict(x_adv[:1000]),axis=1)
    print('adv test_loss: %f, accuracy: %f' % (score_adv[0], score_adv[1]))

    score_clean_def = model.evaluate(x_clean_def[:1000], y_test[:1000])
    clean_def_label = np.argmax(model.predict(x_clean_def[:1000]),axis=1)
    print('clean_def test_loss: %f, accuracy: %f' % (score_clean_def[0], score_clean_def[1]))

    score_adv_def = model.evaluate(x_adv_def[:1000], y_test[:1000])
    adv_def_label = np.argmax(model.predict(x_adv_def[:1000]),axis=1)
    print('adv_def test_loss: %f, accuracy: %f' % (score_adv_def[0], score_adv_def[1]))
