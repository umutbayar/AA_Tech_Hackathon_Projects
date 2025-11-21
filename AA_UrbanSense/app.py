from flask import Flask, jsonify, render_template
from analysis_module import generate_raw_data, clean_and_analyze

# Flask uygulaması kurulumu
app = Flask(__name__)

# Simüle edilmiş ham veri üretimi
RAW_DATA = generate_raw_data(num_records=100)

@app.route('/')
def index():
    return render_template('urbansense_index.html')

# Analiz ve Metrik API Uç Noktası
@app.route('/api/analyze', methods=['GET'])
def get_analysis():
    try:
        # Veri temizleme, analiz ve kriz tespiti
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
    # Not: Gerçek bir projede RAW_DATA'yı buraya yüklemek yerine, 
    # veritabanından çekmek daha doğru olur.
    app.run(debug=True)