# U of T Navigator 🎓
**An Intelligent, Transformer-Powered Alternative to U of T's "Navi"**

[![Status](https://img.shields.io/badge/Status-In_Development-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)]()

## 🚀 The Vision
U of T's current chatbot (Navi) relies on legacy rule-based logic. The **U of T Navigator** uses a modern RAG (Retrieval-Augmented Generation) pipeline to crawl official university subdomains and provide verifiable, cited answers to student inquiries about scholarships, counseling, and registrar policies.

## 🛠️ Tech Stack
- **Ingestion:** `Crawl4AI` (Optimized for LLM-ready Markdown extraction)
- **Orchestration:** `LlamaIndex` (Semantic data indexing & retrieval)
- **Vector DB:** `ChromaDB` (Local vector storage)
- **Brain:** `DeepSeek-V3` / `GPT-4o-mini` via OpenRouter
- **OS:** Developed on Ubuntu Linux

## 🏗️ Architecture
1. **Scrape:** Recursively crawl `*.utoronto.ca` for fresh data.
2. **Embed:** Convert information into high-dimensional vectors.
3. **Query:** Match student intent with official university context.
4. **Cite:** Every answer includes a direct link to the source website.

## 🏃 Getting Started (Ubuntu)
```bash
git clone git@github.com:yourusername/uoft-navigator.git
cd uoft-navigator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium