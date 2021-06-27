# Remove newlines
def remove_newline(text):
    return text.replace("\n", " ")

# Remove URLs
def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

#uncapitalize text
def uncapitalize(text):
    return text.lower()

#Expand abbreviations
def expand_abbr(text):
    new_text = text
    for item in contraction_map:
        if item in text:
            new_text = new_text.replace(item,contraction_map[item])
    return new_text

#Remove punctuations
def remove_punctuation(text):
    for punctuation_token in all_punctuation:
        text = text.replace(punctuation_token,"")
    return text

#Remove stopwords
def remove_stopwords(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stop_words]
    return tokens_without_sw

def get_word_embeddings(text):
    sentence_vectors = np.zeros((100,))
    if len(text)==0:
        return sentence_vectors
    for i in text:
        if i in word_embeddings:
            sentence_vectors += word_embeddings[i]
        else:
            sentence_vectors += np.zeros((100,))
    sentence_vectors = sentence_vectors/len(text)
    return sentence_vectors