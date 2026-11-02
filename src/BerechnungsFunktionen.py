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
    
    #10% lücke tzwischen balken
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
    
    