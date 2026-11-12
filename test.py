import pandas as pd

df = pd.read_csv(
    "data/bereinigt/SMARD_Gesamt_Bereinigt.csv",
    sep=";",
    decimal=",",
    thousands=".",
    na_values=["-"],
)
print(df.loc[df["EE_Anteil"].idxmin(), ["Datum von", "EE_Anteil"]])