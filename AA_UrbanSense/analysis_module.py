import pandas as pd
import numpy as np
import random
import copy

# --- I. VERİ SİMÜLASYONU ---

def generate_raw_data(num_records=100):
    """
    Trafik, Çevre ve Sosyal Medya verilerini içeren ham DataFrame'i simüle eder.
    """
    np.random.seed(42)
    data = {}
    
    # 1. Trafik Verisi Simülasyonu
    data['timestamp'] = pd.to_datetime('2025-11-19 12:00') + pd.to_timedelta(np.arange(num_records), unit='min')
    data['bolge'] = np.random.choice(['Ümraniye', 'Ataşehir', 'Kadıköy', 'Fatih'], size=num_records)
    data['ortalama_hiz_kmh'] = np.clip(np.random.normal(50, 20, num_records), 5, 100)
    data['kaza_bayragi'] = np.random.choice([0, 1], size=num_records, p=[0.95, 0.05]) # %5 kaza ihtimali

    # 2. Çevre Verisi Simülasyonu
    data['pm10'] = np.clip(np.random.normal(30, 10, num_records), 10, 80)
    data['sicaklik_c'] = np.clip(np.random.normal(15, 5, num_records), 5, 30)

    # 3. Sosyal Medya Verisi Simülasyonu (AA Sentinel'den Duygu)
    duygular = ['Pozitif', 'Negatif', 'Nötr']
    data['sosyal_medya_duygu'] = np.random.choice(duygular, size=num_records, p=[0.3, 0.4, 0.3])

    df = pd.DataFrame(data)
    
    # Simülasyon: Rastgele 3-5 satıra kayıp değer ve aykırı değer ekleyelim
    df.loc[np.random.choice(df.index, 3), 'ortalama_hiz_kmh'] = np.nan # Kayıp hız
    df.loc[np.random.choice(df.index, 2), 'pm10'] = 500 # Aykırı PM10
    
    return df

# --- II. VERİ TEMİZLEME ---

def clean_data(df_raw):
    """
    Ham veriyi temizler, eksik ve aykırı değerleri düzeltir.
    """
    df = df_raw.copy()
    
    # 1. Eksik Değer Doldurma (Trafik Hızı)
    # Eksik hız değerlerini o bölgenin medyan hızıyla dolduralım
    df['ortalama_hiz_kmh'].fillna(df.groupby('bolge')['ortalama_hiz_kmh'].transform('median'), inplace=True)

    # 2. Aykırı Değer Temizleme (Çevre Verisi - PM10)
    # PM10 için çok yüksek değerleri (örn: > 150) kaldırılabilir veya eşik değerine çekilebilir
    df.loc[df['pm10'] > 150, 'pm10'] = 150 
    
    # 3. Yeni Özellikler Türetme (Hava Kalitesi Endeksi - HKİ)
    # Basit bir HKİ kategorizasyonu yapalım
    df['hava_kalitesi'] = pd.cut(df['pm10'], 
                                 bins=[0, 35, 75, 150, 501], 
                                 labels=['İyi', 'Orta', 'Hassas', 'Tehlikeli'], 
                                 right=False)
    
    return df

# --- III. ANALİZ VE KRİZ TESPİTİ ---

def perform_crisis_detection(df_cleaned):
    """
    Temizlenmiş verilerden Kriz Tespiti ve Raporlama yapar.
    """
    
    # 1. Metrik Hesaplama
    metrics = {
        "ortalama_pm10": df_cleaned['pm10'].mean(),
        "kaza_sayisi": df_cleaned['kaza_bayragi'].sum(),
        "negatif_duygu_orani": (df_cleaned['sosyal_medya_duygu'] == 'Negatif').mean()
    }
    
    # 2. Kriz Tespit Kuralı (Hibrit Analiz Simülasyonu)
    # Kural: Negatif duygu oranının yüksek olduğu AND (VE) bir kaza raporlandığı bölge
    
    # Bölgesel Oranları Hesapla
    neg_ratio_by_bolge = df_cleaned.groupby('bolge')['sosyal_medya_duygu'].apply(
        lambda x: (x == 'Negatif').mean()
    )
    
    kaza_raporu = df_cleaned.groupby('bolge')['kaza_bayragi'].sum() > 0

    # Kritik eşikler
    NEG_ESIK = 0.50  # %50'den fazla Negatif duygu
    
    kriz_bolgeleri = neg_ratio_by_bolge[
        (neg_ratio_by_bolge > NEG_ESIK) & kaza_raporu
    ].index.tolist()

    kriz_durumu = {
        "tespit_edildi": bool(kriz_bolgeleri),
        "bolgeler": kriz_bolgeleri,
        "mesaj": f"Yüksek Negatif Duygu (%{NEG_ESIK*100}) ve Kaza çakışması tespit edilen bölgeler: {', '.join(kriz_bolgeleri) or 'Yok'}"
    }
    
    return kriz_durumu, metrics

# --- ANA FONKSİYON ---

def clean_and_analyze(raw_data):
    """Tüm adımları çalıştıran ana fonksiyon."""
    
    # 1. Temizleme
    df_cleaned = clean_data(raw_data)
    
    # 2. Analiz ve Kriz Tespiti
    kriz_durumu, metrics = perform_crisis_detection(df_cleaned)
    
    # 🚨 HATA ÖNLEMİ: JSON serileştirme için Pandas/NumPy tiplerini temizle
    metrics_cleaned = {k: (float(v) if isinstance(v, (int, float, np.number)) else v) for k, v in metrics.items()}

    return {
        "temizlenmis_veri_ozeti": df_cleaned,
        "kriz_durumu": kriz_durumu,
        "metrikler": metrics_cleaned
    }