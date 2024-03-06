import os
import re
import math
from collections import defaultdict
from bs4 import BeautifulSoup

folder_path = '/Users/unterlantas/PycharmProjects/infosearch/task1/downloaded_pages'
output_folder = '/Users/unterlantas/PycharmProjects/infosearch/task4/tf_idf'

# Функция для очистки текста и извлечения слов
def clean_and_extract_words(text):
    cleaned_text = re.sub(r'[^а-яА-Я\s]', '', text)
    cleaned_text = cleaned_text.lower()
    words = cleaned_text.split()
    return words

# Загрузка списка терминов из файла
def load_terms(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

# Загрузка лемм из файла
def load_lemmas(file_path):
    lemmas = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            lemma_forms = line.strip().split()
            base_form = lemma_forms[0]
            for form in lemma_forms:
                lemmas[form] = base_form
    return lemmas

# Извлечение текста из HTML файла и преобразование в леммы
def extract_text_and_lemmatize(file_path, lemmas):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        text = soup.get_text(separator=' ', strip=True).lower()
        words = clean_and_extract_words(text)
        lemmatized_words = [lemmas.get(word, word) for word in words]
        return words, lemmatized_words

# Расчет TF и IDF
def calculate_tf_idf(document_words, corpus_documents, lemmas):
    tf = defaultdict(float)
    idf = defaultdict(float)
    tf_idf = defaultdict(float)

    # TF для документа
    total_words = len(document_words)
    word_counts = defaultdict(int)
    for word in document_words:
        word_counts[word] += 1

    # TF и IDF для терминов и лемм
    for word, count in word_counts.items():
        tf[word] = count / total_words
        lemma = lemmas.get(word, word)
        docs_with_word = sum(1 for doc in corpus_documents if lemma in doc)
        idf[word] = math.log(len(corpus_documents) / (1 + docs_with_word))
        tf_idf[word] = tf[word] * idf[word]

    return tf, idf, tf_idf

# Главная функция
def main():
    tokens = load_terms('/Users/unterlantas/PycharmProjects/infosearch/task2/tokens.txt')
    lemmas = load_lemmas('/Users/unterlantas/PycharmProjects/infosearch/task2/lemmas.txt')
    documents = []
    corpus_lemmatized = []

    # Чтение и обработка HTML файлов
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            document_words, lemmatized_words = extract_text_and_lemmatize(file_path, lemmas)
            documents.append(document_words)
            corpus_lemmatized.append(' '.join(lemmatized_words))

    # Расчет TF, IDF и TF-IDF для каждого документа и запись результатов
    for i, (doc_words, lemmatized_text) in enumerate(zip(documents, corpus_lemmatized)):
        tf, idf, tf_idf = calculate_tf_idf(doc_words, corpus_lemmatized, lemmas)
        output_file_path = os.path.join(output_folder, f'doc_{i+1}_tf_idf.txt')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for word, tf_idf_value in tf_idf.items():
                if word in tokens or word in lemmas:
                    f.write(f"{word} {idf[word]} {tf_idf_value}\n")

if __name__ == "__main__":
    main()