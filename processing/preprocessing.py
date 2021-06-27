from helpers import remove_newline, strip_links, uncapitalize, expand_abbr, remove_punctuation, remove_stopwords

def overall_cleantext(telegram_message):
    telegram_message = remove_newline(telegram_message)
    telegram_message = strip_links(telegram_message)
    telegram_message = uncapitalize(telegram_message)
    telegram_message = expand_abbr(telegram_message)
    telegram_message = remove_punctuation(telegram_message)
    telegram_message = remove_stopwords(telegram_message)
    loaded_tokenizer_model = pickle.load(open(tokenizer_file, 'rb'))
    telegram_message = loaded_tokenizer_model.texts_to_sequences([test_text])
    telegram_message = pad_sequences(telegram_message, padding = 'post', maxlen = MAX_SEQUENCE_LENGTH)
    return telegram_message