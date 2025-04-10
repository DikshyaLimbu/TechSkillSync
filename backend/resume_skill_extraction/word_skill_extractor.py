import docx
from transformers import pipeline

SKILL_KEYWORDS = [
    "skills", "technical skills", "core competencies",
    "technologies", "tools", "expertise", "proficiencies",
    "it skills", "additional skills"
]

file = "data-engineer-resume.docx"
file_path = f"data/sample_resumes/{file}"



def get_text():
    lines = word_parser(file_path)
    return "\n".join(lines)

def get_skills():
    data = word_parser(file_path)
    text = find_skill_section(data)
    ner_model(text)

def word_parser(file_path):
    doc = docx.Document(file_path)

    lines = []

    paragraph_count = len([p for p in doc.paragraphs if p.text.strip()])
    table_count = len(doc.tables)

    # Paragraphs
    if paragraph_count:
        print("Parsing from paragraph.")
        for para in doc.paragraphs:
            print(para.text)
            if para.text.strip():
                lines.append(para.text.strip())
    
    # Tables
    if table_count:
        print("Parsing from table.\n")
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        lines.append(cell_text)
    return lines

def find_skill_section(lines):
    max_lines = 20
    skills_text = []
    capture_skills_section =False
    for line in lines:
        if line.lower() in SKILL_KEYWORDS:
            capture_skills_section = True

        if capture_skills_section:
            skills_text.append(line)
        
        if len(skills_text) > max_lines:
            break

    text = "\n".join(skills_text)
    # print(text)

    return text

def ner_model(text):
    ner = pipeline("ner", model="jjzha/jobbert_knowledge_extraction", grouped_entities=True)

    print(text)
    results = ner(text)
    print(results)


    skills = reconstruct_bio_entities(results)

    print(" Extracted Skills/Knowledge:")
    for skill in skills:
        print("-", skill)


def reconstruct_bio_entities(entities):
    skills = []
    current_phrase = []

    for ent in entities:
        word = ent["word"]
        label = ent["entity_group"]

        # Handle subword tokens (e.g., ##s)
        if word.startswith("##"):
            word = word[2:]
            if current_phrase:
                current_phrase[-1] += word
            continue

        if label == "B":
            if current_phrase:
                skills.append(" ".join(current_phrase))
            current_phrase = [word]
        elif label == "I":
            current_phrase.append(word)
            
    # Append the last phrase
    if current_phrase:
        skills.append(" ".join(current_phrase))

    return list(set(skills))  # Remove duplicates
    
    
if __name__ == "__main__":
    get_skills()



    




 


