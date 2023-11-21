import os
import joblib

# Function to load knowledge from joblib files in a folder
def load_knowledge_from_folder(folder_path):
    knowledge = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".joblib"):
            file_path = os.path.join(folder_path, filename)
            key = os.path.splitext(filename)[0]  # Use the filename (without extension) as the key
            knowledge[key] = joblib.load(file_path)
    return knowledge

# Function to respond to user messages using the loaded knowledge
def respond_to_user_message(user_message, knowledge):
    # Check if user_message corresponds to any key in the knowledge
    if user_message in knowledge:
        return knowledge[user_message]
    else:
        return "I'm sorry, I don't have information about that."

# Example usage
if __name__ == "__main__":
    # Replace 'path/to/your/knowledge/folder' with the actual path to your knowledge folder
    knowledge_folder_path = './trained_models/'

    # Load knowledge from joblib files in the specified folder
    loaded_knowledge = load_knowledge_from_folder(knowledge_folder_path)

    # Get user input
    user_input = input("Enter your message: ")

    # Respond to the user's message using the loaded knowledge
    response = respond_to_user_message(user_input, loaded_knowledge)

    # Display the response
    print("Response:", response)
