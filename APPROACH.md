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