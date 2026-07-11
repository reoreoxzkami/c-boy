# Weekly Auto Game Dev (Groq + GitHub Actions)

This repository automatically generates a new HTML5 browser game every week using Llama 3.3 via Groq API.
Every Monday at 09:00 JST (00:00 UTC), the GitHub Action runs, generates a game, commits the files, and deploys.

## Setup

1. Go to your GitHub Repository Settings.
2. Select **Secrets and variables** > **Actions**.
3. Create a repository secret named `GROQ_API_KEY` and set your Groq API Key.
4. Enable Write Permissions for Workflows:
   - Go to **Settings** > **Actions** > **General**.
   - Under **Workflow permissions**, select **Read and write permissions** and click **Save**.
5. Enable GitHub Pages (Optional but recommended):
   - Go to **Settings** > **Pages**.
   - Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
   - Under **Branch**, choose `main` and `/ (root)`.
