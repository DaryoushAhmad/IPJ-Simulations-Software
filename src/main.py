import tkinter as tk
from Funktionen import simulationStarten #Import der Funktion "simulationStarten" aus dem Ordner "Funktionen"
from BerechnungsFunktionen import haeufigkeitsverteilung_EE



#Fenster Einrichten

fenster = tk.Tk()   #Erstellen des Hauptfensters

fenster.title("Energiesystem-Simulator V0.1")   # Fenstertitel festlegen
fenster.geometry("500x550") # Fenstergröße bestimmen



beschriftungStromverbrauch = tk.Label(fenster, text="Stromverbrauch [GW]:")
beschriftungStromverbrauch.pack() #sorgt dafür das es im Fenster angezeigt wird
eingabefeldStromverbrauch = tk.Entry(fenster)
eingabefeldStromverbrauch.pack()



beschriftungPvErzeugung = tk.Label(fenster, text="PV-Erzeugung [GW]:")
beschriftungPvErzeugung.pack()
eingabefeldPvErzeugung = tk.Entry(fenster)
eingabefeldPvErzeugung.pack()


beschriftungWindErzeugung = tk.Label(fenster, text="Wind-Erzeugung [GW]:")
beschriftungWindErzeugung.pack()
eingabefeldWindErzeugung = tk.Entry(fenster)
eingabefeldWindErzeugung.pack()

ausgabeLabel = tk.Label(fenster)
ausgabeLabel.pack(pady=10)
ausgabeStatus = tk.Label(fenster,text="Status:")
ausgabeStatus.pack(pady=10)

button = tk.Button(fenster,
                   text="Simulation starten",   #Name des Buttons
                   command=lambda: simulationStarten(eingabefeldStromverbrauch  #lambda sorgt dafür das die funktion erst nach dem Klick ausgeführt wird und nicht sofort
                                                     ,eingabefeldPvErzeugung
                                                     ,eingabefeldWindErzeugung
                                                     ,fenster
                                                     ,ausgabeLabel
                                                     ,ausgabeStatus))   #Welche Funktion ausgeführt werden soll
button.pack()

haeufigkeitsverteilung_EE()


fenster.mainloop()  # Startet die Ereignesverarbeitung des Fensters(Immer zum Ende)
    