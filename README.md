# CT200 AI Backend

AI-powered backend for generating QA test cases from technical PDF documentation.

## Features

- Upload and parse PDF documents
- Reconstruct document hierarchy
- Store parsed nodes in SQLite
- Search and browse document content
- Create reusable node selections
- Generate QA test cases using Google Gemini
- Cache generated outputs in MongoDB
- Detect stale generations after document updates

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- MongoDB Atlas
- Google Gemini API
- Pydantic

---

## Project Structure

```
app/
├── core/
├── database.py
├── database_mongo.py
├── models/
├── routes/
├── schemas/
├── services/
└── main.py
```

---

## Installation

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Windows

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
MONGODB_URI=YOUR_MONGODB_CONNECTION_STRING
```

---

## Run

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## API Workflow

1. Upload PDF
2. Parse and store document
3. Browse/Search nodes
4. Create Selection
5. Generate Test Cases
6. Cached generations stored in MongoDB
7. Retrieve generation
8. Check staleness

---

## Generation Pipeline

```
PDF
    ↓
Parser
    ↓
Hierarchy Builder
    ↓
SQLite
    ↓
Selection
    ↓
Prompt Builder
    ↓
Gemini
    ↓
JSON Validation
    ↓
MongoDB
```

---

## Cache Strategy

A SHA-256 hash of all selected node hashes is generated.

If the same selection hash and prompt version already exist, the cached generation is returned instead of invoking Gemini.

---

## Staleness Detection

Stored node hashes are compared against current node hashes.

Possible statuses:

- CURRENT
- STALE

---

## Author

Rithesh R
