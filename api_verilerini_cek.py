import os
import time
import datetime
import requests
import pandas as pd

class ApiVerileriEdin:
    def __init__(self, service=None):
        self.service = service

    def tarihleri_timestamp_yap(self, start_date_str: str, end_date_str: str) -> tuple:
        start_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        start_ts = int(time.mktime(start_dt.timetuple()) * 1000)
        end_ts = int(time.mktime(end_dt.timetuple()) * 1000)
        print(start_ts)
        print(end_ts)
        return start_ts, end_ts

    def yillik_verileri_cek_ve_kaydet(self, baslangic_yili: int, bitis_yili: int, sembol="BTCUSDT", klasor="Veriler"):
        os.makedirs(klasor, exist_ok=True)

        for yil in range(baslangic_yili, bitis_yili + 1):
            start_date = f"{yil}-01-01"
            end_date = f"{yil + 1}-01-01"

            start_ts, end_ts = self.tarihleri_timestamp_yap(start_date, end_date)

            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": sembol,
                "interval": "1d",
                "startTime": start_ts,
                "endTime": end_ts
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if not data:
                    print(f"{yil} yılı için veri bulunamadı.")
                    continue

                columns = [
                    "timestamp", "open", "high", "low", "close", "volume",
                    "close_time", "quote_asset_volume", "num_trades",
                    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
                ]
                df = pd.DataFrame(data, columns=columns)
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                df["close"] = df["close"].astype(float)

                dosya_adi = f"{klasor}/{sembol.lower()}_{yil}.csv"
                df.to_csv(dosya_adi, index=False)
                print(f"{yil} verisi kaydedildi: {dosya_adi}")
            else:
                print(f"{yil} verisi alınamadı. Hata kodu: {response.status_code}")

    def saatlik_verileri_cek_ve_kaydet(self, baslangic_tarihi: str, bitis_tarihi: str, sembol="BTCUSDT", klasor="SaatlikVeriler"):
        os.makedirs(klasor, exist_ok=True)

        start_dt = datetime.datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(bitis_tarihi, "%Y-%m-%d")

        gun_sayisi = (end_dt - start_dt).days

        for i in range(gun_sayisi):
            gun_baslangic = start_dt + datetime.timedelta(days=i)
            gun_bitis = gun_baslangic + datetime.timedelta(days=1)

            start_ts = int(gun_baslangic.timestamp() * 1000)
            end_ts = int(gun_bitis.timestamp() * 1000)

            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": sembol,
                "interval": "1h",  # Saatlik veri
                "startTime": start_ts,
                "endTime": end_ts
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if not data:
                    print(f"{gun_baslangic.date()} için veri bulunamadı.")
                    continue

                columns = [
                    "timestamp", "open", "high", "low", "close", "volume",
                    "close_time", "quote_asset_volume", "num_trades",
                    "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
                ]
                df = pd.DataFrame(data, columns=columns)
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                df["close"] = df["close"].astype(float)

                dosya_adi = f"{klasor}/{sembol.lower()}_{gun_baslangic.date()}.csv"
                df.to_csv(dosya_adi, index=False)
                print(f"{gun_baslangic.date()} verisi kaydedildi: {dosya_adi}")
                
            else:
                with open("istek_log.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"Tarih: {gun_baslangic.date()} | Start: {start_ts} | End: {end_ts}\n")






ApiVerileriEdin().saatlik_verileri_cek_ve_kaydet(baslangic_tarihi="2018-01-06",bitis_tarihi="2025-11-21")

