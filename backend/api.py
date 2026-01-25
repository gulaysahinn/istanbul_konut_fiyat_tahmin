from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)
CORS(app)

# Modelleri yükle
MODEL_PATH = 'models'
rf_model = None
gb_model = None
ilce_dict = None

def load_models():
    global rf_model, gb_model, ilce_dict
    try:
        rf_model = joblib.load(os.path.join(MODEL_PATH, 'rf_model.pkl'))
        gb_model = joblib.load(os.path.join(MODEL_PATH, 'gb_model.pkl'))
        ilce_dict = joblib.load(os.path.join(MODEL_PATH, 'ilce_dict.pkl'))
        print("Modeller başarıyla yüklendi!")
    except Exception as e:
        print(f"Model yükleme hatası: {e}")

# İlçe kodları (preprocessing ile aynı sırada olmalı)
ILCE_KODLARI = {
    'Adalar': 0, 'Arnavutköy': 1, 'Ataşehir': 2, 'Avcılar': 3, 'Bağcılar': 4,
    'Bahçelievler': 5, 'Bakırköy': 6, 'Başakşehir': 7, 'Bayrampaşa': 8, 'Beşiktaş': 9,
    'Beykoz': 10, 'Beylikdüzü': 11, 'Beyoğlu': 12, 'Büyükçekmece': 13, 'Çatalca': 14,
    'Çekmeköy': 15, 'Esenler': 16, 'Esenyurt': 17, 'Eyüpsultan': 18, 'Fatih': 19,
    'Gaziosmanpaşa': 20, 'Güngören': 21, 'Kadıköy': 22, 'Kağıthane': 23, 'Kartal': 24,
    'Küçükçekmece': 25, 'Maltepe': 26, 'Pendik': 27, 'Sancaktepe': 28, 'Sarıyer': 29,
    'Silivri': 30, 'Sultanbeyli': 31, 'Sultangazi': 32, 'Şile': 33, 'Şişli': 34,
    'Tuzla': 35, 'Ümraniye': 36, 'Üsküdar': 37, 'Zeytinburnu': 38
}

def isitma_skoru(tip):
    """Isıtma tipini skora çevir"""
    tip = str(tip).lower()
    if 'doğalgaz' in tip or 'dogalgaz' in tip or 'kombi' in tip:
        return 1.0
    elif 'merkezi' in tip:
        return 0.5
    else:
        return 0.0

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Gelen verileri al
        ilce = data.get('ilce', 'Kadıköy')
        metrekare = float(data.get('metrekare', 100))
        oda_sayisi = float(data.get('oda_sayisi', 3))
        bina_yasi = float(data.get('bina_yasi', 5))
        kat_sayisi = float(data.get('kat_sayisi', 10))
        bulundugu_kat = float(data.get('bulundugu_kat', 3))
        isitma_tipi = data.get('isitma_tipi', 'Doğalgaz')
        site_icerisinde = 1 if data.get('site_icerisinde', False) else 0
        
        # Feature'ları hesapla
        ilce_kod = ILCE_KODLARI.get(ilce, 22)
        oda_metrekare = metrekare / (oda_sayisi + 0.1)
        yas_grup = 0 if bina_yasi <= 5 else (1 if bina_yasi <= 10 else (2 if bina_yasi <= 20 else 3))
        metrekare_log = np.log1p(metrekare)
        oda_sayisi_log = np.log1p(oda_sayisi)
        metrekare_x_oda = metrekare * oda_sayisi
        yas_x_metrekare = bina_yasi * metrekare
        ilce_gucu = ilce_dict.get(ilce, 15000000) if ilce_dict else 15000000
        giris_kat_mi = 1 if bulundugu_kat <= 0 else 0
        site_bonus = site_icerisinde * metrekare
        kat_orani = min(1, bulundugu_kat / (kat_sayisi + 0.1))
        isitma_skor = isitma_skoru(isitma_tipi)
        
        # İlçe + Oda kombinasyonu için ortalama (basitleştirilmiş)
        ilce_oda_gucu = ilce_gucu * (1 + (oda_sayisi - 3) * 0.1)
        
        # Lüks katsayısı
        luks_katsayisi = ilce_gucu * site_icerisinde
        
        # Feature vektörü oluştur
        features = np.array([[
            metrekare, oda_sayisi, bina_yasi, ilce_kod,
            oda_metrekare, yas_grup, metrekare_log, oda_sayisi_log,
            metrekare_x_oda, yas_x_metrekare, ilce_gucu,
            site_icerisinde, bulundugu_kat, giris_kat_mi, site_bonus,
            kat_orani, isitma_skor, ilce_oda_gucu, luks_katsayisi
        ]])
        
        # Tahmin yap (log space'de)
        if rf_model and gb_model:
            rf_pred = rf_model.predict(features)[0]
            gb_pred = gb_model.predict(features)[0]
            # Stacked tahmin
            log_tahmin = (rf_pred + gb_pred) / 2
            # Gerçek fiyata çevir
            tahmin = np.expm1(log_tahmin)
        else:
            # Demo tahmin (model yüklenmemişse)
            tahmin = metrekare * (ilce_gucu / 100) * (1 - bina_yasi * 0.01) * (1 + site_icerisinde * 0.15)
        
        # Sonucu yuvarla
        tahmin = round(tahmin / 100000) * 100000  # 100.000'e yuvarla
        
        return jsonify({
            'success': True,
            'tahmin': int(tahmin),
            'ilce': ilce,
            'metrekare': metrekare
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'models_loaded': rf_model is not None and gb_model is not None
    })

# Chatbot için bilgi tabanı
CHATBOT_BILGI = {
    'ilceler': {
        'Beşiktaş': {'m2_fiyat': 300000, 'ozellik': 'Lüks, Boğaz manzarası, prestijli', 'trend': 'stabil'},
        'Kadıköy': {'m2_fiyat': 220000, 'ozellik': 'Kültür merkezi, canlı sosyal yaşam', 'trend': 'artış'},
        'Sarıyer': {'m2_fiyat': 280000, 'ozellik': 'Boğaz, orman, villa bölgeleri', 'trend': 'artış'},
        'Şişli': {'m2_fiyat': 200000, 'ozellik': 'Merkezi konum, iş dünyası', 'trend': 'stabil'},
        'Üsküdar': {'m2_fiyat': 160000, 'ozellik': 'Tarihi doku, Marmaray bağlantısı', 'trend': 'artış'},
        'Ataşehir': {'m2_fiyat': 170000, 'ozellik': 'Finans merkezi, modern', 'trend': 'artış'},
        'Ümraniye': {'m2_fiyat': 140000, 'ozellik': 'İş merkezleri, metro', 'trend': 'artış'},
        'Pendik': {'m2_fiyat': 130000, 'ozellik': 'Havalimanı, marina', 'trend': 'yüksek artış'},
        'Kartal': {'m2_fiyat': 125000, 'ozellik': 'Marmaray, sahil', 'trend': 'artış'},
        'Maltepe': {'m2_fiyat': 150000, 'ozellik': 'Sahil bandı, park', 'trend': 'stabil'},
        'Başakşehir': {'m2_fiyat': 145000, 'ozellik': 'Şehir hastanesi, yeni', 'trend': 'artış'},
        'Beylikdüzü': {'m2_fiyat': 115000, 'ozellik': 'Planlı, metrobüs', 'trend': 'artış'},
        'Esenyurt': {'m2_fiyat': 85000, 'ozellik': 'Ekonomik, kalabalık', 'trend': 'artış'},
        'Bakırköy': {'m2_fiyat': 180000, 'ozellik': 'Sahil, yerleşik', 'trend': 'stabil'},
        'Fatih': {'m2_fiyat': 165000, 'ozellik': 'Tarihi yarımada', 'trend': 'stabil'},
        'Eyüpsultan': {'m2_fiyat': 140000, 'ozellik': 'Tarihi, teleferik', 'trend': 'artış'},
        'Tuzla': {'m2_fiyat': 100000, 'ozellik': 'Sanayi, teknoloji', 'trend': 'artış'},
        'Sancaktepe': {'m2_fiyat': 110000, 'ozellik': 'Metro, gelişen', 'trend': 'yüksek artış'},
        'Çekmeköy': {'m2_fiyat': 120000, 'ozellik': 'Doğa, metro', 'trend': 'artış'},
        'Arnavutköy': {'m2_fiyat': 75000, 'ozellik': 'Havalimanı, yeni', 'trend': 'yüksek artış'},
    },
    'genel_bilgi': {
        'ortalama_m2': 130000,
        'yillik_artis': 45,
        'en_pahali': 'Beşiktaş',
        'en_ucuz': 'Çatalca',
        'en_cok_artan': 'Arnavutköy'
    }
}

def chatbot_yanit(mesaj):
    """Kullanıcı mesajına yanıt oluştur"""
    mesaj = mesaj.lower().strip()
    
    # İlçe sorgusu kontrolü
    for ilce, bilgi in CHATBOT_BILGI['ilceler'].items():
        if ilce.lower() in mesaj:
            return f"""📍 **{ilce} İlçesi Bilgileri**

💰 Ortalama m² Fiyatı: {bilgi['m2_fiyat']:,} TL
🏠 Özellikler: {bilgi['ozellik']}
📈 Fiyat Trendi: {bilgi['trend'].capitalize()}

💡 100 m² daire için tahmini fiyat: {bilgi['m2_fiyat'] * 100:,} TL"""

    # Fiyat soruları
    if any(word in mesaj for word in ['fiyat', 'ne kadar', 'kaç para', 'kaç lira', 'maliyet']):
        return """💰 **İstanbul Konut Fiyatları (2026)**

📊 Ortalama m² fiyatı: 130,000 TL
📈 Yıllık artış oranı: %45

**Segment Bazlı:**
🔵 Ekonomik (Esenyurt, Arnavutköy): 75,000-90,000 TL/m²
🟢 Orta (Pendik, Tuzla, Sancaktepe): 100,000-130,000 TL/m²
🟡 Orta-Üst (Ümraniye, Başakşehir): 140,000-160,000 TL/m²
🟠 Lüks (Kadıköy, Bakırköy): 180,000-220,000 TL/m²
🔴 Premium (Beşiktaş, Sarıyer): 280,000-350,000 TL/m²

Hangi ilçe hakkında detay istersiniz?"""

    # Yatırım soruları
    if any(word in mesaj for word in ['yatırım', 'kazanç', 'değerlen', 'artış', 'potansiyel']):
        return """📈 **Yatırım Potansiyeli Yüksek İlçeler**

🥇 **Arnavutköy** - Havalimanı etkisi, %60+ değer artışı beklentisi
🥈 **Sancaktepe** - Metro projeleri, yeni konut alanları
🥉 **Pendik** - Marina, Sabiha Gökçen, lojistik merkez

**Dikkat Edilmesi Gerekenler:**
✅ Ulaşım projeleri (metro, otoyol)
✅ Kentsel dönüşüm bölgeleri
✅ Yeni iş merkezi planları
❌ Aşırı kalabalık bölgeler
❌ Deprem risk bölgeleri

💡 İpucu: 3-5 yıl içinde metro gelecek bölgelere bakın!"""

    # Kredi soruları
    if any(word in mesaj for word in ['kredi', 'faiz', 'taksit', 'banka', 'mortgage']):
        return """🏦 **Konut Kredisi Bilgileri (2026)**

📊 Güncel Faiz Oranları: %2.5-3.5 (aylık)
📅 Vade: 120-180 ay

**Örnek Hesaplama (5,000,000 TL):**
• 120 ay vade: ~75,000 TL/ay
• 180 ay vade: ~60,000 TL/ay

**Gerekli Belgeler:**
📄 Gelir belgesi / Maaş bordrosu
📄 Kimlik fotokopisi
📄 İkametgah
📄 Tapu fotokopisi

💡 İpucu: Peşinat ne kadar yüksekse, faiz o kadar düşük!"""

    # Site/apartman soruları
    if any(word in mesaj for word in ['site', 'apartman', 'güvenlik', 'otopark', 'havuz']):
        return """🏢 **Site vs Apartman Karşılaştırması**

**Site İçi Konut (+%15-25 değer):**
✅ 7/24 güvenlik
✅ Otopark
✅ Sosyal tesisler (havuz, spor salonu)
✅ Çocuk oyun alanı
❌ Yüksek aidat (2,000-8,000 TL/ay)

**Müstakil Apartman:**
✅ Düşük aidat (500-1,500 TL/ay)
✅ Daha az kural
❌ Güvenlik yok
❌ Sosyal alan yok

💡 Ailelere site, bekarlara apartman daha uygun!"""

    # Metrekare soruları
    if any(word in mesaj for word in ['metrekare', 'm2', 'büyüklük', 'kaç m']):
        return """📐 **Metrekare Rehberi**

**Oda Sayısına Göre Ortalama m²:**
• 1+1: 45-65 m²
• 2+1: 75-100 m²
• 3+1: 110-140 m²
• 4+1: 150-200 m²
• 5+1: 200+ m²

**Net vs Brüt:**
• Brüt m² = Net m² + Ortak alanlar
• Genelde Brüt = Net × 1.20-1.35

💡 İlan'da brüt yazıyor, net'i %20-25 düşük hesaplayın!"""

    # Bina yaşı soruları
    if any(word in mesaj for word in ['bina yaşı', 'eski', 'yeni', 'deprem', 'imar']):
        return """🏗️ **Bina Yaşı Rehberi**

**Yaşa Göre Değer:**
• 0-5 yaş: %100 değer (yeni)
• 5-10 yaş: %90-95 değer
• 10-20 yaş: %80-90 değer
• 20+ yaş: %70-80 değer

**Deprem Yönetmeliği:**
• 2000 sonrası: Güvenli
• 2018 sonrası: En güvenli
• 1999 öncesi: ⚠️ Dikkat!

💡 Kentsel dönüşüm bölgelerinde eski bina alıp yenisini bekleyebilirsiniz!"""

    # Selamlama
    if any(word in mesaj for word in ['merhaba', 'selam', 'hey', 'meraba', 'selamlar']):
        return """👋 Merhaba! Ben Konut Asistan.

Size şu konularda yardımcı olabilirim:
• 📍 İlçe bilgileri (örn: "Kadıköy hakkında bilgi")
• 💰 Fiyat bilgileri
• 📈 Yatırım tavsiyeleri
• 🏦 Kredi hesaplama
• 🏢 Site vs apartman
• 📐 Metrekare rehberi

Sormak istediğiniz bir şey var mı?"""

    # Varsayılan yanıt
    return """🤔 Sorunuzu tam anlayamadım. Şunları sorabilirsiniz:

• "Kadıköy'de fiyatlar nasıl?"
• "Hangi ilçeye yatırım yapmalıyım?"
• "Konut kredisi faizleri nedir?"
• "Site mi apartman mı?"
• "3+1 daire kaç m²?"

Ya da direkt bir ilçe adı yazabilirsiniz!"""

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        mesaj = data.get('mesaj', '')
        
        if not mesaj:
            return jsonify({'success': False, 'error': 'Mesaj boş olamaz'}), 400
        
        yanit = chatbot_yanit(mesaj)
        
        return jsonify({
            'success': True,
            'yanit': yanit
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000)
