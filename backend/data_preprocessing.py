import pandas as pd
import numpy as np

# 1. Verileri Yükle
df_emlak = pd.read_csv('data/Real Estate in ISTANBUL (Emlakjet).csv')
df_chatbot = pd.read_csv('data/chatbot_data.csv')

# Sütun isimlerini temizle
df_emlak.columns = df_emlak.columns.str.strip()
df_chatbot.columns = df_chatbot.columns.str.strip()

print(f"Emlakjet: {len(df_emlak)} satır, Chatbot: {len(df_chatbot)} satır")

# 2. Emlakjet Verisi Hazırlığı (Eksik sütunları varsayılanla ekliyoruz)
df_emlak = df_emlak[['İlçe', 'Brüt_Metrekare', 'Oda_Sayısı', 'Binanın_Yaşı', 'Fiyatı']].copy()
df_emlak.columns = ['İlçe', 'Metrekare', 'Oda_Sayısı', 'Binanın_Yaşı', 'Fiyatı']
df_emlak['Site_Icerisinde'] = 'Hayır'  # Varsayılan değer
df_emlak['Bulundugu_Kat'] = 3           # Ortalama bir kat
df_emlak['Kat_Sayisi'] = 8              # Varsayılan kat sayısı
df_emlak['Isitma_Tipi'] = 'Doğalgaz'    # Varsayılan ısıtma
df_emlak['Veri_Kaynagi'] = 'Emlakjet'   # Kaynak işareti

# 3. Chatbot Verisi Hazırlığı (Sütunları eksiksiz alıyoruz)
df_chatbot = df_chatbot[['Ilce', 'Brut_Metrekare', 'Oda_Sayisi', 'Bina_Yasi', 'Fiyat', 'Site_Icerisinde', 'Bulundugu_Kat', 'Kat_Sayisi', 'Isitma_Tipi']].copy()
df_chatbot.columns = ['İlçe', 'Metrekare', 'Oda_Sayısı', 'Binanın_Yaşı', 'Fiyatı', 'Site_Icerisinde', 'Bulundugu_Kat', 'Kat_Sayisi', 'Isitma_Tipi']
df_chatbot['Veri_Kaynagi'] = 'Chatbot'  # Kaynak işareti

# 4. Birleştir ve İlçe Temizle
df = pd.concat([df_emlak, df_chatbot], ignore_index=True)
df['İlçe'] = df['İlçe'].str.split('(').str[0].str.strip()  # Parantez temizliği
print(f"Birleştirilmiş toplam: {len(df)} satır")

# 5. Site, Kat ve Isıtma Temizleme
df['Site_Icerisinde'] = df['Site_Icerisinde'].map({'Evet': 1, 'Hayır': 0}).fillna(0)
df['Bulundugu_Kat'] = pd.to_numeric(df['Bulundugu_Kat'], errors='coerce').fillna(3)
df['Kat_Sayisi'] = pd.to_numeric(df['Kat_Sayisi'], errors='coerce').fillna(8)

# Isıtma Tipi Skorlama (Doğalgaz: 1, Merkezi: 0.5, Diğer: 0)
def isitma_skoru(x):
    if pd.isna(x):
        return 0.5
    x = str(x).strip().lower()
    if 'doğalgaz' in x or 'dogalgaz' in x or 'kombi' in x:
        return 1.0
    elif 'merkezi' in x:
        return 0.5
    else:
        return 0.0

df['Isitma_Skoru'] = df['Isitma_Tipi'].apply(isitma_skoru)

# 5. Yaş Temizleme
def clean_age(x):
    if pd.isna(x):
        return 10.0
    x = str(x).strip().lower()
    if '21' in x or 'üzeri' in x:
        return 30.0
    if '-' in x:
        try:
            parts = x.split('-')
            return (float(parts[0]) + float(parts[1])) / 2
        except:
            return 10.0
    try:
        return float(x)
    except:
        return 10.0

df['Binanın_Yaşı'] = df['Binanın_Yaşı'].apply(clean_age)

# 6. Oda Temizleme
def clean_room(x):
    if pd.isna(x):
        return 3.0
    x = str(x).lower().strip()
    if '+' in x:
        try:
            parts = x.split('+')
            return float(parts[0]) + float(parts[1])
        except:
            return 3.0
    try:
        return float(x)
    except:
        return 3.0

df['Oda_Sayısı'] = df['Oda_Sayısı'].apply(clean_room)

# 7. Fiyat Temizleme
def clean_price(x):
    if pd.isna(x):
        return np.nan
    # Zaten float ise doğrudan döndür
    if isinstance(x, (int, float)):
        return float(x)
    # String ise temizle (Emlakjet formatı: "18.000.000" veya "18000000")
    x = str(x).replace(" ", "").replace("TL", "").strip()
    # Eğer ondalık nokta varsa (1234.0 gibi), bunu koru
    if x.count('.') == 1 and x.split('.')[-1].isdigit() and len(x.split('.')[-1]) <= 2:
        try:
            return float(x)
        except:
            pass
    # Türk formatı: binlik ayraç olarak nokta (18.000.000 -> 18000000)
    x = x.replace(".", "").replace(",", "")
    try:
        return float(x)
    except:
        return np.nan

df['Fiyatı'] = df['Fiyatı'].apply(clean_price)

# 8. Metrekare Temizleme
df['Metrekare'] = pd.to_numeric(df['Metrekare'], errors='coerce')

# 9. Anomali ve eksik temizliği
df = df.dropna(subset=['Fiyatı', 'Metrekare', 'Oda_Sayısı', 'Binanın_Yaşı'])
df = df[df['Metrekare'] > 20]
df = df[df['Fiyatı'] > 100000]
df = df[(df['Fiyatı'] / df['Metrekare']) < 700000]  # Pahalı ilçeler için artırıldı

# 10. Feature Engineering (Geliştirilmiş)
df['İlçe'] = df['İlçe'].str.strip()
df['İlçe_Kod'] = df['İlçe'].astype('category').cat.codes
df['Oda_Metrekare'] = df['Metrekare'] / (df['Oda_Sayısı'] + 0.1)
df['Yaş_Grup'] = pd.cut(df['Binanın_Yaşı'], bins=[-1, 5, 10, 20, 100], labels=[0, 1, 2, 3]).astype(str).astype(int)
df['Metrekare_Log'] = np.log1p(df['Metrekare'])
df['Oda_Sayisi_Log'] = np.log1p(df['Oda_Sayısı'])
df['Metrekare_x_Oda'] = df['Metrekare'] * df['Oda_Sayısı']
df['Yas_x_Metrekare'] = df['Binanın_Yaşı'] * df['Metrekare']

# İlçe bazlı fiyat gücü (parantezlerden temizlenmiş isimlerle)
ilce_ortalama = df.groupby('İlçe')['Fiyatı'].mean().to_dict()
df['İlçe_Gücü'] = df['İlçe'].map(ilce_ortalama)

# Kat Farkı: Giriş katlar genellikle daha ucuzdur
df['Giris_Kat_Mi'] = df['Bulundugu_Kat'].apply(lambda x: 1 if x <= 0 else 0)

# Site içi bonus
df['Site_Bonus'] = df['Site_Icerisinde'] * df['Metrekare']

# Kat Oranı: Bulunduğu kat / Toplam kat sayısı (konum değeri)
df['Kat_Orani'] = df['Bulundugu_Kat'] / (df['Kat_Sayisi'] + 0.1)
df['Kat_Orani'] = df['Kat_Orani'].clip(0, 1)  # 0-1 arasında tut

# İlçe + Oda Sayısı kombinasyonu target encoding (segment bazlı)
df['Ilce_Oda_Key'] = df['İlçe'] + '_' + df['Oda_Sayısı'].astype(int).astype(str)
ilce_oda_ortalama = df.groupby('Ilce_Oda_Key')['Fiyatı'].mean().to_dict()
df['İlçe_Oda_Gücü'] = df['Ilce_Oda_Key'].map(ilce_oda_ortalama)

# Son temizlik
df = df.dropna()

df.to_csv('data/cleaned_house_data.csv', index=False)
print(f"Ön işleme başarıyla tamamlandı! Toplam {len(df)} kayıt işlendi.")
