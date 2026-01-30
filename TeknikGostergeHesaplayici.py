import pandas as pd

class TeknikGostergeHesaplayici:
    def __init__(self, df: pd.DataFrame, close_col="close", timeframe="1d"):
        self.df = df.copy()
        self.close_col = close_col
        self.timeframe = timeframe.lower()
        self._set_parametreler()

    def _set_parametreler(self):
        """Zaman dilimine göre gösterge parametrelerini ayarla"""
        if self.timeframe == "1h":
            self.rsi_period = 14
            self.bb_period = 20
            self.macd_fast = 12
            self.macd_slow = 26
            self.macd_signal = 9
        elif self.timeframe == "1d":
            self.rsi_period = 14
            self.bb_period = 20
            self.macd_fast = 12
            self.macd_slow = 26
            self.macd_signal = 9
        else:
            raise ValueError("Desteklenmeyen zaman dilimi: '1h' veya '1d' kullanın.")

    def hesapla_macd(self):
        ema_fast = self.df[self.close_col].ewm(span=self.macd_fast, adjust=False).mean()
        ema_slow = self.df[self.close_col].ewm(span=self.macd_slow, adjust=False).mean()
        self.df["MACD"] = ema_fast - ema_slow
        self.df["MACD_Signal"] = self.df["MACD"].ewm(span=self.macd_signal, adjust=False).mean()
        self.df["MACD_Histogram"] = self.df["MACD"] - self.df["MACD_Signal"]

    def hesapla_rsi(self):
        delta = self.df[self.close_col].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=self.rsi_period).mean()
        avg_loss = loss.rolling(window=self.rsi_period).mean()

        rs = avg_gain / avg_loss
        self.df["RSI"] = 100 - (100 / (1 + rs))

    def hesapla_bollinger(self):
        sma = self.df[self.close_col].rolling(window=self.bb_period).mean()
        std = self.df[self.close_col].rolling(window=self.bb_period).std()

        self.df["BB_Middle"] = sma
        self.df["BB_Upper"] = sma + (2 * std)
        self.df["BB_Lower"] = sma - (2 * std)

    def tumunu_hesapla(self):
        self.hesapla_macd()
        self.hesapla_rsi()
        self.hesapla_bollinger()
        return self.df
    


# df = pd.read_csv("Veriler/btcusdt_2017.csv")  # 'Close' sütunu içermeli
# gosterge = TeknikGostergeHesaplayici(df, timeframe="1d")
# df_sonuc = gosterge.tumunu_hesapla()

# print(df_sonuc.to_csv("kaydet.csv"))