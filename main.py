import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from methotlar import Methodlar
from TeknikGostergeHesaplayici import TeknikGostergeHesaplayici

# CSV dosyalarını birleştir

met = Methodlar()
df = met.csvleri_birlestir(klasor_yolu="SaatlikVeriler")
tekHesap = TeknikGostergeHesaplayici(df=df,timeframe="1h")
df = tekHesap.tumunu_hesapla()
print(df.columns)
# print(df.head(30))
df=df.dropna()
# print("------------------------------------------")
# print(df.head(30))
# Girdi sütunları
features = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "MACD",
    "MACD_Signal",
    "MACD_Histogram",
    "RSI",
    "BB_Middle",
    "BB_Upper",
    "BB_Lower",
]
data = df[features].values

# Tüm sütunlar için scaler (X için)
scaler_all = MinMaxScaler()
data_scaled = scaler_all.fit_transform(data)

# Sadece 'close' için ayrı scaler (y için)
scaler_close = MinMaxScaler()
close_scaled = scaler_close.fit_transform(df[["close"]].values)

# X: geçmiş 3 günün tüm özellikleri, y: ertesi günün 'close' değeri
X, y = [], []
for i in range(3, len(data_scaled)):
    X.append(data_scaled[i - 3 : i])  # 3 gün boyunca tüm özellikler
    y.append(close_scaled[i, 0])  # sadece 'close' scaled değeri

X, y = np.array(X), np.array(y)
print(f"x uzunluk = {len(X)}")
print(f"y uzunluk = {len(y)}")

# Eğitim ve test ayrımı
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Model oluşturma
model = Sequential()
model.add(LSTM(units=50, return_sequences=False, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(1))  # sadece 'close' tahmini
model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(X_train, y_train, epochs=200, batch_size=200, verbose=2)

# Tahmin
y_pred = model.predict(X_test)

# Doğru geri dönüşüm (inverse_transform)
y_pred_inv = scaler_close.inverse_transform(y_pred)
y_test_inv = scaler_close.inverse_transform(y_test.reshape(-1, 1))

# Görselleştirme
plt.figure(figsize=(10, 5))
plt.plot(y_test_inv, label="Gerçek (USD)")
plt.plot(y_pred_inv, label="Tahmin (USD)")
plt.legend()
plt.title("Kapanış Fiyatı Tahmini")
plt.xlabel("Zaman")
plt.ylabel("Fiyat (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Hata hesaplama
mae = mean_absolute_error(y_test_inv, y_pred_inv)
mape = mean_absolute_percentage_error(y_test_inv, y_pred_inv) * 100
print(f"Gerçek fiyat bazında ortalama mutlak hata (MAE): {mae:.2f} USD")
print(f"Ortalama yüzde hata (MAPE): {mape:.2f}%")

# Hata çizgisi
plt.figure(figsize=(10, 3))
plt.plot(y_test_inv - y_pred_inv, label="Hata (Gerçek - Tahmin)")
plt.axhline(0, color="gray", linestyle="--")
plt.title("Tahmin Hatası")
plt.legend()
plt.tight_layout()
plt.show()

# Model özeti
model.summary()
