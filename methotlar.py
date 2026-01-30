import os
import pandas as pd

class Methodlar:
    def __init__(self, service=None):
        self.service = service

    def klasordeki_csv_dosyalari(self, klasor_yolu):
        csv_listesi = []
        for dosya_adi in os.listdir(klasor_yolu):
            if dosya_adi.endswith(".csv"):
                tam_yol = os.path.join(klasor_yolu, dosya_adi)
                csv_listesi.append(tam_yol)
        return csv_listesi

    def csvleri_birlestir(self, klasor_yolu):
        csv_yollari = self.klasordeki_csv_dosyalari(klasor_yolu)
        tum_veriler = []

        for yol in csv_yollari:
            try:
                df = pd.read_csv(yol)
                df["kaynak_dosya"] = os.path.basename(yol)
                tum_veriler.append(df)
            except Exception as e:
                print(f"Hata oluştu: {yol} → {e}")

        if tum_veriler:
            birlesik_df = pd.concat(tum_veriler, ignore_index=True)
            return birlesik_df
        else:
            return pd.DataFrame()
        

# m = Methodlar()
# klasor = "Veriler"
# df = m.csvleri_birlestir(klasor)

# print(df.count)