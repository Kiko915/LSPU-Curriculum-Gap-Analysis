# Deployment Guide

This guide will help you deploy your application for free using **Render** (for the Backend) and **Vercel** (for the Frontend).

## Prerequisites
- A [GitHub](https://github.com/) account.
- Your code pushed to a GitHub repository.

---

## Part 1: Deploying the Backend (FastAPI) on Render

1.  **Sign Up/Log In**: Go to [render.com](https://render.com/) and log in with your GitHub account.
2.  **New Web Service**:
    -   Click the **"New +"** button and select **"Web Service"**.
    -   Select "Build and deploy from a Git repository".
    -   Connect your repository (`ml_finals` or whatever you named it).
3.  **Configure Service**:
    -   **Name**: `ml-finals-backend` (or similar).
    -   **Region**: Choose the one closest to you (e.g., Singapore).
    -   **Branch**: `main` (or `master`).
    -   **Root Directory**: Leave this blank (defaults to project root).
    -   **Runtime**: **Python 3**.
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4.  **Environment Variables**:
    -   Render usually handles the python version, but if needed, add `PYTHON_VERSION` = `3.9.0`.
5.  **Deploy**: Click **"Create Web Service"**.
    -   Wait for the deployment to finish. You will see a green "Live" badge.
    -   **Copy the Backend URL** (e.g., `https://ml-finals-backend.onrender.com`). You will need this for Part 2.

> **Warning**: Your current data persistence uses a JSON file (`student_logs.json`). On free hosting like Render, this file will reset every time the server restarts or you redeploy. For a permanent database, you would need to use a service like MongoDB Atlas or Render's PostgreSQL.

---

## Part 2: Deploying the Frontend (Vite + React) on Vercel

1.  **Sign Up/Log In**: Go to [vercel.com](https://vercel.com/) and log in with GitHub.
2.  **Add New Project**:
    -   Click **"Add New..."** -> **"Project"**.
    -   Import your GitHub repository.
3.  **Configure Project**:
    -   **Framework Preset**: It should auto-detect **Vite**.
    -   **Root Directory**: Click "Edit" and select `frontend`.
4.  **Environment Variables**:
    -   Expand the **"Environment Variables"** section.
    -   Add a new variable:
        -   **Key**: `VITE_API_URL`
        -   **Value**: Paste your **Backend URL** from Part 1 (do NOT include a trailing slash `/`, e.g., `https://ml-finals-backend.onrender.com`).
5.  **Deploy**: Click **"Deploy"**.
    -   Vercel will build your project. Once done, you will get a live URL for your frontend (e.g., `https://ml-finals-frontend.vercel.app`).

---

## Part 3: Final Integration

1.  **Frontend Test**: Open your Vercel URL. Try to use the features (Prediction, Gap Analysis).
2.  **CORS & Troubleshooting**:
    -   Your backend is currently configured to allow all origins (`allow_origins=["*"]`), so it should work immediately.
    -   If you get connection errors, inspect the browser console (Right-click -> Inspect -> Console) and check if the requests are going to the correct Render URL.

**Congratulations! Your full-stack app is now live!**
