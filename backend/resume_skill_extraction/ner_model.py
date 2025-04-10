from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification
import re


def reconstruct_bio_entities(entities, min_score=0.8):
    skills = []
    current_phrase = []

    for ent in entities:
        word = ent["word"]
        label = ent["entity_group"]
        score = ent["score"]

        # Skip low confidence tokens
        if score < min_score:
            continue

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

def ner_model(text):    
    ner = pipeline("ner", model="jjzha/jobbert_knowledge_extraction", grouped_entities=True)
    
    print(text)
    results = ner(text)
    print(results)

    skills = reconstruct_bio_entities(results)

    print(" Extracted Skills/Knowledge:")
    for skill in skills:
        print("-", skill)


def ner_advance_model(text):

    model_id = "jjzha/jobbert_knowledge_extraction"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model1 = AutoModelForTokenClassification.from_pretrained(model_id)

    ner = pipeline("ner", model=model1, tokenizer=tokenizer, grouped_entities=True)

    entities = extract_all_skills(text, ner, tokenizer)
    skills = reconstruct_bio_entities(entities)

    print(" Extracted Skills/Knowledge:")
    for skill in skills:
        print("-", skill)

def extract_all_skills(text, ner, tokenizer):
    all_entities = []
    for chunk in split_text_by_token_limit(text, tokenizer):
        try:
            entities = ner(chunk)
            all_entities.extend(entities)
        except RuntimeError as e:
            print(f"Skipping chunk due to error: {e}")
    return all_entities

def split_text_by_token_limit(text, tokenizer, max_tokens=510):
    words = text.split()
    print("\nwords")
    print(words)
    chunks = []
    current_chunk = []

    for word in words:
        # Estimate token count
        token_count = len(tokenizer.tokenize(" ".join(current_chunk + [word])))
        if token_count <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    print("\nchunks")
    print(chunks)
    print("\n")

    for ch in chunks:
        print("----------")
        print(ch)
        print("\n")

    return chunks


if __name__ == "__main__":
    text = """
    SKILLS Spectrix Analytical Services
    Python (NumPy, Pandas,
    Built a customer attrition random forest model that improved
    Scikit-learn, Keras, Flask)
    monthly retention by 12 basis points for clients likely to opt-out
    SQL (MySQL, Postgres)
    by providing relevant product features for them
    Git
    Time Series Forecasting
    Recommendation Engines Partnered with product team to create a production
    Customer Segmentation 
    AWS 
    """
    ner_simple_model(text)
    # ner_advance_model(text)