import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

def load_model(topic):
    # Load the vectorizer and the model
    vectorizer = joblib.load(f'{topic}_vectorizer.joblib')
    model = joblib.load(f'{topic}_model.joblib')
    return vectorizer, model

def predict_topic(user_input, vectorizer, model):
    # Transform user input using the vectorizer
    user_input_vectorized = vectorizer.transform([user_input])

    # Get the feature names from the vectorizer
    feature_names = vectorizer.get_feature_names_out()

    # Find non-zero elements in the transformed vector
    non_zero_indices = user_input_vectorized.nonzero()[1]

    # Map non-zero indices to feature names to get predicted topics
    predicted_topics = [feature_names[i] for i in non_zero_indices]

    return predicted_topics

if __name__ == "__main__":
    user_topic = input("Enter the topic you want to discuss: ")
    
    # Load the model
    vectorizer, model = load_model(user_topic)

    print(f"Bot: Let's talk about {user_topic}! Type 'exit', 'quit', or 'bye' to end the conversation.")

    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Bot: Goodbye!")
            break
        
        # Use the model to predict the topic of the user's input
        predicted_topics = predict_topic(user_input, vectorizer, model)
        
        if predicted_topics:
            print(f"Bot: It seems like you are talking about {', '.join(predicted_topics)}.")
        else:
            print("Bot: I'm not sure about the topic. Can you provide more information?")
