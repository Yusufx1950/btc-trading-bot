import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib

from methotlar import Methodlar
from TeknikGostergeHesaplayici import TeknikGostergeHesaplayici

# -----------------------------
# 1. Veri Hazırlama
# -----------------------------
met = Methodlar()
df = met.csvleri_birlestir(klasor_yolu="SaatlikVeriler")
tekHesap = TeknikGostergeHesaplayici(df=df, timeframe="1h")
df = tekHesap.tumunu_hesapla()
df = df.dropna()

# Getiri (return) hesapla
df["return"] = df["close"].pct_change()
df = df.dropna()

# Girdi sütunları
features = [
    "open", "high", "low", "close", "volume",
    "MACD", "MACD_Signal", "MACD_Histogram",
    "RSI", "BB_Middle", "BB_Upper", "BB_Lower"
]

data = df[features].values

# Tüm sütunlar için scaler (X için)
scaler_all = MinMaxScaler()
data_scaled = scaler_all.fit_transform(data)

# Return için ayrı scaler (y için)
scaler_return = MinMaxScaler()
return_scaled = scaler_return.fit_transform(df[["return"]].values)

# -----------------------------
# 2. X ve y oluşturma
# -----------------------------
window_size = 30  # daha uzun pencere
X, y = [], []
for i in range(window_size, len(data_scaled)):
    X.append(data_scaled[i - window_size : i])  # geçmiş N gün
    y.append(return_scaled[i, 0])  # ertesi günün return değeri

X, y = np.array(X), np.array(y)
print(f"x uzunluk = {len(X)}")
print(f"y uzunluk = {len(y)}")

# -----------------------------
# 3. Eğitim/Test ayrımı
# -----------------------------
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# -----------------------------
# 4. Model oluşturma
# -----------------------------
model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(32))
model.add(Dense(1, activation="linear"))  # return tahmini

model.compile(optimizer="adam", loss="mean_squared_error")

# EarlyStopping
es = EarlyStopping(monitor="val_loss", patience=20, restore_best_weights=True)

 
# 5. Model eğitimi
 
history = model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=64,
    validation_split=0.1,
    callbacks=[es],
    verbose=2
)

 
# 6. Tahmin
 
y_pred = model.predict(X_test)

# inverse transform
y_pred_inv = scaler_return.inverse_transform(y_pred)
y_test_inv = scaler_return.inverse_transform(y_test.reshape(-1, 1))

 
# 7. Fiyatı geri hesaplama
# Test setindeki ilk gerçek fiyat
start_price = df["close"].iloc[train_size + window_size]

# Gerçek fiyat serisi
real_returns = y_test_inv.flatten()
real_prices = [start_price]
for r in real_returns:
    real_prices.append(real_prices[-1] * (1 + r))
real_prices = np.array(real_prices[1:])

# Tahmin fiyat serisi
pred_returns = y_pred_inv.flatten()
pred_prices = [start_price]
for r in pred_returns:
    pred_prices.append(pred_prices[-1] * (1 + r))
pred_prices = np.array(pred_prices[1:])

 
# 8. Görselleştirme
plt.figure(figsize=(12, 6))
plt.plot(real_prices, label="Gerçek Fiyat (USD)")
plt.plot(pred_prices, label="Tahmin Fiyat (USD)")
plt.legend()
plt.title("Return Bazlı Kapanış Fiyatı Tahmini")
plt.xlabel("Zaman")
plt.ylabel("Fiyat (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()

 
# 9. Hata metrikleri
 
mae = mean_absolute_error(real_prices, pred_prices)
mape = mean_absolute_percentage_error(real_prices, pred_prices) * 100
rmse = np.sqrt(mean_squared_error(real_prices, pred_prices))

print(f"Gerçek fiyat bazında MAE: {mae:.2f} USD")
print(f"Gerçek fiyat bazında MAPE: {mape:.2f}%")
print(f"Gerçek fiyat bazında RMSE: {rmse:.2f} USD")

 
# 10. Model ve scaler kaydetme
model.save("lstm_return_model.h5")
joblib.dump(scaler_all, "scaler_all.pkl")
joblib.dump(scaler_return, "scaler_return.pkl")
