import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def get_wikipedia_content(topic):
    url = f'https://en.wikipedia.org/wiki/{topic.replace(" ", "_")}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    return content

def learn_and_save_model(topic):
    # Get content from Wikipedia
    content = get_wikipedia_content(topic)

    # Vectorize the text using TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([content])

    # Save the vectorizer and the model to joblib files
    vectorizer_filename = f'{topic}_vectorizer.joblib'
    model_filename = f'{topic}_model.joblib'
    joblib.dump(vectorizer, vectorizer_filename)
    joblib.dump(X, model_filename)

if __name__ == "__main__":
    user_topic = input("Enter the topic you want to learn about: ")
    learn_and_save_model(user_topic)
    print(f"Model trained on {user_topic} and saved to '{user_topic}_model.joblib'")
