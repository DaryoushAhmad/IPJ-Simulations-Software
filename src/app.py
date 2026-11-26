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
from Simulation import simuliere_ee, berechne_kennzahlen

from BerechnungsFunktionen import (
    erzeuge_ee_histogramm,
    erzeuge_kreisdiagram_spalten,
    erzeuge_zeitreihen_chart,
    simuliere_ee_erzeugung,
    erzeugung_verbrauch_vergleich,
    #produktionsmenge_vergleich,
    verhaeltnis_erzeugung_verbrauch,
    dunkelflauten_graph,
    vergleich_fehlmenge_ueberschuss,
    plot_verbrauch_referenz
)

#grundeinstellungen festlegen
st.set_page_config("Simulationssoftware","⚡" , "wide")

#titel
st.sidebar.title("Energiesystem-Simulator")

#daten laden und und zuweisen
dfGesamt=setUpGesamtcsv()
dfJahres=setUpJahresStatistikcsv()



#auswahlmenü
auswahl_nav=st.sidebar.radio("Navigation", ["Dashboard", "Zeitreihen-Analyse", "Szenario-Konfiguration", "Simulationsdiagramme", "Erklärungen"])

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
    

    szenario_name=st.text_input(
        "Szenario-Name", placeholder="z.b. Ausbauziel 2030"
    )
    
    szenario_beschreibung = st.text_area(
        "Szenario-Beschreibung", placeholder="kurze Beschreibung des Szenarios..."
        )
    
    with st.form("simulation_form"):
        
        #---------- box erzeugung ----------
        with st.container(border=True):
            st.subheader("Erzeugung")
            col_links, col_mitte=st.columns(2)
            
            with col_links:
                leistung_pv=st.number_input(
                    "Photovoltaik-Leistung [GW]",
                    min_value=0.0,
                    value=147.0,
                    step=10.0
                )

                leistung_onshore=st.number_input(
                    "Wind-Onshore-Leistung [GW]",
                    min_value=0.0,
                    value=80.0,
                    step=10.0
                )

                leistung_offshore=st.number_input(
                    "Wind-Offshore-Leistung [GW]",
                    min_value=0.0,
                    value=20.0,
                    step=10.0
                )

            with col_mitte:
                leistung_biomasse=st.number_input(
                    "Biomasse-Leistung [GW]",
                    min_value=0.0,
                    value=7.0,
                    step=1.0
                )

                #nachträglich einfügen wenn ich den wert habe
                leistung_wasserkraft=st.number_input(
                    "Wasserkraft-Leistung [GW]",
                    min_value=0.0,
                    value=1.0,
                    step=1.0
                )
                
                zielJahr=st.number_input(
                    "Zieljahr der Simulation",
                    min_value=2027,
                    max_value=2050,
                    value=2035,
                    step=1,                    
                )
            
        #---------- box verbrauch ----------
        with st.container(border=True):
            st.subheader("Verbrauch")
            col_links, col_mitte=st.columns(2)
        
            with col_links:
                verbrauchsReferenzJahr=st.selectbox(
                                "Referenz Jahr Verbrauch",
                                options=["2020","2021","2022","2023","2024","2025",],
                                index=5,
                            )
            
            with col_mitte:
                gesamtVerbrauchIn_TWh=st.number_input(
                                "Gesamtverbrauch in [TWh]",
                                min_value=0.1,
                                value=530.0,
                                step=10.0
                            )
                
                
 # ---------- box speicher ----------
        with st.container(border=True):
            st.subheader("coming soon: Speicher & Reserve")
            col_links, col_mitte = st.columns(2)

            with col_links:
                st.markdown("**Kurzzeitspeicher (Batterie / Pumpspeicher)**")
                speicher_kurz_kapazitaet_gwh = st.number_input(
                    "Kapazität Kurzzeitspeicher [GWh]",
                    min_value=0.0,
                    value=0.0,
                    step=0.0,
                )
                speicher_kurz_leistung_gw = st.number_input(
                    "Lade-/Entladeleistung [GW]",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )

            with col_mitte:
                st.markdown("**Langzeitspeicher (H₂) & Reservekraftwerke**")
                speicher_lang_kapazitaet_twh = st.number_input(
                    "Kapazität Langzeitspeicher [TWh]",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )
                speicher_lang_laden_gw = st.number_input(
                    "Elektrolyseur-Leistung (Laden) [GW]",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )
                speicher_lang_entladen_gw = st.number_input(
                    "Rückverstromung (Entladen) [GW]",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )
                reserve_leistung_gw = st.number_input(
                    "Reservekraftwerke [GW]",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                )

            #wirkungsgrade ausklappen
            with st.expander("Wirkungsgrade & CO2-Faktor (optional)"):
                col_links, col_mitte, col_rechts = st.columns(3)
                with col_links:
                    eta_kurz_ges = st.number_input(
                        "Wirkungsgrad Kurzzeit [%]",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.0,
                        step=1.0,
                    )
                with col_mitte:
                    eta_lang_laden = st.number_input(
                        "Wirkungsgrad H2-Laden [%]",
                        min_value=0.0,
                        max_value=0.0,
                        value=0.0,
                        step=1.0,
                    )
                    eta_lang_entladen = st.number_input(
                        "Wirkungsgrad H2-Entladen [%]",
                        min_value=0.0,
                        max_value=0.0,
                        value=0.0,
                        step=1.0,
                    )
                with col_rechts:
                    eta_reserve = st.number_input(
                        "Wirkungsgrad Reserve [%]",
                        min_value=0.0,
                        max_value=0.0,
                        value=0.0,
                        step=1.0,
                    )
                    co2_faktor_g_kwh = st.number_input(
                        "CO2-Faktor Reserve [g/kWh]",
                        min_value=0.0,
                        value=0.0,
                        step=1.0,
                    )    
                
                #-----------------------
                
                
                
                
            
            
        simulation_starten = st.form_submit_button(
                    "Simulation starten"
                )
#---------- simulation starten ----------
    if simulation_starten:
            #wenn gedrückt, dann simuliere mit eingegebenen Leistungen in GW
            with st.spinner(f"Simuliere Jahre 2027 bis {zielJahr}..."):
                ergebnis_dict = simuliere_ee(
                    leistung_pv=leistung_pv,
                    leistung_onshore=leistung_onshore,
                    leistung_offshore=leistung_offshore,
                    leistung_biomasse=leistung_biomasse,
                    leistung_wasserkraft=leistung_wasserkraft,
                    verbrauchsReferenzJahr=verbrauchsReferenzJahr,
                    gesamtVerbrauchIn_TWh=gesamtVerbrauchIn_TWh,
                    zielJahr=zielJahr
                )


            #st.session_state["df_simulationen"]=ergebnis_dict
            #st.session_state["szenario_name"]=szenario_name
            #st.session_state["szenario_beschreibung"]=szenario_beschreibung
            
            #anzeige vom buttonklick entkoppeln ?
            #später hinzufügen------
            st.session_state["verbrauchsReferenzJahr"] = verbrauchsReferenzJahr
            st.session_state["df_simulationen"] = ergebnis_dict
            st.success(f"Simulation bis {zielJahr} abgeschlossen!")
        
            # Nur das Zieljahr direkt anzeigen
            df_ziel = ergebnis_dict[zielJahr]
            st.dataframe(df_ziel.head(100), width="stretch")
  
            
        
       
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

        



#--------Tab 4 Diagramme--------
#Marios, Kai, Dary
#bearbeitet von kai, st.titel=... gibts nicht! Nutze lieber st.suberheader("text")

elif(auswahl_nav=="Simulationsdiagramme"):
    st.header("Simulationsergebnisse")
    if "df_simulationen" in st.session_state:
        df_simulationen = st.session_state["df_simulationen"]
        verfuegbare_jahre=sorted(df_simulationen.keys())
        #st.write(df_simulationen.columns)
        #st.write(len(df_simulationen))
        

        ausgewaehltes_jahr=st.selectbox(
            "Simuliertes Jahr für Diagramme wählen",
            options=verfuegbare_jahre,
            index=len(verfuegbare_jahre) - 1,
            key="jahr_diagramme",
        )
        df_simulationen=df_simulationen[ausgewaehltes_jahr]

        
        #========================================von dary===================================================

        st.subheader("Dunkelflauten und PV-/Wind-Erzeugung")
        st.caption(
            "Rot markierte Viertelstunden zeigen eine Dunkelflaute (Ja). "
            "PV + Wind enthält die Anpassung durch die Dunkelflautensimulation. "
            "Zum Vergrößern einen Zeitraum im Diagramm aufziehen; "
            "ein Doppelklick setzt den Zoom zurück."
        )
        st.plotly_chart(dunkelflauten_graph(df_simulationen), width='stretch')
        #===========================================================================================

        #hier ausgabe der Erzeugungen Wind,PV, Wasser usw.z.Zt als Line. wird noch geändert
        fig=simuliere_ee_erzeugung(df_simulationen)
        st.subheader("Simulation der Erzeugungen in MWh")
        st.plotly_chart(fig, width='stretch')

        #hier Ausgabe Erzeugung, Verbrauch und Bilanz. z.Zt als bar. später als Überlagerung
        # #sorry kai, aber ich muss hier mal reingrätschen
        fig1=erzeugung_verbrauch_vergleich(df_simulationen)
        fig2=vergleich_fehlmenge_ueberschuss(df_simulationen)
        st.subheader("Simulation und Vergleich von Erzeugung und Verbrauch")

        #Maximale und mittlere Restlast ausgeben
        max_restlast = df_simulationen["Restlast [GW]"].max()
        mittel_restlast = df_simulationen["Restlast [GW]"].mean()
        col1, col2 = st.columns(2)
        
        with col1:
                st.metric("Mittlere Restlast",f"{mittel_restlast:.1f} GW")
        
        with col2:
                st.metric("Maximale Restlast",f"{max_restlast:.1f} GW")

        #Ausgabe von zwei Plots auf einer höhe
        col1, col2=st.columns(2)
        with col1:
                st.plotly_chart(fig1,width='stretch')

        with col2: 
                st.plotly_chart(fig2,width='stretch')

        #hier Ausgabe von Überschuss und Fehlmenge und Restlast
        #fig=produktionsmenge_vergleich(df_simulationen)
        #st.subheader("Übersicht Überschuss, Fehlmenge und Restlast")
        #st.plotly_chart(fig,width='stretch')


        #Erzeugung/Verbrauch alleine als line
        fig=verhaeltnis_erzeugung_verbrauch(df_simulationen)
        st.subheader("Übersicht Erzeuger-Verbraucherverhältnis")
        st.plotly_chart(fig,width='stretch')

        #Erzeugung/Verbrauch alleine als line
        st.info(f"Verwendetes Verbrauchsprofil: {st.session_state['verbrauchsReferenzJahr']}")

        st.subheader("Vergleich Verbrauch Referenzjahr und Auswahljahr")
        fig=plot_verbrauch_referenz(df_simulationen)
        st.plotly_chart(fig,width='stretch')


    else:
        st.warning("Erst Simulation durchführen")
    

    










    










    
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















#---------- tab5 ----------

elif(auswahl_nav=="Erklärungen"):
    
    st.title("4. coming soon...")
    
    st.write("Mein code funktioniert nicht: Ich weiß nicht warum")
    st.write("Mein code funktioniert: ich weiß absolut nicht warum")
    
    st.write("")
    st.write("Hardware: Das Teil am Computer, auf das man einschlagen kann, wenn die Software nicht funktioniert")
    st.write("Software: Das Teil, das man nicht sehen kann, aber dafür bezahlt")
    
    st.write("")
    st.write("Der Unterschied zwischen Windows und einem U-Boot? Wenn man ein Fenster öffnet, sterben beim U-Boot weniger Menschen")



#kpi karten










