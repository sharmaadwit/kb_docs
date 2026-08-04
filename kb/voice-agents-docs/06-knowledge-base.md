---
title: Knowledge Base
description: RAG configuration, document upload, and retrieval settings
source: https://voiceagents.gupshup.io/developer-docs
---

# Knowledge Base

## Knowledge Base Tab

The Knowledge Base tab enables Retrieval-Augmented Generation (RAG), allowing agents to ground their responses in organisational documents. Uploaded files are indexed and queried in real time during conversations.

### Key Actions

| Action | Description |
|---|---|
| Configure RAG | Opens RAG configuration: chunking strategy, embedding model, and retrieval parameters |
| Add Document (dropdown) | Upload documents to the knowledge base. Supports PDF, plain text, Markdown, and other common formats |
| Search Knowledge Base... | Full-text search across all uploaded documents within the agent |
| \+ Type / + Creator filters | Filter the document list by file type or the user who uploaded the document |

### Configuration Procedure

  * Click Add Document and select the relevant file(s) from your local system

  * Allow the system to index the uploaded documents

  * Click Configure RAG to adjust retrieval parameters including chunk size, embedding model, and similarity threshold

  * The agent will reference these documents in real time to provide accurate, grounded responses

> ℹ NOTE For optimal RAG performance, upload well-structured documents (PDFs with clear headings, formatted FAQs). Configure the chunking strategy to match your document type — smaller chunks improve precision for Q&A workloads.
