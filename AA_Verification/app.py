import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from analysis_module import analyze_image_integrity, reverse_image_search

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify', methods=['POST'])
def verify_image():
    if 'file' not in request.files:
        return jsonify({"error": "Dosya yüklenmedi"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Dosya adı boş"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            integrity_results = analyze_image_integrity(filepath)
            
            search_results = reverse_image_search(filename) 
            
            final_score = (integrity_results['score'] + search_results['score']) / 2
            
            response = {
                "filename": filename,
                "overall_score": f"{final_score:.2f}",
                "integrity_report": integrity_results,
                "search_report": search_results,
                "status": "Success",
            }
            return jsonify(response)
        
        except Exception as e:
            os.remove(filepath)
            return jsonify({"error": f"Analiz sırasında hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
