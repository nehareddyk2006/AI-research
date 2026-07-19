# 🧠 ResearchWeaver AI

> Transform research papers into interactive knowledge using AI.

ResearchWeaver AI is an intelligent research assistant that helps researchers, students, and professionals understand academic papers faster. Upload any research paper in PDF format to generate AI-powered summaries, visualize knowledge graphs, identify research gaps, plan follow-up experiments, and chat with the paper using Retrieval-Augmented Generation (RAG).

---

## 🌐 Live Demo

🔗 **Live Application:** https://ai-research-weaver-platform.streamlit.app/

📂 **GitHub Repository:** https://github.com/nehareddyk2006/AI-research

---

## ✨ Features

### 📄 PDF Analysis
- Upload research papers in PDF format
- Extract title, authors, journal, abstract, keywords, and metadata
- Estimate reading time and word count

### 🤖 AI Paper Analysis
Generate structured insights including:
- Executive Summary
- Research Problem
- Methodology
- Datasets
- Models
- Evaluation Metrics
- Limitations
- Future Work

### 🕸️ Knowledge Graph
Visualize relationships between important concepts, entities, and ideas extracted from the paper.

### 🔍 Research Gap Detection
Automatically identify:
- Research gaps
- Possible future directions
- Difficulty level for exploring each gap

### 🧪 Experiment Planner
Generate AI-powered experiment suggestions including:
- Objectives
- Recommended datasets
- Proposed models
- Preprocessing steps
- Baseline models
- Evaluation metrics
- Expected outcomes

### 💬 Chat with Your Paper
Powered by Retrieval-Augmented Generation (RAG):
- Semantic search using FAISS
- Hugging Face embeddings
- Context-aware AI responses
- Intelligent inferences when explicit answers are unavailable

---

# 🏗️ Architecture

```text
                    PDF Upload
                         │
                         ▼
                 PyMuPDF Extraction
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
   AI Analysis                     Text Chunking
 (Google Gemini)                        │
         │                              ▼
         │                     HuggingFace Embeddings
         │                              │
         ▼                              ▼
 Knowledge Graph                  FAISS Vector Store
 Research Gaps                          │
 Experiment Plan                        ▼
         │                     Retrieval-Augmented
         └──────────────►      Chat Assistant
```

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### AI
- Google Gemini 3.1 Flash Lite

### RAG
- LangChain
- FAISS
- Hugging Face Embeddings
- Sentence Transformers

### PDF Processing
- PyMuPDF

### Visualization
- PyVis
- NetworkX

### Backend
- Python

---

# 📸 Screenshots

> Add screenshots after deployment.

Suggested screenshots:

- Landing Page
- AI Analysis
- Knowledge Graph
- Research Gap Finder
- Experiment Planner
- Chat Interface

Example:

```
assets/
│── home.png
│── analysis.png
│── graph.png
│── gaps.png
│── planner.png
│── chat.png
```

Then include:

```md
## Home

![Home](assets/home.png)

## Knowledge Graph

![Graph](assets/graph.png)
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/nehareddyk2006/AI-research.git
```

Move into the project

```bash
cd AI-research
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_MODEL=gemini-3.1-flash-lite
```

Run the application

```bash
streamlit run app.py
```

---

# 📂 Project Structure

```text
AI-research
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│
├── src/
│   ├── ai/
│   ├── extraction/
│   ├── graphs/
│   └── rag/
│
└── data/
```

---

# 💡 Future Enhancements

- Multi-paper comparison
- Literature review generation
- Citation graph visualization
- PDF & Markdown export
- Research notebook
- Related paper recommendations
- Cloud database support
- User authentication
- Collaboration workspace

---

# 👨‍💻 Author

**Neha Reddy**

GitHub:
https://github.com/nehareddyk2006

LinkedIn:
https://www.linkedin.com/in/kondam-neha-reddy-103476264/

---

# 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub.