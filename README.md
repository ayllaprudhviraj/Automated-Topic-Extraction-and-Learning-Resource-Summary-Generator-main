# Automated Topic Extraction & Learning Resource Summary Generator

An AI-powered lecture assistant and study hub that extracts key conceptual topics from lecture slides and documents (`.pdf`, `.pptx`), retrieves verified educational articles and YouTube tutorials, generates active-recall quizzes and flashcards, and provides an interactive conversational AI tutor.

---

## ✨ Features

- **📄 Document Processing**: Instant parsing of `.pdf` and `.pptx` lecture presentations using PyMuPDF and python-pptx.
- **🧠 KeyBERT Topic Extraction**: High-precision topic extraction using Maximal Marginal Relevance (MMR) and academic stopword filters.
- **🔍 Curated Learning Resources**: Automated discovery of high-quality educational articles via SerpApi.
- **🎥 YouTube Video Tutorials**: Direct retrieval of video explanations and lectures for every extracted concept.
- **📝 Resilient Concept Summaries**: Extraction and summarization with automatic Wikipedia API failover.
- **⚡ Interactive AI Lecture Assistant**: Powered by Groq LLM (`openai/gpt-oss-120b`) for lightning-fast Q&A on your uploaded lecture content.
- **💡 Active Recall Quizzes & Flashcards**: Auto-generated practice questions and answer keys to test retention.
- **🎨 Modern Dark UI**: Responsive, clean interface built with Gradio.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [Git](https://git-scm.com/)

### 2. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ayllaprudhviraj/Automated-Topic-Extraction-and-Learning-Resource-Summary-Generator.git
   cd Automated-Topic-Extraction-and-Learning-Resource-Summary-Generator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r Automated-Topic-Extraction-and-Learning-Resource-Summary-Generator-main/requirements.txt
   ```

4. **Set up API keys**:
   Copy `.env.example` to `.env` inside `Automated-Topic-Extraction-and-Learning-Resource-Summary-Generator-main/.env`:
   ```env
   SERPAPI_API_KEY=your_serpapi_key_here
   GROQ_API_KEY=your_groq_key_here
   ```

### 3. Run the App

- **Using the batch launcher (Windows)**:
  Double-click `run_app.bat` or run in terminal:
  ```bash
  .\run_app.bat
  ```
- **Or directly using Python**:
  ```bash
  python app.py
  ```

Open your browser at: **`http://127.0.0.1:7860`**

---

## 🛠️ Tech Stack

- **Frontend**: [Gradio](https://gradio.app/)
- **Topic Extraction**: [KeyBERT](https://maartengr.github.io/KeyBERT/), Sentence-Transformers, PyTorch
- **NLP**: NLTK, Newspaper3k, Wikipedia API
- **AI / LLM**: [Groq API](https://groq.com/)
- **Search & Multimedia**: [SerpApi](https://serpapi.com/)
