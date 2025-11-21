import random
# from textblob import TextBlob # TextBlob yerine basit kural tabanlı simülasyon kullanıyoruz

def analyze_and_generate_prompt(news_text):
    """
    Haber metnini analiz eder ve görsel üretimi için bir komut (prompt) oluşturur.
    """
    
    # 1. Simülasyon: Anahtar Kelime/Varlık Çıkarımı
    keywords = {
        "Siyaset": ["başbakan", "meclis", "seçim", "lider"],
        "Ekonomi": ["enflasyon", "merkez bankası", "döviz", "piyasa"],
        "Spor": ["futbol", "derbi", "şampiyon", "stad"],
        "Afet": ["deprem", "enkaz", "kurtarma ekibi", "arama kurtarma"],
        "Teknoloji": ["yapay zeka", "drone", "yazılım", "robot"]
    }
    
    # Metindeki anahtar kelimeleri bul ve ana kategoriyi belirle
    detected_keywords = []
    main_category = "Genel"
    
    for category, k_list in keywords.items():
        for keyword in k_list:
            if keyword in news_text.lower():
                detected_keywords.append(keyword)
                main_category = category
                break # Her kategoriden bir kelime bulmak yeterli

    if not detected_keywords:
        detected_keywords.append("haber masası") # Hiçbir şey bulunamazsa varsayılan
    
    main_subject = detected_keywords[0].capitalize()
    
    # 2. Simülasyon: Duygu Analizi ve Stil Belirleme
    # Gerçek uygulamada NLP ile yapılır, burada kural tabanlı simüle edelim.
    sentiment = "sakin ve profesyonel"
    if any(word in news_text.lower() for word in ["acil", "kriz", "felaket", "şok"]):
        sentiment = "dramatik ve kasvetli"
    elif any(word in news_text.lower() for word in ["başarı", "rekor", "zafer", "kutlama"]):
        sentiment = "neşeli ve aydınlık"
        
    style = "foto-gerçekçi dijital resim, haber ajansı estetiği"
    
    # 3. Prompt Mühendisliği (Komut Oluşturma)
    # Metin tabanlı komutu oluştur
    base_prompt = (
        f"AA (Anadolu Ajansı) tarzında, {style}, {main_subject} konusunu öne çıkaran bir görsel. "
        f"Detay: {main_category} ortamında, {sentiment} bir atmosfer. Telifsiz ve profesyonel görünüm."
    )

    return {
        "analysis": {
            "main_subject": main_subject,
            "category": main_category,
            "sentiment": sentiment
        },
        "prompt": base_prompt
    }