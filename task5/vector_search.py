import os
import math
from bs4 import BeautifulSoup

html_dir = '/Users/unterlantas/PycharmProjects/infosearch/task1/downloaded_pages'
tfidf_dir = '/Users/unterlantas/PycharmProjects/infosearch/task4/tokens_tf_idf'


def calculate_cosine_similarity(vector1, vector2):
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(v ** 2 for v in vector1))
    magnitude2 = math.sqrt(sum(v ** 2 for v in vector2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


def read_tfidf_file(file_path):
    tfidf_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            tfidf_dict[parts[0]] = float(parts[2])
    return tfidf_dict


def get_page_title(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip()
        else:
            return None


def search(query):
    query_tokens = query.split()
    query_tfidf_vector = [0] * len(query_tokens)

    for i, token in enumerate(query_tokens):
        query_tfidf_vector[i] = 1

    similarities = []

    for file_name in os.listdir(tfidf_dir):
        if not file_name.endswith('.txt'):
            continue
        try:
            doc_number = int(file_name.split('.')[0])
        except ValueError:
            continue
        html_file_path = os.path.join(html_dir, f"{doc_number}.html")
        title = get_page_title(html_file_path)
        if title is None:
            continue
        tfidf_file_path = os.path.join(tfidf_dir, file_name)
        document_tfidf = read_tfidf_file(tfidf_file_path)

        document_tfidf_vector = [document_tfidf.get(token, 0) for token in query_tokens]

        similarity = calculate_cosine_similarity(query_tfidf_vector, document_tfidf_vector)

        if similarity != 0:
            similarities.append((doc_number, title, similarity))  # Добавляем номер страницы в список пар

        similarities.sort(key=lambda x: x[2], reverse=True)

    return similarities


if __name__ == "__main__":
    query = input("Введите поисковый запрос: ")
    search_results = search(query)

    for doc_number, title, similarity in search_results:
        print(f"{doc_number}. {title}. Индекс сходства: {similarity:.5f}")
