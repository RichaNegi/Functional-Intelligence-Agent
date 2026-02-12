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
            'html_analysis': html_result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)