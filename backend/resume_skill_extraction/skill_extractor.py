import pdfplumber
import spacy

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


def extract_resume_skills(pdf_path, skill_list):
    text = extract_text_from_pdf(pdf_path)
    skills_found = extract_skills(text, set(skill_list))
    return skills_found


# Example usage:
if __name__ == "__main__":
    resume_file = "data/sample_resumes/data-scientist-resume-example.pdf"
    skills = extract_resume_skills(resume_file, SKILLS)
    print("Skills Found:", skills)