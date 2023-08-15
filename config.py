class Config(object):
    num_classes = {'imdb': 2, 'yahoo': 10, 'agnews': 4, 'sst': 2, 'toxic':2,'enron':2}
    word_max_len = {'imdb': 500, 'yahoo': 1000, 'agnews': 300, 'sst': 100, 'toxic':300,'enron':800}
    char_max_len = {'agnews': 1014}
    num_words = {'imdb': 20000, 'yahoo': 20000, 'agnews': 5000, 'sst': 5000, 'toxic':40000,'enron':40000}

    wordCNN_batch_size = {'imdb': 32, 'yahoo': 32, 'agnews': 32, 'sst': 32, 'toxic':32,'enron':32}
    wordCNN_epochs = {'imdb': 2, 'yahoo': 6, 'agnews': 32, 'sst':15, 'toxic':15,'enron':15}

    bdLSTM_batch_size = {'imdb': 128, 'yahoo': 32, 'agnews': 128, 'sst':32, 'toxic':128,'enron':128}
    bdLSTM_epochs = {'imdb': 15, 'yahoo': 16, 'agnews': 15, 'sst':10, 'toxic':10,'enron':10}

    charCNN_batch_size = {'agnews': 128}
    charCNN_epochs = {'agnews': 4}

    LSTM_batch_size = {'imdb': 32, 'agnews': 64, 'sst':32, 'toxic':128,'enron':128}
    LSTM_epochs = {'imdb': 30, 'agnews': 30, 'sst':30, 'toxic':10,'enron':102}

    loss = {'imdb': 'binary_crossentropy', 'yahoo': 'categorical_crossentropy', 'agnews': 'categorical_crossentropy', 'sst':'binary_crossentropy', 'toxic':'binary_crossentropy','enron':'binary_crossentropy'}
    activation = {'imdb': 'sigmoid', 'yahoo': 'softmax', 'agnews': 'softmax', 'sst':'sigmoid', 'toxic':'sigmoid','enron':'sigmoid'}

    wordCNN_embedding_dims = {'imdb': 300, 'yahoo': 50, 'agnews': 300, 'sst':300, 'toxic':300,'enron':300}
    bdLSTM_embedding_dims = {'imdb': 300, 'yahoo': 128, 'agnews': 300, 'sst':128, 'toxic':300,'enron':300}
    LSTM_embedding_dims = {'imdb': 100, 'agnews': 100, 'sst':100, 'toxic':100,'enron':100}


config = Config()
