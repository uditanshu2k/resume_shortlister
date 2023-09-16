import pandas as pd

# Replace 'your_dataset.csv' with the actual path to your CSV file.
csv_file_path = 'training_data.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Extract 10-15 job descriptions
num_descriptions_to_fetch = 8  # You can adjust this number as needed

# Assuming that the column containing job descriptions is named 'job_description'
job_descriptions = df['job_description'][:num_descriptions_to_fetch]

# Specify the path for the text file where you want to save the job descriptions.
text_file_path = 'job_descriptions.txt'

# Save the job descriptions to the text file
with open(text_file_path, 'w', encoding='utf-8') as text_file:
    for i, description in enumerate(job_descriptions):
        text_file.write(f"Job Description {i+1}:\n{description}\n\n")

print(f"Job descriptions saved to '{text_file_path}'")
