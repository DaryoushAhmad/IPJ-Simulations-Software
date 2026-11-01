# hauptdatei für die UI

# ausführen:                python -m streamlit run app.py

# anforderungen -übersichtlichtkeit für schnelle einblicke
#               -fachliche tiefe
#               -interaktive flüssige simulationen


#imports
import streamlit as st
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv


#grundeinstellungen festlegen
st.set_page_config("Titel","icon" , "wide") #funtkioniert das?

#titel
st.sidebar.title("Energiesystem-Simulator")

#daten laden und und zuweisen
dfGesamt=setUpGesamtcsv()
dfJahres=setUpJahresStatistikcsv()



#auswahlmenü
auswahl_nav=st.sidebar.radio("Navigation", ["Dashboard", "Zeitreihen-Analyse", "Szenarien-Simu"])

if(auswahl_nav=="Dashboard"):
    #dashboard aufgerufen
    st.title("dashboard ausführen")
    
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
    
    
    
    
    
    
    
elif(auswahl_nav=="Zeitreihen-Analyse"):
    #
    st.title("2. ausführen")

elif(auswahl_nav=="Szenarien-Simu"):
    #3
    st.title("3. ausführen")





#kpi karten








st.write("Willkommen zu deinem Dashboard")

