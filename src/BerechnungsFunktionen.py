import pandas as pd
import plotly.express as px
#go ist zum Testen da
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from DataFunktionen import setUpGesamtcsv, setUpJahresStatistikcsv, setUpErzeugerProfil
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
    
    
    #kai
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
                      yaxis_title="Anzahl Viertelstunden",
                      height=700,
                      )
    
    
    #geändert
    #fig.update_layout(
    #    template="plotly_white", #geändert
    #    paper_bgcolor="white", #geändert
    #    plot_bgcolor="white", #geändert
    #    font=dict(color="black"),
    #    xaxis=dict(
    #        tickfont=dict(color="black", size=28),
    #        title_font=dict(color="black", size=28),
    #        gridcolor="#E5E7EB"
    #    ),
    #    yaxis=dict(
    #        tickfont=dict(color="black", size=28),
    #        title_font=dict(color="black", size=28),
    #        gridcolor="#E5E7EB"
    #    ),
        
        
    #    font_color="#111111", #geändert
       
    #)
    
    #rote linie bei 100% deckung
    fig.add_vline(x=100,
                  line_dash="dash",
                  line_color="red",
                  line_width=2,
                  annotation_text="100% Deckung",
                  annotation_position="top right",
                  annotation_font=dict(color="white", size=14), #geändert
                  )
    
    #gelbe linie bei 80% deckung
    fig.add_vline(x=80,
                      line_dash="dash",
                      line_color="yellow",
                      line_width=2,
                      annotation_text="80% Deckung",
                      annotation_position="top right",
                      annotation_font=dict(color="white", size=14), #geändert
                      )
    
    #5% balkenraster sauber ab 0 ausrichten, erste intervalle 0 bis 10 frei lassen
    fig.update_traces(xbins=dict(start=0.0, size=5.0))
    
    #range zwingt x achse, bei 0 bis 155 zu zeigen
    fig.update_xaxes(range=[0, 155], dtick=10)
    
    return fig



#---------- Funktion zum erstellen eines Kreisdiagtramms ----------
#kai
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
#kai
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

#Simulation (Marios)
#Zunächst in V1 line plots.  Ich habe vor da nachzubessern. Gerne Feedback!
#Es könnte auch sein, dass ich so eine zeitauflösungsstufe mache wie in Tab 2 von Kai. es sind sonst einfach echt Viele Werte auf einmal
def simuliere_ee_erzeugung(df):
    spalten_erzeugung_simulation={"PV [MWh]" :"gold",
           "Wind Onshore [MWh]" :"blue",
           "Wind Offshore [MWh]" :"lightblue",
           "Biomasse [MWh]" :"green",
           "Wasserkraft [MWh]" :"orange"}
    '''
    df_long=df.melt(
        id_vars=["Viertelstunde (Beginn)"],
        value_vars=spalten_erzeugung_simulation,
        var_name="Quelle",
        value_name="Erzeugung [MWh]"
    )
    
    fig=px.area(
        df_long,
        x="Viertelstunde (Beginn)",
        y="Erzeugung [MWh]",
        color='Quelle',
        title='Simulationsergebnisse Erzeugung durch erneuerbare Energieträger'
    )
    '''
    fig=go.Figure()

    for spalte,farbe in spalten_erzeugung_simulation.items():

        fig.add_trace(go.Scatter(
                x=df["Viertelstunde (Beginn)"],
                y=df[spalte],
                mode='lines',
                name=spalte,
                stackgroup='one',
                line=dict(color=farbe,width=0.5)
                ))

    fig.add_trace(
        go.Scatter(
            x=df["Viertelstunde (Beginn)"],
            y=df["EE_Erzeugung [MWh]"],
            mode='lines',
            name="Gesamterzeugung",
            line=dict(color="red", width=1)
        )
    )

    fig.update_layout(
        hovermode="x unified",
        height=600,
        #title="Simulation Erzeugungen EE",
        xaxis_title="Datum",
        yaxis_title="Erzeugung in [MWh]",
        legend_title="Quelle",
        legend=dict(                #Legende über dem Plot darstellen
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                    ),
                    margin=dict(t=120,
                                b=100)
            )

    return fig


def vergleich_fehlmenge_ueberschuss(df):
    #spalten_Fehlmenge_Ueberschuss=["Fehlmenge [MWh]","Ueberschuss [MWh]"]
    fig=go.Figure()

    fig.add_trace(go.Scatter(
                x=df["Viertelstunde (Beginn)"],
                y=df["Fehlmenge [MWh]"],
                mode='lines',
                name='Fehlmenge',
                line=dict(color='red',width=0.5)
                ))

    fig.add_trace(go.Scatter(
                x=df["Viertelstunde (Beginn)"],
                y=df["Ueberschuss [MWh]"],
                mode='lines',
                fill='tozeroy',
                name='Verbrauch',
                line=dict(color='green',width=0.5),
                opacity=0.7
            ))
    
    
    '''
    fig=px.area(
        df,
        x="Viertelstunde (Beginn)",
        y=spalten_Fehlmenge_Ueberschuss,
        title='Visualisierung Überschuss/Fehlmenge',
        color_discrete_sequence=['red','green']
    ) '''

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Datum",
        yaxis_title="Energie in [MWh]",
        legend_title='Beschreibung',
        legend=dict(                #Legende über dem Plot darstellen
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=120,
                    b=100)
    )

    return fig


#Vergleich zwischen Erzeugung, Verbrauch und Bilanz. kann man gestapelt darstellen oder so
def erzeugung_verbrauch_vergleich(df):
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Viertelstunde (Beginn)"],
        y=df["EE_Erzeugung [MWh]"],
        mode='lines',
        fill='tozeroy',
        name='EE-Erzeugung',
        line=dict(width=0.5),
        opacity=0.7
    ))

    fig.add_trace(go.Scatter(
            x=df["Viertelstunde (Beginn)"],
            y=df["Verbrauch [MWh]"],
            mode='lines',
            fill='tozeroy',
            name='Verbrauch',
            line=dict(width=0.5),
            opacity=0.7
        ))

    fig.add_trace(go.Scatter(
                x=df["Viertelstunde (Beginn)"],
                y=df["Bilanz [MWh]"],
                mode='lines',
                name='Bilanz',
                line=dict(color='red',width=0.5)
            ))

    fig.update_layout(
        hovermode="x unified",
        title="Vergleich Erzeugung und Verbrauch",
        xaxis_title="Datum",
        yaxis_title="Energie in MWh",
        legend_title='Kategorie',
        legend=dict(                #Legende über dem Plot darstellen
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5
                    ),
                    margin=dict(t=120,
                                b=100)

    )

    return fig

#Hier muss restlast noch in seine Eigene Y-Achse gepackt werden, da keine Energie sondern eine Leistung
#def produktionsmenge_vergleich(df):
    fig=px.line(
            df,
            x="Viertelstunde (Beginn)",
            y=["Ueberschuss [MWh]", "Fehlmenge [MWh]"],
            color_discrete_map={
                 "Ueberschuss [MWh]": "green"
            }
    )
    for trace in fig.data:
        trace.opacity=0.5

    fig.update_layout(
        hovermode="x unified",
        title="Aussortieren von Produktionsmengenvergleich",
        xaxis_title="Datum",
        yaxis_title="Energie in MWh"
    
        )
    
    return fig

def verhaeltnis_erzeugung_verbrauch(df):
    fig=px.line(
            df,
            x="Viertelstunde (Beginn)",
            y=["Erzeugung / Verbrauch [%]"],
        )
    fig.update_layout(
        hovermode="x unified",
        title="Verhältnis zwischen Erzeugung und Verbrauch",
        xaxis_title="Datum",
        yaxis_title="Anteil in Prozent",
        legend_title="Verhältnis",
        legend=dict(                #Legende über dem Plot darstellen
                    orientation='h',        
                    yanchor='bottom',        
                    y=1.02,
                    xanchor='center',
                    x=0.5
                    ),
                    margin=dict(t=120,b=100)     
    
        )
    return fig

def plot_verbrauch_referenz(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Viertelstunde (Beginn)"],
            y=df["Verbrauch [MWh]"],
            mode="lines",
            name="Verbrauch",
            line=dict(color="blue")
        )
    )
    fig.update_layout(
            hovermode="x unified",
            xaxis_title="Datum",
            yaxis_title="Energie in [MWh]"
            )

    return fig





def dunkelflauten_graph(df):
    """Zeigt simulierte PV-/Wind-Erzeugung und Dunkelflauten je Viertelstunde.

    In den Simulationsdaten bedeutet Dunkelflaute == 0 eine aktive Dunkelflaute.
    Die gemeinsame Erzeugung enthält bereits die Dunkelflauten-Anpassung.
    """
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.75, 0.25], vertical_spacing=0.08,
        subplot_titles=("PV + Wind", "Dunkelflaute je Viertelstunde"),
    )

    if df.empty:
        fig.add_annotation(text="Keine Simulationsdaten vorhanden", showarrow=False)
        return fig

    zeit = df["Viertelstunde (Beginn)"]
    if not pd.api.types.is_datetime64_any_dtype(zeit):
        # Das Jahresprofil enthält kein Jahr. 2000 erlaubt auch den 29. Februar;
        # angezeigt werden ausschließlich Tag, Monat und Uhrzeit.
        zeit = pd.to_datetime("2000 " + zeit, format="%Y %d.%m. %H:%M")

    # Eine Stufe gilt bis zum Ende der Viertelstunde, auch am Datenende.
    zeit = zeit.tolist() + [zeit.iloc[-1] + pd.Timedelta(minutes=15)]
    erzeugung = df["Wind + PV [MWh]"].tolist()
    aktiv = df["Dunkelflaute"].eq(0).astype(int).tolist()
    status_text = ["Ja" if wert else "Nein" for wert in aktiv]
    status_text.append(status_text[-1])

    fig.add_trace(go.Scatter(
        x=zeit, y=erzeugung + [erzeugung[-1]],
        mode="lines", name="PV + Wind (simuliert)",
        line=dict(color="#2980b9", width=1.5, shape="hv"),
        customdata=status_text,
        hovertemplate=("%{x|%d.%m. %H:%M}<br>PV + Wind: %{y:.2f} MWh"
                       "<br>Dunkelflaute: %{customdata}<extra></extra>"),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=zeit, y=aktiv + [aktiv[-1]],
        mode="lines", name="Dunkelflaute",
        line=dict(color="#c0392b", width=1, shape="hv"),
        fill="tozeroy", fillcolor="rgba(192, 57, 43, 0.3)",
        customdata=status_text,
        hovertemplate=("%{x|%d.%m. %H:%M}<br>Dunkelflaute: "
                       "%{customdata}<extra></extra>"),
    ), row=2, col=1)

    fig.update_yaxes(title_text="Erzeugung [MWh / Viertelstunde]", rangemode="tozero", row=1, col=1)
    fig.update_yaxes(tickvals=[0, 1], ticktext=["Nein", "Ja"], range=[-0.05, 1.1], row=2, col=1)
    fig.update_xaxes(tickformat="%d.%m.<br>%H:%M", hoverformat="%d.%m. %H:%M")
    fig.update_xaxes(title_text="Viertelstunde (Beginn)", row=2, col=1)
    fig.update_layout(
        title="Dunkelflauten und Erzeugung aus PV + Wind",
        hovermode="x unified", height=650,
        legend=dict(orientation="h", y=-0.2),
    )
    return fig




