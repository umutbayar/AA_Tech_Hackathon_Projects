from flask import Flask, request, jsonify, render_template
from image_generation_module import analyze_and_generate_prompt

# Flask uygulaması kurulumu
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('visualizer_index.html')

# Görsel Komutu Üretme API Uç Noktası
@app.route('/api/generate_prompt', methods=['POST'])
def generate_visual():
    data = request.json
    
    if not data or 'news_text' not in data:
        return jsonify({"error": "news_text alanı zorunludur."}), 400

    news_text = data['news_text']

    try:
        # NLP ve Prompt Üretim Modülünü Çalıştır
        result = analyze_and_generate_prompt(news_text)
        
        response = {
            "status": "Success",
            "analysis": result['analysis'],
            "generated_prompt": result['prompt'],
            "demo_image_url": "Simulasyon_URL_Buraya_Gelecek" # Gerçek bir AI servisi kullanılmadığı için placeholder
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Komut üretimi sırasında hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)