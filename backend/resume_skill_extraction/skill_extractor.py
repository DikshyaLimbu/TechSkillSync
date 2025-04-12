import pdfplumber
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import re

nlp = spacy.load("en_core_web_sm")

SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data analysis", "sql", "pandas", "numpy", "communication",
    "teamwork", "tensorflow", "keras", "excel", "power bi", "aws"
]


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.lower()


def extract_skills(text, skill_set):
    doc = nlp(text)
    extracted_skills = set()

    # Match single-word and multi-word skills
    for token in doc:
        if token.text.lower() in skill_set:
            extracted_skills.add(token.text.lower())

    for chunk in doc.noun_chunks:
        if chunk.text.lower().strip() in skill_set:
            extracted_skills.add(chunk.text.lower().strip())

    return list(extracted_skills)

#Added by Anjali in order to handle synonyms
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def extract_contextual_skills(text, additional_skills):
    skill_candidates = list(set(SKILLS + additional_skills))
    extracted = []

    for skill in skill_candidates:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            extracted.append(skill.lower())

    return list(set(extracted))


def extract_resume_skills(pdf_path, skill_list):
    text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(text)  # 🧽 Clean the extracted text

    skills_found = extract_skills(cleaned_text, set(skill_list))
    additional_skills_found = extract_contextual_skills(cleaned_text, set(skill_list))

    # Combine both sets of skills if needed
    all_skills = list(set(skills_found + additional_skills_found))
    return all_skills


# Example usage:
if __name__ == "__main__":
    resume_file = "data/sample_resumes/data-scientist-resume-example.pdf"
    skills = extract_resume_skills(resume_file, SKILLS)
    print("Skills Found:", skills)