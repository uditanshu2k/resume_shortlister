import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel
import torch

# Load pre-trained DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

# Load your CSV file containing CV data into a DataFrame
cv_data = pd.read_csv("extract_csv\extracted_information.csv")

# Load your text file containing job descriptions
try:
    with open("job_descriptions.txt", "r", encoding="utf-8") as file:
        job_descriptions = file.readlines()
except UnicodeDecodeError as e:
    print(f"Error reading file: {e}")

# Tokenize and compute embeddings for CVs
cv_embeddings = []

for _, row in cv_data.iterrows():
    cv_text = f"{row['Category']} {row['Skills']} {row['Education']}"
    cv_tokens = tokenizer(cv_text, padding=True, truncation=True, return_tensors="pt")
    cv_embedding = model(**cv_tokens).last_hidden_state.mean(dim=1)
    cv_embeddings.append(cv_embedding)

cv_embeddings = torch.cat(cv_embeddings, dim=0)

# Create a DataFrame to store rankings
rankings = pd.DataFrame(columns=['Job Description', 'CV Index', 'Similarity'])

# Calculate cosine similarity and rank CVs for each job description
for i, job_description in enumerate(job_descriptions):
    # Tokenize the job description
    job_tokens = tokenizer(job_description, padding=True, truncation=True, return_tensors="pt")
    
    # Get embeddings for the job description
    job_embedding = model(**job_tokens).last_hidden_state.mean(dim=1)
    
    # Calculate cosine similarity
    similarities = cosine_similarity(job_embedding.detach().numpy(), cv_embeddings.detach().numpy())
    
    # Get the indices of CVs sorted by similarity (descending order)
    sorted_indices = similarities.argsort()[0][::-1]
    
    # Create a DataFrame for this job description's rankings
    job_rankings = pd.DataFrame({
        'Job Description': [job_description] * len(cv_data),
        'CV Index': sorted_indices,
        'Similarity': similarities[0][sorted_indices]
    })
    
    # Append the top 5 rankings to the main DataFrame
    top_5_rankings = job_rankings.head(5)
    rankings = pd.concat([rankings, top_5_rankings], ignore_index=True)

# Print the top 5 rankings
print(rankings)
