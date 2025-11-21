from flask import Flask, jsonify, render_template
from sentiment_module import get_sentiment_metrics, run_sentiment_analysis

# Flask uygulaması kurulumu
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sentinel_index.html')

# Anlık Duygu Metrikleri API Uç Noktası
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    try:
        # Belirli sayıda yeni yorum üret ve analiz et
        analyzed_data = run_sentiment_analysis(num_comments=50) 
        
        # Metrikleri hesapla (Toplam, Yüzdeler, Son Yorumlar)
        metrics = get_sentiment_metrics(analyzed_data)

        response = {
            "status": "Success",
            "metrics": metrics,
            "data_snapshot": analyzed_data # Görselleştirme için ham veri
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Duygu analizi sırasında hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)