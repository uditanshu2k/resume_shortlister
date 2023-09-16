import os
import re
import csv
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_file):
    try:
        text = extract_text(pdf_file)
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_file}: {str(e)}")
        return ""

if __name__ == "__main__":
    input_directory = "data"
    output_directory = "extract_csv"
    output_csv_filename = "extracted_information.csv"

    # Create a CSV file for output with 'utf-8' encoding
    with open(os.path.join(output_directory, output_csv_filename), mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row
        csv_writer.writerow(["File Name", "Category", "Education", "Skills"])

        # Recursively scan for PDF files in the input_directory and its subfolders
        for root, _, files in os.walk(input_directory):
            for pdf_file in files:
                if pdf_file.endswith(".pdf"):
                    pdf_path = os.path.join(root, pdf_file)
                    extracted_text = extract_text_from_pdf(pdf_path)
                    if extracted_text:
                        # Define regular expressions to extract relevant information
                        name_pattern = r"^(.+)$"  # Assumes the category is in the first line
                        education_pattern = r"Education\n(.+)"  # Assumes education details are under "Education" section
                        skills_pattern = r"Skills\n(.+)"  # Assumes skills are under "Skills" section

                        # Extract information using regular expressions
                        name_match = re.search(name_pattern, extracted_text, re.MULTILINE)
                        education_match = re.search(education_pattern, extracted_text)
                        skills_match = re.search(skills_pattern, extracted_text)

                        # Extracted information
                        if name_match:
                            name = name_match.group(1)
                        else:
                            name = "Category not found"

                        if education_match:
                            education = education_match.group(1).strip()
                        else:
                            education = "Education not found"

                        if skills_match:
                            skills = skills_match.group(1).strip()
                        else:
                            skills = "Skills not found"

                        # Write the extracted information to the CSV file
                        csv_writer.writerow([pdf_file, name, education, skills])

                        print(f"Extracted information from {pdf_file} and saved to CSV.")
