# hauptdatei für die UI

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
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv
from BerechnungsFunktionen import erzeuge_ee_histogramm
from BerechnungsFunktionen import erzeuge_kreisdiagram_spalten

#grundeinstellungen festlegen
st.set_page_config("Titel","icon" , "wide") #funtkioniert das?

#titel
st.sidebar.title("Energiesystem-Simulator")

#daten laden und und zuweisen
dfGesamt=setUpGesamtcsv()
dfJahres=setUpJahresStatistikcsv()



#auswahlmenü
auswahl_nav=st.sidebar.radio("Navigation", ["Dashboard", "Zeitreihen-Analyse", "Szenarien-Simu"])

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
    #
    st.title("2. coming soon...")
    
    st.write("Mein code funktioniert nicht: Ich weiß nicht warum")
    st.write("Mein code funktioniert: ich weiß absolut nicht warum")
    
    st.write("")
    st.write("Hardware: Das Teil am Computer, auf das man einschlagen kann, wenn die Software nicht funktioniert")
    st.write("Software: Das Teil, das man nicht sehen kann, aber dafür bezahlt")
    
    st.write("")
    st.write("Der Unterschied zwischen Windows und einem U-Boot? Wenn man ein Fenster öffnet, sterben beim U-Boot weniger Menschen")

#---------- tab3 ----------
elif(auswahl_nav=="Szenarien-Simu"):
    #3
    st.title("3. coming soon...")





#kpi karten










