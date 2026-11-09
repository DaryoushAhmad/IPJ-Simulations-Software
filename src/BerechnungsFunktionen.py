import pandas as pd
import plotly.express as px
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv
import plotly.express as px



def haeufigkeitsverteilung_EE():

    dfGesamt = setUpGesamtcsv()

    ee_intervallgrenzen = list(range(0, 170, 10))

    dfGesamt["EE_Intervall"] = pd.cut(dfGesamt["EE_Anteil"], bins=ee_intervallgrenzen, include_lowest=True)

    EE_Intervall_Haeufigkeit = dfGesamt["EE_Intervall"].value_counts(sort=False)

    fig = px.bar(
        x=EE_Intervall_Haeufigkeit.index.astype(str),
        y=EE_Intervall_Haeufigkeit.values
    )

    # Diagramm mit einem Titel und Achsenbeschriftungen versehen
    fig.update_layout(
        title="Häufigkeitsverteilung der EE-Anteile (2020-2026)",
        xaxis_title="Anteil erneuerbarer Energien [%]",
        yaxis_title="Anzahl der Viertelstunden"
    )

    fig.show()
    
    
    
def erzeuge_ee_histogramm(df_eingabe):
    fig=px.histogram(
        data_frame=df_eingabe,
        x="EE_Anteil",
        nbins=32,
        title="Häufigkeitsverteilung des erneuerbaren Anteils",
        #labels={"EE_Anteil": "Erneuerbarer Anteil[%]"}
        color_discrete_sequence=["#2ecc71"]
    )
    
    #5% lücke zwischen balken
    fig.update_layout(bargap=0.05, title_font_size=18, hovermode="x unified",
                      xaxis_title="Erneuerbarer Anteil [%]",
                      yaxis_title="Anzahl Viertelstunden")
    
    #rote linie bei 100% deckung
    fig.add_vline(x=100,
                  line_dash="dash",
                  line_color="red",
                  line_width=2,
                  annotation_text="100% Deckung",
                  annotation_position="top right"
                  )
    
    #gelbe linie bei 80% deckung
    fig.add_vline(x=80,
                      line_dash="dash",
                      line_color="yellow",
                      line_width=2,
                      annotation_text="80% Deckung",
                      annotation_position="top right"
                      )
    
    return fig



#---------- Funktion zum erstellen eines Kreisdiagtramms ----------
def erzeuge_kreisdiagram_spalten(df_eingabe):
    #erzeugungsspalten auswählen
    spalten_erzeugung=["Biomasse [MWh] Originalauflösungen","Wasserkraft [MWh] Originalauflösungen","Wind Offshore [MWh] Originalauflösungen","Wind Onshore [MWh] Originalauflösungen","Photovoltaik [MWh] Originalauflösungen","Sonstige Erneuerbare [MWh] Originalauflösungen","Kernenergie [MWh] Originalauflösungen","Braunkohle [MWh] Originalauflösungen","Steinkohle [MWh] Originalauflösungen","Erdgas [MWh] Originalauflösungen","Pumpspeicher [MWh] Originalauflösungen_x","Sonstige Konventionelle [MWh] Originalauflösungen",]
    
    #summen über zeitraum berechnen
    df_mix=df_eingabe[spalten_erzeugung].sum().reset_index()
    df_mix.columns=["Energieträger", "Erzeugung MWh"]
    
    #beschriftungen bereinigen?
    df_mix["Energieträger"]=df_mix["Energieträger"].str.replace(" [MWh] Originalauflösungen", "", regex=False)
    
    
    #kreisdiagramm erstellen
    fig=px.pie(
        df_mix,
        names="Energieträger",
        values="Erzeugung MWh",
        title="Gesamter Erzeugungsmix seit 2020",
        hole=0.4, #kreisoptik 0.4
    )
    
    
    #anzeige details
    fig.update_traces(textinfo="percent+label", textposition="outside")
    fig.update_layout(title_font_size=18, showlegend=True,
                      height=900,)
    
    
    return fig
    
    
#---------- Funktion zum erstellen eines gestapelten Flächendiagramms ----------
def erzeuge_zeitreihen_chart(df_eingabe):
    spalten_erzeugung=["Biomasse [MWh] Originalauflösungen","Wasserkraft [MWh] Originalauflösungen","Wind Offshore [MWh] Originalauflösungen","Wind Onshore [MWh] Originalauflösungen","Photovoltaik [MWh] Originalauflösungen","Sonstige Erneuerbare [MWh] Originalauflösungen","Kernenergie [MWh] Originalauflösungen","Braunkohle [MWh] Originalauflösungen","Steinkohle [MWh] Originalauflösungen","Erdgas [MWh] Originalauflösungen","Pumpspeicher [MWh] Originalauflösungen_x","Sonstige Konventionelle [MWh] Originalauflösungen",]
    #spalten_erzeugung=spalten_erzeugung.str.replace(" [MWh] Originalauflösungen", "", regex=False) funktioniert nicht
    
    fig=px.area(
        data_frame=df_eingabe,
        x="Datum von",
        y=spalten_erzeugung,
        title="Stromerzeugung nach Energieträgern im Zeitverlauf",
    )
    
    #beschriftungen bereinigen, damit nicht "Orginalaufösungen steht"
    fig.for_each_trace(
        lambda trace: trace.update(
            name=trace.name.replace(" [MWh] Originalauflösungen", "")
        )
    )
    
    fig.update_layout(
        hovermode="x unified",
        height=650,
        xaxis_title="Datum/ Uhrzeit",
        yaxis_title="Erzeugung [MWh]",
    )
    
    
    return fig