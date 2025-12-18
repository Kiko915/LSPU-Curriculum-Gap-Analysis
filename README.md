# DheKode: Predictive Industry Skill Analysis System

[![SDG 4: Quality Education](https://img.shields.io/badge/SDG-4_Quality_Education-C5192D?style=for-the-badge)](https://sdgs.un.org/goals/goal4)
[![SDG 8: Decent Work](https://img.shields.io/badge/SDG-8_Decent_Work-A21942?style=for-the-badge)](https://sdgs.un.org/goals/goal8)
[![Status](https://img.shields.io/badge/Status-Development-yellow?style=for-the-badge)]()

**DheKode** is a thesis project designed to bridge the "skills gap" between the academe and the IT industry. It uses Machine Learning and Knowledge Graphs to dynamically assess how well the **LSPU-SCC Computer Studies curriculum** aligns with real-time job market demands.

---

## 📄 Project Overview
There is often a mismatch between the skills taught in universities and the fast-evolving demands of the tech industry. This project aims to solve that by:
1.  **Predicting** the most relevant job roles for a given curriculum using Machine Learning.
2.  **Identifying** specific skill gaps using a semantic Knowledge Graph.
3.  **Recommending** actionable curriculum updates for faculty and upskilling paths for students.

## 🚀 Key Features
* **Curriculum Parser:** Automated extraction of skills and topics from PDF course syllabi using NLP (spaCy).
* **Industry Knowledge Graph:** A network-based model (NetworkX) that maps relationships between skills (e.g., *Python* → *Data Science*), allowing for semantic gap analysis rather than simple keyword matching.
* **Job Role Classifier:** An ML model that predicts which industry roles (e.g., "Full Stack Dev", "QA Engineer") a curriculum is best suited for.
* **Interactive Dashboard:** A React-based visualization allowing users to explore the "Skill Graph" and view match percentages.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Frontend** | React (Vite), Tailwind CSS, React-Force-Graph |
| **Backend** | FastAPI (Python), Uvicorn |
| **Data Science** | Pandas, Scikit-learn, NetworkX, SpaCy |
| **Data Sources** | Synthetic Job Data (Kaggle), LSPU Curriculum PDFs |

## 📂 Project Structure
```text
DheKode/
├── data/                 # Raw datasets and processed JSONs
├── notebooks/            # Jupyter notebooks for EDA and Model Testing
├── scripts/              # Standalone ETL scripts (Graph builder, Scraper)
├── backend/              # FastAPI Server & ML Logic
│   ├── ml_engine/        # The Core Logic (Graph + Model)
│   └── routers/          # API Endpoints
└── frontend/             # React Application
