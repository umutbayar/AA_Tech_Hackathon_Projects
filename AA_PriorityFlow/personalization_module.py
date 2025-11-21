import random
import copy

def initialize_data():
    """Simüle edilmiş haber ve kullanıcı verilerini oluşturur ve temizler."""
    
    NEWS_DATA = {
        1: {"title": "Meclis Bütçe Görüşmeleri Başladı", "category": "Siyaset", "date": "2025-11-18", "is_urgent": False},
        2: {"title": "Enflasyonla Mücadele Paketi Açıklandı", "category": "Ekonomi", "date": "2025-11-19", "is_urgent": False},
        3: {"title": "Fenerbahçe-Galatasaray Derbisi", "category": "Spor", "date": "2025-11-17", "is_urgent": False},
        4: {"title": "Yerel Yönetimler Yeni Projeleri Tanıttı", "category": "Siyaset", "date": "2025-11-16", "is_urgent": False},
        5: {"title": "Döviz Kurlarında Kritik Gelişme", "category": "Ekonomi", "date": "2025-11-19", "is_urgent": False},
        6: {"title": "Avrupa Şampiyonası Eleme Maçı", "category": "Spor", "date": "2025-11-15", "is_urgent": False},
        7: {"title": "Rusya-Ukrayna Yeni Müzakereler", "category": "Dünya", "date": "2025-11-19", "is_urgent": False},
        8: {"title": "Yerli Otomobil İhracat Hedefleri", "category": "Ekonomi", "date": "2025-11-18", "is_urgent": False},
        9: {"title": "Yeni Anayasa Çalışmaları", "category": "Siyaset", "date": "2025-11-19", "is_urgent": False},
        10: {"title": "Uzay Ajansı Yeni Misyonu Duyurdu", "category": "Bilim", "date": "2025-11-18", "is_urgent": False}
    }

    USER_PROFILES_RAW = {
        'U001': {'name': 'Editör A', 'interests': {'Siyaset': 0.9, 'Ekonomi': 0.7, 'Spor': 0.1}},
        'U002': {'name': 'Muhabir B', 'interests': {'Ekonomi': 0.9, 'Dünya': 0.8, 'Siyaset': 0.4}},
        'U003': {'name': 'Abone C', 'interests': {'Spor': 0.9, 'Bilim': 0.7, 'Ekonomi': 0.2}},
    }
    
    # 🚨 HATA ÇÖZÜMÜ: Tüm ilgi katsayılarını float() ile temizleyerek JSON serileştirme hatasını engelleme.
    USER_PROFILES_CLEANED = {}
    for user_id, profile in USER_PROFILES_RAW.items():
        cleaned_profile = profile.copy()
        cleaned_profile['interests'] = {
            k: float(v) 
            for k, v in profile['interests'].items()
        }
        USER_PROFILES_CLEANED[user_id] = cleaned_profile

    return NEWS_DATA, USER_PROFILES_CLEANED

# initialization'ı çalıştırıyoruz.
NEWS_DATA, USER_PROFILES = initialize_data()

# Geri kalan fonksiyonlar değişmeden kalır

def get_personalized_feed(user_id, is_breaking, news_data, user_profiles, max_feed_size=8):
    user_interest_vector = user_profiles[user_id]['interests']
    weighted_news = []
    
    # 1. Kişiselleştirme Aşaması
    for news_id, news_item in news_data.items():
        category = news_item['category']
        interest_weight = user_interest_vector.get(category, 0.0)
        score = interest_weight * (random.uniform(1.0, 1.2)) 
        
        item_copy = copy.deepcopy(news_item)
        item_copy['news_id'] = news_id
        item_copy['relevance_score'] = f"{score:.4f}"
        
        weighted_news.append(item_copy)
    
    weighted_news.sort(key=lambda x: float(x['relevance_score']), reverse=True)
    final_feed = weighted_news[:max_feed_size]
    
    # 2. Önceliklendirme Aşaması
    if is_breaking:
        breaking_news = {
            "news_id": 100,
            "title": "**🚨 ACİL: Bölgesel Güvenlik Zirvesi Anlık Başladı!**",
            "category": "Acil",
            "date": "2025-11-19",
            "is_urgent": True,
            "relevance_score": "1.0000",
            "reason": "Editoryal Öncelik Kuralı"
        }
        
        final_feed.insert(0, breaking_news)
        final_feed = final_feed[:max_feed_size + 1] 
    
    return final_feed