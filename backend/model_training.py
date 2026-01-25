import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import joblib

# 1. Veriyi Yükle
df = pd.read_csv('data/cleaned_house_data.csv')

# 2. Uç Değerleri Temizle - İlçe Bazlı IQR Yöntemi
def temizle_ilce_bazli(df):
    """Her ilçe için ayrı ayrı aykırı değerleri temizle"""
    df['m2_fiyat'] = df['Fiyatı'] / df['Metrekare']
    temiz_df = []
    
    for ilce in df['İlçe'].unique():
        ilce_df = df[df['İlçe'] == ilce].copy()
        m2 = ilce_df['m2_fiyat']
        q1, q3 = m2.quantile(0.10), m2.quantile(0.90)
        iqr = q3 - q1
        low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
        ilce_df = ilce_df[(m2 >= low) & (m2 <= high)]
        temiz_df.append(ilce_df)
    
    return pd.concat(temiz_df, ignore_index=True)

df = temizle_ilce_bazli(df)
print(f"Aykırı değer temizliği sonrası: {len(df)} kayıt")

# 3. İlçe bazlı fiyat ortalaması ekle (lokasyon gücü)
ilce_ortalama = df.groupby('İlçe')['Fiyatı'].mean().to_dict()
df['İlçe_Gücü'] = df['İlçe'].map(ilce_ortalama)

# 4. Yeni Özellik: Lüks Katsayısı (İlçe Gücü x Site İçi)
df['Luks_Katsayisi'] = df['İlçe_Gücü'] * df['Site_Icerisinde']

# 5. Özellikleri Seç (Luks_Katsayisi eklendi)
X = df[['Metrekare', 'Oda_Sayısı', 'Binanın_Yaşı', 'İlçe_Kod', 
        'Oda_Metrekare', 'Yaş_Grup', 'Metrekare_Log', 'Oda_Sayisi_Log',
        'Metrekare_x_Oda', 'Yas_x_Metrekare', 'İlçe_Gücü',
        'Site_Icerisinde', 'Bulundugu_Kat', 'Giris_Kat_Mi', 'Site_Bonus',
        'Kat_Orani', 'Isitma_Skoru', 'İlçe_Oda_Gücü', 'Luks_Katsayisi']]

# 6. Logaritmik Hedef Dönüşümü (Fiyat normalleştirme)
y = np.log1p(df['Fiyatı'])  # log(1 + fiyat)

# Farklı random_state ile test (daha güvenilir sonuç)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=123)

# 7. Modelleri Eğit
rf_model = RandomForestRegressor(
    n_estimators=1000, 
    max_depth=30, 
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)

gb_model = GradientBoostingRegressor(
    n_estimators=1000, 
    max_depth=15, 
    learning_rate=0.05,
    subsample=0.8,
    min_samples_split=2,
    random_state=42
)

lr_model = LinearRegression()

print("-" * 40)
print("YAPAY ZEKA TEKNİKLERİ KARŞILAŞTIRMA")
print("-" * 40)

# Her modeli eğit
rf_model.fit(X_train, y_train)
gb_model.fit(X_train, y_train)
lr_model.fit(X_train, y_train)

# Tahminler (log space'de)
rf_pred = rf_model.predict(X_test)
gb_pred = gb_model.predict(X_test)
lr_pred = lr_model.predict(X_test)

# 8. Stacking: RF + GB ortalaması
stacked_pred = (rf_pred + gb_pred) / 2

# Skorları hesapla (log space'de)
rf_score = r2_score(y_test, rf_pred)
gb_score = r2_score(y_test, gb_pred)
lr_score = r2_score(y_test, lr_pred)
stacked_score = r2_score(y_test, stacked_pred)

# Gerçek fiyat space'ine dönüştür
y_test_real = np.expm1(y_test)
rf_pred_real = np.expm1(rf_pred)
gb_pred_real = np.expm1(gb_pred)
lr_pred_real = np.expm1(lr_pred)
stacked_pred_real = np.expm1(stacked_pred)

# Tüm metrikleri hesapla (Gerçek fiyatlar üzerinden)
def hesapla_metrikler(y_true, y_pred, model_adi):
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    return {
        'Model': model_adi,
        'R²': r2,
        'MAE': mae,
        'RMSE': rmse,
        'MAPE (%)': mape
    }

# Her model için metrikler
metrikler = [
    hesapla_metrikler(y_test_real, lr_pred_real, 'Linear Regression'),
    hesapla_metrikler(y_test_real, rf_pred_real, 'Random Forest'),
    hesapla_metrikler(y_test_real, gb_pred_real, 'Gradient Boosting'),
    hesapla_metrikler(y_test_real, stacked_pred_real, 'Stacked (RF+GB)')
]

# Sonuçları yazdır
print("\n" + "=" * 100)
print("MODEL KARŞILAŞTIRMA TABLOSU")
print("=" * 100)
print(f"{'Model':<25} {'R² Skoru':<15} {'MAE (TL)':<20} {'RMSE (TL)':<20} {'MAPE (%)':<15}")
print("-" * 100)

for m in metrikler:
    print(f"{m['Model']:<25} {m['R²']:.4f}         {m['MAE']:>15,.0f}    {m['RMSE']:>15,.0f}    {m['MAPE (%)']:>10.2f}%")

print("=" * 100)

# En iyi modeli bul (R² bazlı)
scores = {
    'Linear Regression': r2_score(y_test_real, lr_pred_real),
    'Random Forest': r2_score(y_test_real, rf_pred_real),
    'Gradient Boosting': r2_score(y_test_real, gb_pred_real),
    'Stacked (RF+GB)': r2_score(y_test_real, stacked_pred_real)
}
best_name = max(scores, key=scores.get)
best_r2 = scores[best_name]

# Metrik açıklamaları
print("\n📊 METRİK AÇIKLAMALARI:")
print("-" * 50)
print("R² (Determination Coefficient): Modelin veriyi ne kadar iyi açıkladığı (1'e yakın = iyi)")
print("MAE (Mean Absolute Error): Ortalama mutlak hata (TL cinsinden)")
print("RMSE (Root Mean Squared Error): Karekök ortalama kare hatası (büyük hatalara hassas)")
print("MAPE (Mean Absolute Percentage Error): Ortalama yüzdesel hata")

# 9. Modelleri Kaydet (Stacking için ikisini de kaydet)
joblib.dump(rf_model, 'models/rf_model.pkl')
joblib.dump(gb_model, 'models/gb_model.pkl')
joblib.dump(ilce_ortalama, 'models/ilce_dict.pkl')

print("\n" + "=" * 50)
print(f"🏆 EN BAŞARILI MODEL: {best_name}")
print(f"📈 En İyi R² Skoru: %{best_r2*100:.2f}")
print("=" * 50)
print("\n✅ Modeller 'models/' klasörüne kaydedildi.")
