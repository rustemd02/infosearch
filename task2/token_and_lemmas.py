import os
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text

def clean_and_tokenize(text, stop_words):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if re.fullmatch(r'[а-яё]+', token) and token not in stop_words]
    return tokens

def lemmatize(tokens, morph):
    lemmas = [morph.parse(token)[0].normal_form for token in tokens]
    return lemmas

def process_files(directory, morph, stop_words):
    all_tokens = set()
    lemmas_dict = {}

    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_html(file_path)
            tokens = clean_and_tokenize(text, stop_words)
            all_tokens.update(tokens)
            lemmas = lemmatize(tokens, morph)
            for lemma, original in zip(lemmas, tokens):
                if lemma in lemmas_dict:
                    lemmas_dict[lemma].add(original)
                else:
                    lemmas_dict[lemma] = {original}

    with open('tokens.txt', 'w', encoding='utf-8') as f:
        for token in sorted(all_tokens):
            f.write(f"{token}\n")

    with open('lemmas.txt', 'w', encoding='utf-8') as f:
        for lemma, original_tokens in sorted(lemmas_dict.items()):
            f.write(f"{lemma} {' '.join(sorted(original_tokens))}\n")

if __name__ == '__main__':
    nltk.download('punkt')
    nltk.download('stopwords')
    morph = pymorphy2.MorphAnalyzer()
    stop_words = set(stopwords.words('russian'))
    directory_path = '/Users/unterlantas/PycharmProjects/infosearch/task1/downloaded_pages'
    process_files(directory_path, morph, stop_words)