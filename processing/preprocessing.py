from helpers import remove_newline, strip_links, uncapitalize, expand_abbr, remove_punctuation, remove_stopwords

def overall_cleantext(telegram_message):
    telegram_message = remove_newline(telegram_message)
    telegram_message = strip_links(telegram_message)
    telegram_message = uncapitalize(telegram_message)
    telegram_message = expand_abbr(telegram_message)
    telegram_message = remove_punctuation(telegram_message)
    telegram_message = remove_stopwords(telegram_message)