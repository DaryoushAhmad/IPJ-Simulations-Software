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
from BerechnungsFunktionen import erzeuge_ee_histogramm
from BerechnungsFunktionen import erzeuge_kreisdiagram_spalten
from BerechnungsFunktionen import erzeuge_zeitreihen_chart

#grundeinstellungen festlegen
st.set_page_config("Simulationssoftware","⚡" , "wide") #funtkioniert das?

#titel
st.sidebar.title("Energiesystem-Simulator")

#daten laden und und zuweisen
dfGesamt=setUpGesamtcsv()
dfJahres=setUpJahresStatistikcsv()



#auswahlmenü
auswahl_nav=st.sidebar.radio("Navigation", ["Dashboard", "Zeitreihen-Analyse", "Szenario-Konfiguration", "erklärungen"])

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
    st.plotly_chart(fig_histogramm, use_container_width=True)
    
    #kreisdiagramm einbauen
    fig_kreisdiagramm=erzeuge_kreisdiagram_spalten(dfGesamt)
    st.plotly_chart(fig_kreisdiagramm, use_container_width=True)
    
    
    
    
    

    
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
    st.plotly_chart(fig_zeitreihe, use_container_width=True)











#---------- tab3 ----------
elif(auswahl_nav=="Szenario-Konfiguration"):
    #st.title("3. coming soon...")
    
    #eingabe von infos des zu erstellenden szenario
    st.header("Szenario-Konfigurator")
    st.subheader("Szenario erstellen(noch nicht lauffähig)")
    
    szenario_name=st.text_input(
        "Szenario-Name", value="(erforderlich)"
    )
    
    szenario_beschreibung=st.text_area(
        "Szenario-Beschreibung", value="(erforderlich)"
    )
    
    #2 spalten erstellen für version und autor
    col_links, col_rechts=st.columns(2)
    with col_links:
        szenario_version=st.text_input(
            "Szenario-Version", value="(erforderlich)"
        )
    with col_rechts:
        szenario_autor=st.text_input(
            "Szenario-Autor", value="(erforderlich)"
        )
    st.divider()


#abschnitt last(verbrauch) pro sektor ----------
    st.subheader("Last(verbrauch)-pro Sektor")
    st.write("Haushalte(Standardlastprofil)")
    
    
    szenario_lastprofil_haushalt_basis=st.text_input(
            "Lastprofil für Haushalt_Basis", value=""
        )
    
    
    #2 spalten erstellen für verbrauch hausalte 2030 und 2045
    col_links, col_rechts=st.columns(2)
    with col_links:
        szenario_eingabe_verbrauch_haushalt_2030=st.number_input(
            "Verbrauch Haushalte[TWh] 2030", value=120
        )
    with col_rechts:
        szenario_eingabe_verbrauch_haushalt_2045=st.number_input(
            "Verbrauch Haushalte[TWh] 2045", value=120
        )
        
        
        
        
        
    #---------- gewerbe ----------
    st.write("Gewerbe")
    
    szenario_lastprofil_gewerbe_basis=st.text_input(
                "Lastprofil für Gewerbe_Basis", value=""
            )
    
    
    #2 spalten erstellen für verbrauch gewerbe 2030 und 2045
    col_links, col_rechts=st.columns(2)
    with col_links:
        szenario_eingabe_verbrauch_gewerbe_2030=st.number_input(
            "Verbrauch Gewerbe[TWh] 2030", value=140
        )
        
    with col_rechts:
        szenario_eingabe_verbrauch_gewerbe_2045=st.number_input(
            "Verbrauch Gewerbe[TWh] 2045", value=130
        )



#---------- landwirtschaft ----------
    st.write("Landwirtschaft")
    
    szenario_lastprofil_landwirtschaft_basis=st.text_input(
                "Lastprofil für Landwirtschaft_Basis", value=""
            )
    
    
    #2 spalten erstellen für verbrauch landwirtschaft 2030 und 2045
    col_links, col_rechts=st.columns(2)
    with col_links:
        szenario_eingabe_verbrauch_landwirtschaft_2030=st.number_input(
            "Verbrauch Landwirtschaft[TWh] 2030", value=300
        )
        
    with col_rechts:
        szenario_eingabe_verbrauch_landwirtschaft_2045=st.number_input(
            "Verbrauch Landwirtschaft[TWh] 2045", value=350
        )



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
        
        
        
        
        
        
        
#----------------------------------------------------------------------
        
        
  




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










