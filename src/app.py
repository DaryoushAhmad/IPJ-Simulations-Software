# hauptdatei für die UI
#kai

# ausführen:       1.         app.py in integrierten Terminal öffnen
#                  2.         python -m streamlit run app.py



# anforderungen -übersichtlichtkeit für schnelle einblicke
#               -fachliche tiefe
#               -interaktive flüssige simulationen


#todo:pathlib? sodass pfasd immer gleich
#               app.py fertigstellen
#               was essen nicht vergessen

#imports
import streamlit as st
import pandas as pd
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv
from BerechnungsFunktionen import erzeuge_ee_histogramm, erzeugung_verbrauch_vergleich, produktionsmenge_vergleich, verhaeltnis_erzeugung_verbrauch
from BerechnungsFunktionen import erzeuge_kreisdiagram_spalten
from BerechnungsFunktionen import erzeuge_zeitreihen_chart
from BerechnungsFunktionen import simuliere_ee_erzeugung
from BerechnungsFunktionen import dunkelflauten_graph
from Simulation import simuliere_ee, berechne_kennzahlen


#grundeinstellungen festlegen
st.set_page_config("Simulationssoftware","⚡" , "wide") #funtkioniert das?

#titel
st.sidebar.title("Energiesystem-Simulator")

#daten laden und und zuweisen
dfGesamt=setUpGesamtcsv()
dfJahres=setUpJahresStatistikcsv()



#auswahlmenü
auswahl_nav=st.sidebar.radio("Navigation", ["Dashboard", "Zeitreihen-Analyse", "Szenario-Konfiguration", "Simulationsdiagramme", "erklärungen"])

#---------- dashboard ----------
if(auswahl_nav=="Dashboard"):
    #dashboard aufgerufen
    st.title("Dashboard")
    st.write("Willkommen zu deinem Dashboard")
    
    #werte berechnen min, max, mittelwert aus daten in prozent
    mittel_ee=dfGesamt["EE_Anteil"].mean()
    max_ee=dfGesamt["EE_Anteil"].max()
    min_ee=dfGesamt["EE_Anteil"].min()
    
    #layout in 3 spalten aufteilen
    col1, col2, col3 =st.columns(3)
    
    #kpi karten in spalten anzeigen
    col1.metric(label="durchschn. EE-Anteil", value=f"{mittel_ee:.1f}%")
    col2.metric(label="max EE-Anteil", value=f"{max_ee:.1f}%")
    col3.metric(label="min EE-Anteil", value=f"{min_ee:.1f}%")
    
    #diagramm häufigkeitsverteilung des ee anteils einbauen
    fig_histogramm=erzeuge_ee_histogramm(dfGesamt)
    st.plotly_chart(fig_histogramm, width='stretch')
    
    #kreisdiagramm einbauen
    fig_kreisdiagramm=erzeuge_kreisdiagram_spalten(dfGesamt)
    st.plotly_chart(fig_kreisdiagramm, width='stretch')
    
    
    
    
    

    
#---------- tab2 ----------
elif(auswahl_nav=="Zeitreihen-Analyse"):
    
    
    #min und max werte für aus spalte bestimmen und in Datumsobjekte umwandeln
    min_datum=dfGesamt["Datum von"].dt.date.min()
    max_datum=dfGesamt["Datum von"].dt.date.max()

    gewaelter_zeitraum=st.sidebar.date_input(
        "Zeitraum wählen",
        value=(max_datum - pd.Timedelta(days=7), max_datum),
        min_value=min_datum,
        max_value=max_datum,
    )

    if len(gewaelter_zeitraum)==2:
        start_date, end_date=gewaelter_zeitraum
        df_gefiltert_datum=dfGesamt[(dfGesamt["Datum von"].dt.date >= start_date)
                            &(dfGesamt["Datum von"].dt.date <=end_date)
                            ]
    else:
        df_gefiltert_datum=dfGesamt

    fig_zeitreihe=erzeuge_zeitreihen_chart(df_gefiltert_datum)
    st.plotly_chart(fig_zeitreihe, width='stretch')











#---------- tab3 simulation ----------
elif(auswahl_nav=="Szenario-Konfiguration"):
    #st.title("3. coming soon...")
    
    #eingabe und infos des zu erstellenden szenario
    st.header("Szenario-Konfigurator")
    #st.subheader("Szenario erstellen(noch nicht lauffähig)")
    st.header("Szenario-Konfigurator")

    szenario_name=st.text_input(
        "Szenario-Name", placeholder="z.b. ausbauziel 2030"
    )
    
    szenario_beschreibung = st.text_area(
        "Szenario-Beschreibung", placeholder="kurze beschreibung des szenarios..."
        )

    

    # erneuerbare energien und verbrauch, verbindung zu simulation.py von dary
    st.subheader("Ausbau der erneuerbaren Energien & Verbrauch")


    #faktor_pv = 1
    #faktor_onshore = 1
    #faktor_offshore = 1
   
    with st.form("simulation_form"):
        col_links, col_rechts=st.columns(2)

        with col_links:
            faktor_pv=st.number_input(
                "Photovoltaik-Leistung",
                min_value=0.0,
                value=1.0,
                step=0.1
            )

            faktor_onshore=st.number_input(
                "Wind-Onshore-Leistung",
                min_value=0.0,
                value=1.0,
                step=0.1
            )

            faktor_offshore=st.number_input(
                "Wind-Offshore-Leistung",
                min_value=0.0,
                value=1.0,
                step=0.1
            )

        with col_rechts:
            faktor_biomasse=st.number_input(
                "Biomasse-Leistung",
                min_value=0.0,
                value=1.0,
                step=0.1
            )

            faktor_wasserkraft=st.number_input(
                "Wasserkraft-Leistung",
                min_value=0.0,
                value=1.0,
                step=0.1
            )

            verbrauchsReferenzJahr=st.selectbox(
                "Referenz Jahr Verbrauch",
                options=["2020","2021","2022","2023","2024","2025",],
                index=5,
            )
            gesamtVerbrauchIn_TWh=st.number_input(
                "Gesamtverbrauch in [TWh]",
                min_value=0.1,
                value=600.0,
                step=10.0
            )

        simulation_starten = st.form_submit_button(
                    "Simulation starten"
                )

    if simulation_starten:
            #wenn gedrückt, dann simuliere mit ausgewählten Faktoren
            ergebnis = simuliere_ee(
                leistung_pv=faktor_pv,
                leistung_onshore=faktor_onshore,
                leistung_offshore=faktor_offshore,
                leistung_biomasse=faktor_biomasse,
                leistung_wasserkraft=faktor_wasserkraft,
                verbrauchsReferenzJahr=verbrauchsReferenzJahr,
                gesamtVerbrauchIn_TWh=gesamtVerbrauchIn_TWh
            )

            st.subheader("Simulationsergebnisse")
            st.dataframe(ergebnis.head(1000)) #Daten Aus Simulation werden in einer Tabelle der größe 12 dargestellt
            #Zwischenspeichern der Simulation zum späteren Plotten der Ergebnisse
            st.session_state["df_simulation"]=ergebnis


#--------Tab 4 Diagramme--------
#Marios
#bearbeitet von kai, st.titel=... gibts nicht! Nutze lieber st.suberheader("text")

elif(auswahl_nav=="Simulationsdiagramme"):
    st.header("Simulationsergebnisse")
    if "df_simulation" in st.session_state:
        df_simulation = st.session_state["df_simulation"]
        #st.write(df_simulation.columns)
        #st.write(len(df_simulation))
        #========================================von dary===================================================

        st.subheader("Dunkelflauten und PV-/Wind-Erzeugung")
        st.caption(
            "Rot markierte Viertelstunden zeigen eine Dunkelflaute (Ja). "
            "PV + Wind enthält die Anpassung durch die Dunkelflautensimulation. "
            "Zum Vergrößern einen Zeitraum im Diagramm aufziehen; "
            "ein Doppelklick setzt den Zoom zurück."
        )
        st.plotly_chart(dunkelflauten_graph(df_simulation), width='stretch')
        #===========================================================================================

        #hier ausgabe der Erzeugungen Wind,PV, Wasser usw.z.Zt als Line. wird noch geändert
        fig=simuliere_ee_erzeugung(df_simulation)
        st.subheader("Simulation der Erzeugungen in MWh")
        st.plotly_chart(fig, width='stretch')

        #hier Ausgabe Erzeugung, Verbrauch und Bilanz. z.Zt als bar. später als Überlagerung
        fig=erzeugung_verbrauch_vergleich(df_simulation)
        st.subheader("Simulation und Vergleich von Erzeugung und Verbrauch")
        st.plotly_chart(fig,width='stretch')

        #hier Ausgabe von Überschuss und Fehlmenge und Restlast
        fig=produktionsmenge_vergleich(df_simulation)
        st.subheader("Übersicht Überschuss, Fehlmenge und Restlast")
        st.plotly_chart(fig,width='stretch')


        #Erzeugung/Verbrauch alleine als line
        fig=verhaeltnis_erzeugung_verbrauch(df_simulation)
        st.subheader("Übersicht Überschuss, Fehlmenge und Restlast")
        st.plotly_chart(fig,width='stretch')


    else:
        st.warning("Erst Simulation durchführen")
    

    










    
# #nachher löschen wenn schon gebaut--------------------------------------------
#     with st.form("simulation_form"):

#         faktor_pv = st.number_input(
#             "Photovoltaik-Faktor",
#             min_value=0.0,
#             value=1.0,
#             step=0.1
#         )

#         faktor_onshore = st.number_input(
#             "Wind-Onshore-Faktor",
#             min_value=0.0,
#             value=1.0,
#             step=0.1
#         )

#         faktor_offshore = st.number_input(
#             "Wind-Offshore-Faktor",
#             min_value=0.0,
#             value=1.0,
#             step=0.1
#         )

#         simulation_starten = st.form_submit_button(
#             "Simulation starten"
#         )

#     if simulation_starten:

#         ergebnis = simuliere_ee(
#             faktor_pv,
#             faktor_onshore,
#             faktor_offshore
#         )

#         st.subheader("Simulationsergebnisse")
#         st.dataframe(ergebnis.head(12))











    
    # #2 spalten erstellen für version und autor
    # col_links, col_rechts=st.columns(2)
    # with col_links:
    #     szenario_version=st.text_input(
    #         "Szenario-Version", value="(erforderlich)"
    #     )
    # with col_rechts:
    #     szenario_autor=st.text_input(
    #         "Szenario-Autor", value="(erforderlich)"
    #     )
    # st.divider()


# #abschnitt last(verbrauch) pro sektor ----------
#     st.subheader("Last(verbrauch)-pro Sektor")
#     st.write("Haushalte(Standardlastprofil)")
    
    
#     szenario_lastprofil_haushalt_basis=st.text_input(
#             "Lastprofil für Haushalt_Basis", value=""
#         )
    
    
    # #2 spalten erstellen für verbrauch hausalte 2030 und 2045
    # col_links, col_rechts=st.columns(2)
    # with col_links:
    #     szenario_eingabe_verbrauch_haushalt_2030=st.number_input(
    #         "Verbrauch Haushalte[TWh] 2030", value=120
    #     )
    # with col_rechts:
    #     szenario_eingabe_verbrauch_haushalt_2045=st.number_input(
    #         "Verbrauch Haushalte[TWh] 2045", value=120
    #     )
        
        
        
        
        
    # #---------- gewerbe ----------
    # st.write("Gewerbe")
    
    # szenario_lastprofil_gewerbe_basis=st.text_input(
    #             "Lastprofil für Gewerbe_Basis", value=""
    #         )
    
    
    # #2 spalten erstellen für verbrauch gewerbe 2030 und 2045
    # col_links, col_rechts=st.columns(2)
    # with col_links:
    #     szenario_eingabe_verbrauch_gewerbe_2030=st.number_input(
    #         "Verbrauch Gewerbe[TWh] 2030", value=140
    #     )
        
    # with col_rechts:
    #     szenario_eingabe_verbrauch_gewerbe_2045=st.number_input(
    #         "Verbrauch Gewerbe[TWh] 2045", value=130
    #     )



# #---------- landwirtschaft ----------
#     st.write("Landwirtschaft")
    
#     szenario_lastprofil_landwirtschaft_basis=st.text_input(
#                 "Lastprofil für Landwirtschaft_Basis", value=""
#             )
    
    
#     #2 spalten erstellen für verbrauch landwirtschaft 2030 und 2045
#     col_links, col_rechts=st.columns(2)
#     with col_links:
#         szenario_eingabe_verbrauch_landwirtschaft_2030=st.number_input(
#             "Verbrauch Landwirtschaft[TWh] 2030", value=300
#         )
        
#     with col_rechts:
#         szenario_eingabe_verbrauch_landwirtschaft_2045=st.number_input(
#             "Verbrauch Landwirtschaft[TWh] 2045", value=350
#         )



#---------- wärmepumpem ----------
    #st.divider()
    #st.subheader("neue Parameter")
    
    #2030
    #st.write("Jahr 2030")
    
    #2 spalten erstellen für verbrauch installierte wp(stück) + wärmebedarf
    #col_links, col_rechts=st.columns(2)
    #with col_links:
     #   szenario_eingabe_installierte_wp_2030=st.number_input(
      #      "Installierte WP(Stück)", value=3000000
       # )
           
    #with col_rechts:
     #   szenario_waermebedarf_wp_in_kwprojahr_2030=st.number_input(
      #      "Wärmebedarf/Wp[kWh/Jahr]", value=51000
       # )
        
        
    #2 spalten erstellen für cop und wetterdaten
    #col_links, col_rechts=st.columns(2)
    #with col_links:
    #    szenario_eingabe_cop_2030=st.number_input(
    #        "COP Ø 2030", value=3.40
    #    )
        
    #with col_rechts:
    #    szenario_eingabe_wetterdaten_2030=st.number_input(
     #       "Wetterdaten"
     #   )
        
        
        
        
        
        
        
#---------------------------für die simulation----------------------------------

        
  




#----------------------------------------















#---------- tab4 ----------

elif(auswahl_nav=="erklärungen"):
    
    st.title("4. coming soon...")
    
    st.write("Mein code funktioniert nicht: Ich weiß nicht warum")
    st.write("Mein code funktioniert: ich weiß absolut nicht warum")
    
    st.write("")
    st.write("Hardware: Das Teil am Computer, auf das man einschlagen kann, wenn die Software nicht funktioniert")
    st.write("Software: Das Teil, das man nicht sehen kann, aber dafür bezahlt")
    
    st.write("")
    st.write("Der Unterschied zwischen Windows und einem U-Boot? Wenn man ein Fenster öffnet, sterben beim U-Boot weniger Menschen")



#kpi karten










