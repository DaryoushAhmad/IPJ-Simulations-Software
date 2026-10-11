import tkinter as tk
from tkinter import messagebox

def simulationStarten(stromVerbrauch, pvErzeugung, windErzeugung,fenster):
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

    ausgabe = tk.Label(fenster, text=ausgabetext, justify="left" )
    ausgabe.pack(pady=10)

    if pBilanz > 0:
        tk.Label(fenster, text="Status: Stromüberschuss").pack()
    elif pBilanz < 0:
        tk.Label(fenster, text="Status: Stromdefizit").pack()
    else:
        tk.Label(fenster, text="Status: Erzeugung und Verbrauch ausgeglichen").pack()

