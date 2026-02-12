from flask import Flask, render_template, request, jsonify
from agents.planner_agent import PlannerAgent
import markdown

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        repo_url = request.json.get('repo_url')
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        agent = PlannerAgent()
        result = agent.analyze(repo_url)
        
        # Convert markdown to HTML for better display
        html_result = markdown.markdown(result)
        
        return jsonify({
            'success': True,
            'analysis': result,
            'html_analysis': html_result,
            'repo_url': repo_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_issue', methods=['POST'])
def create_issue():
    try:
        repo_url = request.json.get('repo_url')
        analysis_result = request.json.get('analysis_result')
        
        if not repo_url or not analysis_result:
            return jsonify({'error': 'Repository URL and analysis result are required'}), 400
        
        agent = PlannerAgent()
        
        # Check if GitHub token is set
        if not agent.github_token:
            return jsonify({'error': 'GitHub token not found. Please set GITHUB_TOKEN in your .env file with repo access permissions.'}), 400
        
        print(f"Creating issue for repo: {repo_url}")  # Debug log
        issue_result = agent.create_issue_with_analysis(repo_url, analysis_result)
        print(f"Issue creation result: {issue_result}")  # Debug log
        
        return jsonify(issue_result)
    except Exception as e:
        print(f"Error in create_issue endpoint: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)