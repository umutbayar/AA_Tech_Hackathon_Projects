from flask import Flask, jsonify, render_template
from analysis_module import generate_raw_data, clean_and_analyze

app = Flask(__name__)

RAW_DATA = generate_raw_data(num_records=100)

@app.route('/')
def index():
    return render_template('urbansense_index.html')

@app.route('/api/analyze', methods=['GET'])
def get_analysis():
    try:
        analysis_results = clean_and_analyze(RAW_DATA)

        response = {
            "status": "Success",
            "kriz_durumu": analysis_results['kriz_durumu'],
            "sonuclar": analysis_results['temizlenmis_veri_ozeti'].head(5).to_dict('records'), # İlk 5 kaydı gönder
            "metrikler": analysis_results['metrikler']
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Analiz sırasında hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':

    app.run(debug=True)
