# Approach

## Overview

The backend converts technical PDF documents into structured QA test cases using a retrieval and generation pipeline.

## Architecture

1. Parse uploaded PDF into hierarchical nodes.
2. Store nodes and document metadata in SQLite.
3. Allow users to browse, search, and create selections.
4. Reconstruct the selected document content.
5. Generate a prompt from the reconstructed text.
6. Send the prompt to Google Gemini.
7. Validate the returned JSON structure.
8. Store the generation and metadata in MongoDB.
9. Return cached generations when an identical selection is requested.
10. Detect stale generations by comparing stored node hashes with current node hashes.

## Design Decisions

- SQLite stores structured document metadata and relationships.
- MongoDB stores generated test cases because generation documents are semi-structured.
- SHA-256 hashes uniquely identify document content and selections.
- Prompt versioning allows future prompt improvements without invalidating historical generations.
- JSON validation ensures all LLM responses conform to the expected schema before storage.

## Generation Flow

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
Validation
 ↓
MongoDB
```
# Decision Log

## 1. Which part of the system is most likely to silently produce incorrect results?

The hierarchy reconstruction stage is the most likely component to silently produce incorrect results. If a heading is incorrectly classified or attached to the wrong parent, every downstream feature—including browsing, selections, version matching, and QA generation—continues to function without raising an error, but operates on an incorrect document structure.

To reduce this risk, I manually inspected the parsed hierarchy, compared it with the original PDF, and added unit tests covering duplicate headings, hierarchy reconstruction, and heading classification. During development I also logged intermediate parsing results to validate parent-child relationships before storing them in the database.

---

## 2. Where did you choose simplicity over correctness because of time?

For document versioning, I primarily relied on content hashing and document structure rather than implementing semantic similarity matching. This approach is deterministic, simple to maintain, and efficient for the provided documents, but it can incorrectly classify logically identical sections as changed when only wording or formatting differs.

In a production system I would combine hashing with semantic embeddings or fuzzy matching to better identify logically unchanged content across document versions.

---

## 3. Name one input your system does not currently handle.

The parser is designed specifically for the CT-200 manuals and does not fully support arbitrary PDF layouts containing complex multi-column pages, floating figures, or nested tables.

When unsupported layouts are encountered, the parser preserves the extracted text whenever possible but may not perfectly reconstruct the document hierarchy. This limitation is documented rather than silently ignored so that incorrect structural reconstruction can be identified during validation.