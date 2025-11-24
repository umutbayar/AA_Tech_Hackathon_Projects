import os
from flask import Flask, request, jsonify, render_template
from nlp_module import initialize_das_simulation, find_relevant_content

app = Flask(__name__)

DAS_INDEX, DAS_ARCHIVE = initialize_das_simulation()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/context', methods=['POST'])
def get_context():
    data = request.json
    
    if not data or 'news_text' not in data:
        return jsonify({"error": "news_text alanı zorunludur."}), 400

    news_text = data['news_text']

    try:
        results = find_relevant_content(news_text, DAS_INDEX, DAS_ARCHIVE)
        
        response = {
            "query": news_text[:50] + "...",
            "status": "Success",
            "relevant_content": results,
            "count": len(results)
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Analiz sırasında hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

