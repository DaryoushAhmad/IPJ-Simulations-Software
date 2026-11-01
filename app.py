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

#auswahlmenü
auswahl_nav=st.sidebar.radio("Navigation", ["Dashboard", "Zeitreihen-Analyse", "Szenarien-Simu"])

if(auswahl_nav=="Dashboard"):
    #dashboard aufgerufen
    st.title("dashboard ausführen")
    
elif(auswahl_nav=="Zeitreihen-Analyse"):
    #
    st.title("2. ausführen")

elif(auswahl_nav=="Szenarien-Simu"):
    #3
    st.title("3. ausführen")





# ladeanzeige während des ersten ausführens








st.write("Willkommen zu deinem Dashboard")

