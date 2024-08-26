
# FastAPi app for matching in 2 text

This FastApi application is written in order to take 2 files, run them through the ner spaCy model and output two lists: matched and unmatched


## API Endpont

```POST /upload_and_compare```

This endpoint accepts two file uploads (vacancy for job description and resume for resume) and compares the extracted text using named entity recognition.


## Technologies  used 

- Python
- FastAPI
- PyMuPDF (for PDF processing)
- python-docx (for DOCX processing)
- spaCy (for natural language processing)
- Docker
## Installation

Pip Install command

```python
pip install fastapi uvicorn scikit-learn python-multipart python-docx PyMuPDF spacy
```
or 
```python
pip install -r requirements.txt
```
## Usage

```python
python main.py #starting the server

curl -F "vacancy=@path/to/file.docx" -F "resume=@path/to/file.docx" http://127.0.0.1:8000/compare #console command with endpoint "compare"
```


## Example

Input

```python
python main.py #run server 

curl -F "vacancy=@E:/eng/content/IT_vacancies_cut.docx" -F "resume=@E:/eng/content/hh_ru.cut.docx" http://127.0.0.1:8000/upload_and_compare #console command with links to the necessary files

```

Output

```python
{"matched":["PHP","UX"],"unmatched":["UI Designer","Python","True","Angular","CSS","JS","Pride","SQL","Node.js","PostgreSQL","1С\nTrue","Adobe Illustrator","'","SEO","MySQL","140000.0","Grid Dynamics\nFull","1С: Предприятие 8","1С","48813842","34800.0","Baker","Django Framework","73950.0","Space307","CRM","Golang","Redis","80000.0","Docker","Linux","Photoshop","30000.0","Nginx","70000.0","Nagios","Google AdWords","Git","150000.0","Analytics","HTML","UI","Zenon"]}
```
# How to build Docker image

run this command from the project folder:
```docker build -t hr_match_v1 .```
