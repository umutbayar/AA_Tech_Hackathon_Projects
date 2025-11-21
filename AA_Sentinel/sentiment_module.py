import random

# Simüle edilmiş Türkçe Yorum Veritabanı
POSITIVE_COMMENTS = [
    "AA'nın bu haberi çok başarılı ve yerinde olmuş. Güvenilir kaynak!",
    "Harika bir analiz, detaylı ve aydınlatıcı. Teşekkürler.",
    "Doğru bilgiye ulaşmak için AA'yı takip ediyorum, yine şaşırtmadı.",
    "Bu gelişme ülkemiz adına çok sevindirici."
]

NEGATIVE_COMMENTS = [
    "Bu haberin yayınlanma şekli yanlı ve taraflı görünüyor.",
    "Yeterince detay yok, yüzeysel bir haber olmuş.",
    "Bu durum ülkemiz için büyük bir fiyasko ve hayal kırıklığı.",
    "Kesinlikle yanlış yorumlanmış ve çarpıtılmış."
]

NEUTRAL_COMMENTS = [
    "Haber metnini okudum, başka kaynaklarla karşılaştıracağım.",
    "Gelişmeleri takip ediyorum.",
    "Konu hakkında yorum yapmak için erken.",
    "Sıradan bir gelişme."
]

def simple_turkish_sentiment(comment):
    """
    Basit kural tabanlı Türkçe duygu analizi simülasyonu.
    Gerçekte: BERT veya LSTM gibi modeller kullanılır.
    """
    comment = comment.lower()
    
    # Negatif kelime kontrolü
    if any(word in comment for word in ["yanlı", "taraflı", "yetersiz", "yanlış", "fiyasko"]):
        return "Negatif"
    # Pozitif kelime kontrolü
    elif any(word in comment for word in ["başarılı", "harika", "sevindirici", "güvenilir", "aydınlatıcı"]):
        return "Pozitif"
    else:
        return "Nötr"

def run_sentiment_analysis(num_comments=30):
    """Rastgele yorumlar üretir ve duygu analizi yapar."""
    all_comments = POSITIVE_COMMENTS + NEGATIVE_COMMENTS + NEUTRAL_COMMENTS
    analyzed_results = []
    
    for _ in range(num_comments):
        comment_text = random.choice(all_comments)
        
        # Rastgelelik katmak için bazen ters duygu atayalım (model hatalarını simüle etmek için)
        if random.random() < 0.15: # %15 ihtimalle rastgele duygu atama
            sentiment = random.choice(["Pozitif", "Negatif", "Nötr"])
        else:
            sentiment = simple_turkish_sentiment(comment_text)
            
        
        # Rastgele bir anahtar kelime atayalım (Filtreleme simülasyonu için)
        keyword = random.choice(["Ekonomi", "Siyaset", "Spor", "Genel"])

        analyzed_results.append({
            "comment": comment_text,
            "sentiment": sentiment,
            "keyword": keyword,
            "timestamp": f"2025-11-19 {random.randint(10, 18)}:{random.randint(0, 59)}"
        })
        
    return analyzed_results

def get_sentiment_metrics(analyzed_data):
    """Analiz edilmiş verilerden metrikleri hesaplar."""
    total_count = len(analyzed_data)
    counts = {"Pozitif": 0, "Negatif": 0, "Nötr": 0}
    
    for item in analyzed_data:
        counts[item['sentiment']] += 1
        
    metrics = {
        "total_comments": total_count,
        "sentiment_counts": counts,
        "sentiment_percentages": {
            k: (v / total_count * 100) if total_count > 0 else 0 
            for k, v in counts.items()
        },
        "recent_comments": analyzed_data[:10]
    }
    
    return metrics