import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_fields(extracted_fields):

    data_path = r'D:\software\Hackathon\Challenge_3\data\data.csv'

    with open(data_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    header = rows[0]
    # Exclude the "Năm" column
    attributes = header[1:]

    # Add extracted_fields to the list of attributes for comparison
    attributes.append(extracted_fields)

    # Compute TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform(attributes)
    vectors = vectorizer.toarray()

    # Compute cosine similarity between the last vector (extracted_fields) and all other vectors
    cosine_similarities = cosine_similarity([vectors[-1]], vectors[:-1])

    # Find the index of the most similar attribute
    most_similar_index = cosine_similarities[0].argmax()

    # Find the name of the most similar attribute
    column_name = header[most_similar_index + 1]

    column_index = header.index(column_name)

    last_row = rows[-1]
    last_row[column_index] = str(int(last_row[column_index]) + 1)

    
    with open(data_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    return header[most_similar_index + 1]  


