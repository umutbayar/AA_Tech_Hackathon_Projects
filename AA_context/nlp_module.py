from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import pandas as pd
import numpy as np

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

def initialize_das_simulation():
    """DAS verisini yükler ve TF-IDF vektör indeksini oluşturur."""
    
    df = create_mock_data()
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['text'])
    
    
    return (vectorizer, tfidf_matrix), df 


def find_relevant_content(query_text, das_index, das_archive, top_n=5):
    """
    Sorgu metnine en alakalı arşiv içeriğini bulur.
    """
    vectorizer, tfidf_matrix = das_index
    
    query_vec = vectorizer.transform([query_text])
 
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    related_docs_indices = cosine_similarities.argsort()[:-top_n-1:-1]
    
    results = []
    
    for i in related_docs_indices:
        
        doc = das_archive.iloc[i]
        similarity_score = cosine_similarities[i]
        
        summary = doc['text'][:100] + "..."
        
        results.append({
            "id": int(doc['id']),
            "title": doc['title'],
            "date": doc['date'],
            "similarity_score": f"{similarity_score:.4f}",
            "summary": summary,
            "full_text": doc['text'] 
        })
        
    return results
