# Enterprise GitHub Functional Intelligence Planner Agent

# Gemini via API (NO Vertex AI)
 
import os
from dotenv import load_dotenv

import requests

import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()
 
 
class PlannerAgent:
 
    def __init__(self):
 
        # Gemini API setup

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:

            raise Exception("GEMINI_API_KEY not set")
 
        genai.configure(api_key=api_key)
 
        self.model = genai.GenerativeModel("gemini-2.5-flash")
 
        # Optional GitHub token (recommended)

        self.github_token = os.getenv("GITHUB_TOKEN")
 
    # ------------------------------------------------

    # GitHub Data Fetching

    # ------------------------------------------------
 
    def fetch_repo_data(self, repo_url):
 
        repo = repo_url.replace("https://github.com/", "")

        headers = {}
 
        if self.github_token:

            headers["Authorization"] = f"Bearer {self.github_token}"
 
        # Repo metadata

        repo_api = f"https://api.github.com/repos/{repo}"

        repo_data = requests.get(repo_api, headers=headers).json()
 
        # Issues

        issues_api = f"https://api.github.com/repos/{repo}/issues?state=open"

        issues = requests.get(issues_api, headers=headers).json()
 
        # Pull Requests

        pr_api = f"https://api.github.com/repos/{repo}/pulls?state=open"

        prs = requests.get(pr_api, headers=headers).json()
 
        return {

            "repo": repo_data,

            "issues": issues[:20],   # limit for token efficiency

            "prs": prs[:20]

        }
 
    # ------------------------------------------------

    # Gemini Planning + Functional Intelligence

    # ------------------------------------------------
 
    def analyze(self, repo_url):
 
        github_data = self.fetch_repo_data(repo_url)
 
        prompt = f"""

You are an Enterprise GitHub Functional Intelligence Agent.
 
Analyze the following repository data and identify:
 
1. Security risks or missing security practices in codebase

2. Architecture improvement opportunities in codebase

3. Performance risks or scalability gaps in codebase

4. Missing enterprise features or functionality in codebase

5. Developer efficiency improvement suggestions in codebase
 
Repository metadata:

{github_data['repo']}
 
Open Issues:

{github_data['issues']}
 
Open Pull Requests:

{github_data['prs']}
 
Provide structured enterprise analysis with clear recommendations.

"""
 
        response = self.model.generate_content(prompt)
 
        return response.text

 