import tkinter as tk
from tkinter import messagebox

def simulationStarten(stromVerbrauch, pvErzeugung, windErzeugung,fenster, ausgabeLabel, ausgabeStatus):
    # Die eingaben aus den Feldern herholen + eingabe wird als String geliefert: muss gecastet werden!
    try:
        userEingabeStromVerbrauch = float(stromVerbrauch.get())
        userEingabePvErzeugung = float(pvErzeugung.get())
        userEingabeWindErzeugung = float(windErzeugung.get())
    except ValueError:
        messagebox.showerror(
        "Ungültige Eingabe",
        "Bitte gib in allen Feldern gültige Zahlen ein!"
        )
        return

    



    pEEGesamt = userEingabePvErzeugung + userEingabeWindErzeugung
    if userEingabeStromVerbrauch > 0:
        anteilEEinProzent = pEEGesamt/userEingabeStromVerbrauch *100
    else:
        anteilEEinProzent = 0
        messagebox.showerror(
                "Ungültige Eingabe",
                "Der Stromverbrauch muss größer 0 sein!"
                )
        return
    
    pBilanz = pEEGesamt - userEingabeStromVerbrauch
    pDefizit = max(0,-pBilanz)
    pÜberschuss = max(0,pBilanz)

    ausgabetext = (
        f"Ergebnisse\n"
        f"EE Gesamt: {pEEGesamt:.2f} GW\n"
        f"EE Anteil: {anteilEEinProzent:.1f} %\n"
        f"Bilanz: {pBilanz:.2f} GW\n"
        f"Defizit: {pDefizit:.2f} GW\n"
        f"Überschuss: {pÜberschuss:.2f} GW\n"
    )

    ausgabeLabel.config(text=ausgabetext)


    if pBilanz > 0:
        ausgabeStatus.config(text="Status: Stromüberschuss")
    elif pBilanz < 0:
        ausgabeStatus.config(text="Status: Stromdefizit")
    else:
        ausgabeStatus.config(text="Status: Erzeugung und Verbrauch ausgeglichen")


