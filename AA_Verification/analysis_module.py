from PIL import Image
from PIL.ExifTags import TAGS
import random
import os

# --- A. GÖRSEL BÜTÜNLÜK ANALİZİ ---
def analyze_image_integrity(filepath):
    """
    Görselin EXIF verilerini çıkarır ve bütünlük skoru hesaplar.
    """
    metadata = {}
    is_manipulated = False
    integrity_score = 100 # Başlangıçta tam puan

    try:
        image = Image.open(filepath)
        
        # 1. EXIF Verilerini Çıkarma
        exifdata = image.getexif()
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            metadata[tag] = data

        # 2. Basit Manipülasyon Kontrolleri (Hackathon Simülasyonu)
        # Eğer EXIF verisi yoksa veya "Software" etiketi Photoshop vb. içeriyorsa skor düşürülür.
        if not metadata:
            is_manipulated = True
            integrity_score -= 30
            
        if 'Software' in metadata and 'Photoshop' in metadata['Software']:
             integrity_score -= 15
        
        # JPEG kalitesi kontrolü (çok düşük kalite manipülasyon işareti olabilir)
        if image.format == 'JPEG' and image.info.get('quality', 95) < 70:
             integrity_score -= 10
             
    except Exception as e:
        # Dosya görsel değilse veya okunamıyorsa
        integrity_score = 50
        is_manipulated = True
        metadata = {"Hata": str(e), "Açıklama": "Görsel dosyası okunamadı veya biçimi desteklenmiyor."}
        
    return {
        "score": integrity_score,
        "is_suspicious": is_manipulated or integrity_score < 75,
        "metadata": metadata,
        "reason": "EXIF verisi eksikliği veya düzenleme araçları tespiti"
    }

# --- B. TERSİNE GÖRSEL ARAMA SİMÜLASYONU ---
def reverse_image_search(filename):
    """
    Harici bir API (Google, Yandex) kullanılmadığı için simülasyon yapılır.
    """
    
    # 1. Simülasyon Sonuçları
    sources = [
        {"url": "socialmedia.com/post1", "date": "2025-11-20", "context": "Hava durumu raporu"},
        {"url": "haberajansi.com/org", "date": "2025-11-10", "context": "Orijinal haber kaynağı"},
        {"url": "forumlar.net/yalan", "date": "2025-11-21", "context": "Yanlış bağlamda yayınlanmış"}
    ]
    
    # 2. Skorlama Mantığı (Basit)
    # Eğer orijinal kaynaktan daha yeni bir tarihte, farklı bağlamda çok sayıda paylaşım varsa skor düşer.
    
    # Simülasyonla rastgele skor düşürme
    risk_factor = random.randint(10, 40)
    search_score = 100 - risk_factor
    
    # Eğer orijinal kaynak varsa ve ilk yayın tarihi farklı ise skor düşer
    if search_score < 70:
        is_suspicious = True
        reason = "Aynı görsel, orijinalinden farklı bağlam ve tarihte çok sayıda farklı kaynaktan tespit edildi."
    else:
        is_suspicious = False
        reason = "Çoğunlukla orijinal veya ilgili kaynaklarda yayınlanmış."


    return {
        "score": search_score,
        "is_suspicious": is_suspicious,
        "first_seen": "2025-11-10T09:00:00Z", # En eski tarih simülasyonu
        "sources_found": sources,
        "reason": reason
    }

# Simülasyonu çalıştırırken dosyanın silinmesi gerekeceği için buraya dahil etmedim.
# Normalde kodlama bitince import edip test edebilirsiniz.