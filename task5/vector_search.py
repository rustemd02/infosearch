import os
import math

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
            tfidf_dict[parts[0]] = float(parts[2])  # токен/лемма: TF-IDF
    return tfidf_dict


def search(query, tfidf_dir):
    """
    Выполняет поиск по TF-IDF для заданного запроса.
    """
    query_tokens = query.split()  # Разбиваем запрос на токены
    query_tfidf_vector = [0] * len(query_tokens)  # Вектор запроса

    # Читаем файлы с TF-IDF и создаем вектор запроса
    for i, token in enumerate(query_tokens):
        query_tfidf_vector[i] = 1  # Просто бинарный вектор запроса

    # Список для хранения пар (номер документа, сходство)
    similarities = []

    # Вычисляем сходство между запросом и каждым документом
    for file_name in os.listdir(tfidf_dir):
        if not file_name.endswith('.txt'):
            continue
        try:
            doc_number = int(file_name.split('.')[0])
        except ValueError:
            continue
        tfidf_file_path = os.path.join(tfidf_dir, file_name)
        document_tfidf = read_tfidf_file(tfidf_file_path)

        document_tfidf_vector = [document_tfidf.get(token, 0) for token in query_tokens]

        similarity = calculate_cosine_similarity(query_tfidf_vector, document_tfidf_vector)

        if similarity != 0:
            similarities.append((doc_number, similarity))

    similarities.sort(key=lambda x: (x[0], x[1]), reverse=False)

    return similarities


if __name__ == "__main__":
    query = input("Введите поисковый запрос: ")
    search_results = search(query, tfidf_dir)

    for doc_number, similarity in search_results:
        print(f"Страница: {doc_number}, индекс сходства: {similarity:.5f}")
