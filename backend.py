import logging
import spacy
from fastapi import FastAPI
import json

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the FastAPI app instance
app = FastAPI()

# Load the pre-trained NLP model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Load image descriptions from JSON
with open("image_data.json", "r") as file:
    image_data = json.load(file)

@app.get("/")
def read_root():
    return {"message": "Welcome to AurumAI Backend!"}

@app.get("/predict/")
def predict_image(prompt: str):
    """Matches the prompt with the most relevant image based on keywords."""
    
    # Process the prompt using NLP
    doc = nlp(prompt.lower())  
    prompt_keywords = {token.lemma_ for token in doc if token.is_alpha and not token.is_stop}  # Extract meaningful words
    
    logging.info(f"Prompt Keywords: {prompt_keywords}")  # Log the keywords extracted from the prompt

    best_match = None
    max_match_count = 0

    # Iterate through images to find the best match
    for filename, keywords in image_data.items():
        image_keywords = {keyword.lower() for keyword in keywords}  # Convert image keywords to lowercase
        match_count = len(prompt_keywords & image_keywords)  # Count common words
        
        logging.info(f"Comparing with Image: {filename}, Image Keywords: {image_keywords}, Match Count: {match_count}")  # Log comparison details
        
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = filename

    return {"selected_image": best_match if best_match else "No match found"}




