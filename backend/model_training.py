import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = 'DejaVu Sans'

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

print("-" * 60)
print("🔍 RANDOMIZED SEARCH CV İLE HİPERPARAMETRE OPTİMİZASYONU")
print("-" * 60)

# ============================================
# RANDOM FOREST - RandomizedSearchCV
# ============================================
print("\n📊 Random Forest optimizasyonu başlıyor...")

rf_param_dist = {
    'n_estimators': [500, 800, 1000, 1200],
    'max_depth': [20, 25, 30, 35, None],
    'min_samples_split': [2, 3, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2', 0.3, 0.5]
}

rf_base = RandomForestRegressor(random_state=42, n_jobs=-1)

rf_search = RandomizedSearchCV(
    rf_base,
    param_distributions=rf_param_dist,
    n_iter=20,  # 20 farklı kombinasyon dene
    cv=5,       # 5-fold cross validation
    scoring='r2',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

rf_search.fit(X_train, y_train)
rf_model = rf_search.best_estimator_

print(f"\n✅ RF En İyi Parametreler: {rf_search.best_params_}")
print(f"✅ RF En İyi CV Skoru: {rf_search.best_score_:.4f}")

# ============================================
# GRADIENT BOOSTING - RandomizedSearchCV
# ============================================
print("\n📊 Gradient Boosting optimizasyonu başlıyor...")

gb_param_dist = {
    'n_estimators': [500, 800, 1000],
    'max_depth': [10, 15, 20],
    'learning_rate': [0.01, 0.03, 0.05, 0.1],
    'subsample': [0.7, 0.8, 0.9],
    'min_samples_split': [2, 3, 5]
}

gb_base = GradientBoostingRegressor(random_state=42)

gb_search = RandomizedSearchCV(
    gb_base,
    param_distributions=gb_param_dist,
    n_iter=15,  # 15 farklı kombinasyon dene
    cv=3,       # 3-fold (GB daha yavaş)
    scoring='r2',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

gb_search.fit(X_train, y_train)
gb_model = gb_search.best_estimator_

print(f"\n✅ GB En İyi Parametreler: {gb_search.best_params_}")
print(f"✅ GB En İyi CV Skoru: {gb_search.best_score_:.4f}")

# ============================================
# LINEAR REGRESSION (Baseline)
# ============================================
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

print("\n" + "=" * 60)
print("📈 TEST SETİ ÜZERİNDE DEĞERLENDİRME")
print("=" * 60)

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

# ============================================
# CONFUSION MATRIX - FİYAT ARALIKLARINA GÖRE
# ============================================
print("\n" + "=" * 60)
print("📊 CONFUSION MATRIX - FİYAT ARALIKLARINA GÖRE SINIFLANDIRMA")
print("=" * 60)

# Fiyatları kategorilere ayır
def fiyat_kategorisi(fiyat):
    if fiyat < 2_000_000:
        return "0-2M TL"
    elif fiyat < 5_000_000:
        return "2-5M TL"
    elif fiyat < 10_000_000:
        return "5-10M TL"
    elif fiyat < 20_000_000:
        return "10-20M TL"
    else:
        return "20M+ TL"

# Gerçek ve tahmin edilen kategoriler
y_true_cat = [fiyat_kategorisi(f) for f in y_test_real]
y_pred_cat = [fiyat_kategorisi(f) for f in stacked_pred_real]  # En iyi model: Stacked

# Kategori sırası
kategori_sirasi = ["0-2M TL", "2-5M TL", "5-10M TL", "10-20M TL", "20M+ TL"]

# Confusion Matrix hesapla
cm = confusion_matrix(y_true_cat, y_pred_cat, labels=kategori_sirasi)

# Classification Report
print("\n📋 SINIFLANDIRMA RAPORU (Stacked Model):")
print("-" * 60)
print(classification_report(y_true_cat, y_pred_cat, labels=kategori_sirasi, zero_division=0))

# Confusion Matrix Görselleştirmesi
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 1. Confusion Matrix Heatmap
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=kategori_sirasi, 
            yticklabels=kategori_sirasi,
            ax=axes[0])
axes[0].set_xlabel('Tahmin Edilen Fiyat Aralığı', fontsize=12)
axes[0].set_ylabel('Gerçek Fiyat Aralığı', fontsize=12)
axes[0].set_title('Confusion Matrix - Fiyat Aralıkları\n(Stacked RF+GB Model)', fontsize=14, fontweight='bold')

# 2. Gerçek vs Tahmin Scatter Plot
axes[1].scatter(y_test_real / 1_000_000, stacked_pred_real / 1_000_000, alpha=0.5, edgecolors='black', linewidth=0.5)
max_val = max(y_test_real.max(), stacked_pred_real.max()) / 1_000_000
axes[1].plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Mükemmel Tahmin')
axes[1].set_xlabel('Gerçek Fiyat (Milyon TL)', fontsize=12)
axes[1].set_ylabel('Tahmin Edilen Fiyat (Milyon TL)', fontsize=12)
axes[1].set_title(f'Gerçek vs Tahmin Karşılaştırması\nR² = {stacked_score:.4f}', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('models/confusion_matrix_ve_tahmin.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Confusion Matrix görseli 'models/confusion_matrix_ve_tahmin.png' olarak kaydedildi.")

# Doğruluk Oranı (Aynı kategoriye düşme)
dogru_tahmin = sum([1 for t, p in zip(y_true_cat, y_pred_cat) if t == p])
toplam = len(y_true_cat)
dogruluk = dogru_tahmin / toplam * 100

print(f"\n📊 FİYAT ARALIĞI DOĞRULUK ORANI: %{dogruluk:.1f}")
print(f"   ({dogru_tahmin}/{toplam} konut doğru aralıkta tahmin edildi)")

# Bir komşu kategoriye tolerans (1 aralık sapma kabul edilebilir)
kategori_index = {k: i for i, k in enumerate(kategori_sirasi)}
yakin_tahmin = sum([1 for t, p in zip(y_true_cat, y_pred_cat) 
                    if abs(kategori_index[t] - kategori_index[p]) <= 1])
yakin_dogruluk = yakin_tahmin / toplam * 100

print(f"\n📊 ±1 ARALIK TOLERANSLI DOĞRULUK: %{yakin_dogruluk:.1f}")
print(f"   ({yakin_tahmin}/{toplam} konut ±1 aralık içinde tahmin edildi)")
