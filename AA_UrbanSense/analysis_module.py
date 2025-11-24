import pandas as pd
import numpy as np
import random
import copy



def generate_raw_data(num_records=100):
    """
    Trafik, Çevre ve Sosyal Medya verilerini içeren ham DataFrame'i simüle eder.
    """
    np.random.seed(17)
    data = {}
    
    data['timestamp'] = pd.to_datetime('2025-11-19 12:00') + pd.to_timedelta(np.arange(num_records), unit='min')
    data['bolge'] = np.random.choice(['Ümraniye', 'Ataşehir', 'Kadıköy', 'Fatih'], size=num_records)
    data['ortalama_hiz_kmh'] = np.clip(np.random.normal(50, 20, num_records), 5, 100)
    data['kaza_bayragi'] = np.random.choice([0, 1], size=num_records, p=[0.95, 0.05]) # %5 kaza ihtimali

    data['pm10'] = np.clip(np.random.normal(30, 10, num_records), 10, 80)
    data['sicaklik_c'] = np.clip(np.random.normal(15, 5, num_records), 5, 30)

    duygular = ['Pozitif', 'Negatif', 'Nötr']
    data['sosyal_medya_duygu'] = np.random.choice(duygular, size=num_records, p=[0.3, 0.4, 0.3])

    df = pd.DataFrame(data)
    
    df.loc[np.random.choice(df.index, 3), 'ortalama_hiz_kmh'] = np.nan # Kayıp hız
    df.loc[np.random.choice(df.index, 2), 'pm10'] = 500 # Aykırı PM10
    
    return df


def clean_data(df_raw):
    """
    Ham veriyi temizler, eksik ve aykırı değerleri düzeltir.
    """
    df = df_raw.copy()
    

    df['ortalama_hiz_kmh'].fillna(df.groupby('bolge')['ortalama_hiz_kmh'].transform('median'), inplace=True)

   
    df.loc[df['pm10'] > 150, 'pm10'] = 150 
    
    df['hava_kalitesi'] = pd.cut(df['pm10'], 
                                 bins=[0, 35, 75, 150, 501], 
                                 labels=['İyi', 'Orta', 'Hassas', 'Tehlikeli'], 
                                 right=False)
    
    return df

def perform_crisis_detection(df_cleaned):
    """
    Temizlenmiş verilerden Kriz Tespiti ve Raporlama yapar.
    """
    
    metrics = {
        "ortalama_pm10": df_cleaned['pm10'].mean(),
        "kaza_sayisi": df_cleaned['kaza_bayragi'].sum(),
        "negatif_duygu_orani": (df_cleaned['sosyal_medya_duygu'] == 'Negatif').mean()
    }
    
    neg_ratio_by_bolge = df_cleaned.groupby('bolge')['sosyal_medya_duygu'].apply(
        lambda x: (x == 'Negatif').mean()
    )
    
    kaza_raporu = df_cleaned.groupby('bolge')['kaza_bayragi'].sum() > 0

    NEG_ESIK = 0.50  
    
    kriz_bolgeleri = neg_ratio_by_bolge[
        (neg_ratio_by_bolge > NEG_ESIK) & kaza_raporu
    ].index.tolist()

    kriz_durumu = {
        "tespit_edildi": bool(kriz_bolgeleri),
        "bolgeler": kriz_bolgeleri,
        "mesaj": f"Yüksek Negatif Duygu (%{NEG_ESIK*100}) ve Kaza çakışması tespit edilen bölgeler: {', '.join(kriz_bolgeleri) or 'Yok'}"
    }
    
    return kriz_durumu, metrics


def clean_and_analyze(raw_data):
    """Tüm adımları çalıştıran ana fonksiyon."""
    
    df_cleaned = clean_data(raw_data)
    
    kriz_durumu, metrics = perform_crisis_detection(df_cleaned)
    
    metrics_cleaned = {k: (float(v) if isinstance(v, (int, float, np.number)) else v) for k, v in metrics.items()}

    return {
        "temizlenmis_veri_ozeti": df_cleaned,
        "kriz_durumu": kriz_durumu,
        "metrikler": metrics_cleaned
    }
