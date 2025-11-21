from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import pandas as pd
import numpy as np

# --- 1. DAS (Dijital Arşiv Sistemi) Simülasyon Verisi ---
def create_mock_data():
    """DAS'taki geçmiş haberleri simüle eden veri seti oluşturur."""
    data = [
        {"id": 101, "title": "2018 Cumhurbaşkanlığı Seçimleri", "text": "2018'deki seçimlerde Cumhurbaşkanlığı sistemi ve ittifaklar ön plandaydı. O dönemin ana gündemi ekonomi ve siyasi istikrardı. Sonuçlar büyük ilgi gördü.", "date": "2018-06-25"},
        {"id": 102, "title": "2023 Genel Seçim Analizi", "text": "Türkiye'nin 2023 genel seçimleri, yüksek katılım ve yoğun rekabetle geçti. Meclis aritmetiği önemli ölçüde değişti.", "date": "2023-05-15"},
        {"id": 103, "title": "Basketbolda Milli Takım Başarısı", "text": "Milli basketbol takımımız Avrupa Şampiyonası'nda çeyrek finale yükseldi. Spor dünyasında büyük sevinç yaşandı. Turnuva çekişmeli geçti.", "date": "2024-09-10"},
        {"id": 104, "title": "Tarihi İstanbul Depremi", "text": "1999 yılında meydana gelen büyük Marmara depremi, bölgede büyük yıkıma yol açtı. Afet yönetimi ve kriz koordinasyonu dersleri çıkarıldı.", "date": "1999-08-17"},
        {"id": 105, "title": "Ekonomide Yeni Reform Paketi", "text": "Hükümet, yüksek enflasyonla mücadele kapsamında yeni bir mali reform paketini açıkladı. Paket, piyasalarda beklentiyi karşıladı.", "date": "2025-11-18"},
        {"id": 106, "title": "Salgın Dönemi Kısıtlamaları", "text": "2020 yılında küresel salgın nedeniyle alınan kısıtlama kararları ve sokağa çıkma yasakları. Vatandaşlar evlerinde kaldı.", "date": "2020-04-01"},
        {"id": 107, "title": "Meclis Bütçe Görüşmeleri", "text": "Türkiye Büyük Millet Meclisi'nde 2026 yılı bütçe görüşmeleri başladı. Muhalefet ve iktidar partileri arasında sert tartışmalar yaşandı.", "date": "2025-11-19"},
    ]
    return pd.DataFrame(data)

# --- 2. İndeksi Başlatma Fonksiyonu ---
def initialize_das_simulation():
    """DAS verisini yükler ve TF-IDF vektör indeksini oluşturur."""
    
    # Mock veriyi yükle
    df = create_mock_data()
    
    # TF-IDF Vektörleştiriciyi tanımla ve veriye uygula
    # stop_words: 'english' kullanıldı ancak gerçek uygulamada Türkçe stop word listesi kullanılmalıdır.
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['text'])
    
    # İndeks (Vektör Matrisi) ve Vektörleştirici (DAS_INDEX) kaydedilir
    # df (DAS_ARCHIVE) de kaydedilir
    return (vectorizer, tfidf_matrix), df 


# --- 3. İçerik Arama Fonksiyonu (Ana İşlem) ---
def find_relevant_content(query_text, das_index, das_archive, top_n=5):
    """
    Sorgu metnine en alakalı arşiv içeriğini bulur.
    """
    vectorizer, tfidf_matrix = das_index
    
    # 1. Sorgu metnini vektörleştir
    query_vec = vectorizer.transform([query_text])
    
    # 2. Kosinüs Benzerliği ile benzerlikleri hesapla (Anlamsal Arama)
    # Bu, sorgu vektörünün DAS matrisindeki her bir dökümanla ne kadar benzer olduğunu ölçer
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # 3. En iyi 'top_n' sonuçların indeksini al
    related_docs_indices = cosine_similarities.argsort()[:-top_n-1:-1]
    
    results = []
    
    # 4. Sonuçları formatla
    for i in related_docs_indices:
        
        doc = das_archive.iloc[i]
        similarity_score = cosine_similarities[i]
        
        # Basit özetleme simülasyonu (Gerçekte NLP ile özetlenir)
        summary = doc['text'][:100] + "..."
        
        results.append({
            "id": int(doc['id']),
            "title": doc['title'],
            "date": doc['date'],
            "similarity_score": f"{similarity_score:.4f}", # 4 ondalık hassasiyet
            "summary": summary,
            "full_text": doc['text'] # Detaylı inceleme için tam metin
        })
        
    return results