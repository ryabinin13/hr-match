from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
import docx
import io
import spacy
import os


app = FastAPI()
vectorizer = TfidfVectorizer()

model_path = os.path.join(os.path.dirname(__file__), "ner_model")
nlp = spacy.load(model_path)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(io.BytesIO(file))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_file(file: UploadFile):
    print(f"Received file with content type: {file.content_type}")
    if file.content_type == "application/pdf" or file.filename.endswith(".pdf"):
        return extract_text_from_pdf(file.file.read())
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file.filename.endswith(".docx"):
        return extract_text_from_docx(file.file.read())
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}, filename: {file.filename}")


def get_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents]

def compare_texts(job_desc, resume):
    job_entities = set(get_entities(job_desc))
    resume_entities = set(get_entities(resume))
    
    # Выделение совпадающих и несовпадающих сущностей
    matched_entities = job_entities & resume_entities
    unmatched_entities = job_entities ^ resume_entities
    
    return list(matched_entities), list(unmatched_entities)

@app.post("/compare")
async def compare_texts_endpoint(vacancy: UploadFile = File(...), resume: UploadFile = File(...)):

    print(f"Vacancy file type: {vacancy.content_type}, filename: {vacancy.filename}")
    print(f"Resume file type: {resume.content_type}, filename: {resume.filename}")

    job_desc_text = extract_text_from_file(vacancy)
    resume_text = extract_text_from_file(resume)
    
    matched, unmatched = compare_texts(job_desc_text, resume_text)
    
    return {
        "matched": matched,
        "unmatched": unmatched
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
