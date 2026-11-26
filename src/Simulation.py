from DataFunktionen import setUpErzeugerProfil
from DunkelflautenSimulation import simuliereDunkelflauten
import streamlit as st
#app starten: python -m streamlit run src/app.py

@st.cache_data(show_spinner=False)
def simuliere_ee(leistung_pv, leistung_onshore, leistung_offshore, leistung_biomasse, leistung_wasserkraft,verbrauchsReferenzJahr ,gesamtVerbrauchIn_TWh, zielJahr=2035 ):
    """Simuliert MWh je Viertelstunde aus installierten Leistungen in GW."""
    # Profilwerte in Prozent: / 100 * 1000 MW/GW * 0.25 h = Faktor 2.5.

    basisJahr = 2026
    dfSimulationen = {}
    zielLeistung_pv = leistung_pv
    zielLeistung_onshore = leistung_onshore
    zielLeistung_offshore = leistung_offshore
    zielLeistung_biomasse = leistung_biomasse
    zielLeistung_wasserkraft = leistung_wasserkraft
    anfangsLeistung_pv = 133.3
    anfangsLeistung_onshore = 72.29
    anfangsLeistung_offshore = 11.69
    anfangsLeistung_biomasse = 9.04
    anfangsLeistung_wasserkraft = 5.32
    # Quelle: https://www.energy-charts.info/charts/installed_power/chart.htm?l=en


    steigungLeistung_pv = (
        (zielLeistung_pv - anfangsLeistung_pv)
        / (zielJahr - basisJahr)
    )

    steigungLeistung_onshore = (
        (zielLeistung_onshore - anfangsLeistung_onshore)
        / (zielJahr - basisJahr)
    )

    steigungLeistung_offshore = (
        (zielLeistung_offshore - anfangsLeistung_offshore)
        / (zielJahr - basisJahr)
    )

    steigungLeistung_biomasse = (
        (zielLeistung_biomasse - anfangsLeistung_biomasse)
        / (zielJahr - basisJahr)
    )

    steigungLeistung_wasserkraft = (
        (zielLeistung_wasserkraft - anfangsLeistung_wasserkraft)
        / (zielJahr - basisJahr)
    )

    for jahr in range(2027, zielJahr + 1):
        leistung_pv = (
            anfangsLeistung_pv
            + ( jahr - basisJahr) * steigungLeistung_pv
        )

        leistung_onshore = (
            anfangsLeistung_onshore
            + ( jahr - basisJahr) * steigungLeistung_onshore
        )

        leistung_offshore = (
            anfangsLeistung_offshore
            + ( jahr - basisJahr) * steigungLeistung_offshore
        )

        leistung_biomasse = (
            anfangsLeistung_biomasse
            + ( jahr - basisJahr) * steigungLeistung_biomasse
        )

        leistung_wasserkraft = (
            anfangsLeistung_wasserkraft
            + ( jahr - basisJahr) * steigungLeistung_wasserkraft
        )
        
            
        # Erzeugerprofil einlesen
        dfProfil = setUpErzeugerProfil()

        # Dataframe für Simulation erstellen
        dfSimulation = dfProfil.copy()

        # Photovoltaik Simulieren
        dfSimulation["PV [MWh]"] = (
            dfProfil["PV"]
            * leistung_pv
            * 2.5
        )

        # Wind Onshore Simulieren
        dfSimulation["Wind Onshore [MWh]"] = (
            dfProfil["Wind Onshore"]
            * leistung_onshore
            * 2.5   #1000 * 0.25 / 100 = 2.5
        )
        # Wind Offshore Simulieren
        dfSimulation["Wind Offshore [MWh]"] = (
            dfProfil["Wind Offshore"]
            * leistung_offshore
            * 2.5
        )

        # Biomasse Simulieren
        dfSimulation["Biomasse [MWh]"] = (
            dfProfil["Biomasse"]
            * leistung_biomasse
            * 2.5
        )

        # Wasserkraft Simulieren
        dfSimulation["Wasserkraft [MWh]"] = (
            dfProfil["Wasserkraft"]
            * leistung_wasserkraft
            * 2.5
        )

        # Verbrauch "Simulieren"
        dfSimulation["Verbrauch [MWh]"] = (
            dfProfil[f"Verbrauch {verbrauchsReferenzJahr}"] / 100
            * gesamtVerbrauchIn_TWh * 1000000
        )


        # Gesamte installierte Wind- und PV-Leistung [GW]
        installierteLeistungWindPV = (
            leistung_pv
            + leistung_onshore
            + leistung_offshore
        )

        # Wind und PV zusammenfassen
        dfSimulation["Wind + PV [MWh]"] = (
            dfSimulation["PV [MWh]"]
            + dfSimulation["Wind Onshore [MWh]"]
            + dfSimulation["Wind Offshore [MWh]"]
        ).astype(float)

        dfSimulation["Anteil PV"] = (
            dfSimulation["PV [MWh]"] / dfSimulation["Wind + PV [MWh]"]
        )

        dfSimulation["Anteil Wind Onshore"] = (
            dfSimulation["Wind Onshore [MWh]"] / dfSimulation["Wind + PV [MWh]"]
        )

        dfSimulation["Anteil Wind Offshore"] = (
            dfSimulation["Wind Offshore [MWh]"] / dfSimulation["Wind + PV [MWh]"]
        )


        # Dunkelflauten simulieren
        dfSimulation = simuliereDunkelflauten(
            dfSimulation,
            installierteLeistungWindPV,
            maxAenderung=1.0,
            seed=None
        )
        
        # EE Erzeugung berechnen
        dfSimulation["EE_Erzeugung [MWh]"] = (
            dfSimulation["Wind + PV [MWh]"]
            + dfSimulation["Biomasse [MWh]"]
            + dfSimulation["Wasserkraft [MWh]"]
        )


        # Bilanz berechnen
        dfSimulation["Bilanz [MWh]"] = (
            dfSimulation["EE_Erzeugung [MWh]"]
            - dfSimulation["Verbrauch [MWh]"]
        )

        # Überschuss berechnen
        dfSimulation["Ueberschuss [MWh]"] = (
            dfSimulation["Bilanz [MWh]"].clip(lower=0) # clip() bedeutet alle negativen werte mit 0 ersetzen
        )

        # Fehlmenge berechnen
        dfSimulation["Fehlmenge [MWh]"] = (
            (-dfSimulation["Bilanz [MWh]"]).clip(lower=0) # (-) beachten
        )

        dfSimulation["Direkt genutzt [MWh]"] = (
            dfSimulation[
                ["EE_Erzeugung [MWh]", "Verbrauch [MWh]"]
            ].min(axis=1)
        )

        dfSimulation["Erzeugung / Verbrauch [%]"] = (
            dfSimulation["EE_Erzeugung [MWh]"]
            / dfSimulation["Verbrauch [MWh]"]
            * 100
        )

        dfSimulation["Direkte Deckung [%]"] = (
            dfSimulation["Direkt genutzt [MWh]"]
            / dfSimulation["Verbrauch [MWh]"]
            * 100
        )

        dfSimulation["Restlast [GW]"] = (
            dfSimulation["Verbrauch [MWh]"]
            - dfSimulation["EE_Erzeugung [MWh]"]
        ) / 250

        anzahlDunkelflautenViertelstunden = (
            dfSimulation["Dunkelflaute"] == 0
        ).sum()

        anteilDunkelflauten = (
            anzahlDunkelflautenViertelstunden
            / len(dfSimulation)
            * 100
        )

        print("Viertelstunden mit Dunkelflaute:", anzahlDunkelflautenViertelstunden)
        print("Anteil Dunkelflauten [%]:", anteilDunkelflauten)

        anzahlDunkelflauten = (
            (dfSimulation["Dunkelflaute"] == 0)
            & (dfSimulation["Dunkelflaute"].shift(1) != 0)
        ).sum()

        print("Anzahl Dunkelflauten:", anzahlDunkelflauten)

        dfSimulationen[jahr] = dfSimulation

    return dfSimulationen

#eventuell später auslagern nach BerechnungsFunktionen!
def berechne_kennzahlen(dfSimulation):

    jahreserzeugung = (
        dfSimulation["EE_Erzeugung [MWh]"].sum()
    )

    jahresverbrauch = (
        dfSimulation["Verbrauch [MWh]"].sum()
    )

    direkt_genutzt = (
        dfSimulation["Direkt genutzt [MWh]"].sum()
    )

    jahresanteil = (
        jahreserzeugung / jahresverbrauch * 100
    )

    direkter_deckungsgrad = (
        direkt_genutzt / jahresverbrauch * 100
    )

    return {
        "Jahreserzeugung [TWh]": jahreserzeugung / 1_000_000,
        "Jahresverbrauch [TWh]": jahresverbrauch / 1_000_000,
        "Jahresanteil [%]": jahresanteil,
        "Direkter Deckungsgrad [%]": direkter_deckungsgrad
    }
