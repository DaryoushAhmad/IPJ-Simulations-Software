import pandas as pd
import plotly.express as px

dfGesamt = pd.read_csv(
    "data/bereinigt/SMARD_Gesamt_Bereinigt.csv",
    sep=";",    
    decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
    thousands=".",   #Pandas erklären das es ein 1000 Zeichen
    na_values=["-"]
)
dfGesamt["Datum von"] = pd.to_datetime(
dfGesamt["Datum von"],
format="%d.%m.%Y %H:%M"
)

dfGesamt["Datum bis"] = pd.to_datetime(
dfGesamt["Datum bis"],
format="%d.%m.%Y %H:%M"
)   


dfJahresStatistik = pd.read_csv(
    "data/bereinigt/SMARD_Jahresstatistik.csv",
    sep=";",    
    decimal=",",    #Pandas erklären das es ein Dezimalzeichen ist
    thousands=".",   #Pandas erklären das es ein 1000 Zeichen
    na_values=["-"]
)


'''
# Die Jahresstatistik enthält bereits die Summe des Verbrauchs je Jahr.
dfJahresStatistik = dfJahresStatistik.sort_values("Datum von")
dfJahresStatistik["Jahr"] = dfJahresStatistik["Datum von"].astype(str)
dfJahresStatistik["Verbrauch [TWh]"] = (
    dfJahresStatistik["Netzlast [MWh] Originalauflösungen"] / 1000000
)

# Unvollständige Jahre anhand der Anzahl der Viertelstunden kennzeichnen.
jahresbeginn = pd.to_datetime(dfJahresStatistik["Jahr"], format="%Y")
erwarteteViertelstunden = (365 + jahresbeginn.dt.is_leap_year.astype(int)) * 96
dfJahresStatistik["Datenstand"] = "Vollständiges Jahr"
dfJahresStatistik.loc[
    dfJahresStatistik["Anzahl_Viertelstunden"] < erwarteteViertelstunden,
    "Datenstand",
] = "Unvollständiges Jahr"

diagramm = px.bar(
    dfJahresStatistik,
    x="Jahr",
    y="Verbrauch [TWh]",
    color="Datenstand",
    text="Verbrauch [TWh]",
    title="Stromverbrauch je Jahr (Netzlast)",
    color_discrete_map={
        "Vollständiges Jahr": "#2563eb",
        "Unvollständiges Jahr": "#f59e0b",
    },
)
diagramm.update_traces(texttemplate="%{y:.1f}", textposition="outside")
diagramm.update_layout(
    xaxis_type="category",
    template="plotly_white",
    yaxis_rangemode="tozero",
)

# Das interaktive Diagramm im Browser öffnen.
diagramm.show(renderer="browser")
'''


# Nur 2020 und 2026 auswählen
dfGefiltert = dfGesamt.loc[
    dfGesamt["Datum von"].dt.year.isin([2020,2022,2025])
].copy()

# Neue Spalten für Jahr und Monat erstellen
dfGefiltert["Jahr"] = dfGefiltert["Datum von"].dt.year
dfGefiltert["Monat"] = dfGefiltert["Datum von"].dt.month

# Monatlichen Gesamtverbrauch berechnen
df20_26 = dfGefiltert.groupby(
    ["Jahr", "Monat"], as_index=False
)["Netzlast [MWh] Originalauflösungen"].sum()

#Diagramm plotten von chat
# Gemeinsamer Monatsvergleich

monatsnamen = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]

# Monatswerte beider Jahre vorbereiten, fehlende Monate bleiben leer.
monatsdaten_pro_jahr = []
for jahr in [2020,2022,2025]:
    dfMonate = (
        df20_26.loc[df20_26["Jahr"] == jahr]
        .set_index("Monat")
        .reindex(range(1, 13))
    )
    dfMonate["Verbrauch [TWh]"] = (
        dfMonate["Netzlast [MWh] Originalauflösungen"] / 1_000_000
    )
    dfMonate["Datenstand"] = "Vollständiger Monat"
    dfJahr = dfGefiltert.loc[dfGefiltert["Jahr"] == jahr]

    for monat in range(1, 13):
        monatsdaten = dfJahr.loc[dfJahr["Monat"] == monat]
        monatsbeginn = pd.Timestamp(year=jahr, month=monat, day=1)
        monatsende = monatsbeginn + pd.offsets.MonthBegin(1)
        if monatsdaten.empty:
            dfMonate.loc[monat, "Datenstand"] = "Keine Daten"
        elif (
            monatsdaten["Datum von"].min() > monatsbeginn
            or monatsdaten["Datum bis"].max() < monatsende
        ):
            dfMonate.loc[monat, "Datenstand"] = "Unvollständiger Monat"

    dfMonate["Monat"] = monatsnamen
    dfMonate["Jahr"] = str(jahr)
    monatsdaten_pro_jahr.append(dfMonate)

dfMonatsvergleich = pd.concat(monatsdaten_pro_jahr, ignore_index=True)
monatsdiagramm = px.bar(
    dfMonatsvergleich,
    x="Monat",
    y="Verbrauch [TWh]",
    color="Jahr",
    barmode="group",
    text="Verbrauch [TWh]",
    hover_data=["Datenstand"],
    title="Monatlicher Stromverbrauch: 2020 und 2026 (Netzlast)",
    category_orders={"Monat": monatsnamen, "Jahr": ["2020", "2026"]},
    color_discrete_map={"2020": "#2563eb", "2026": "#f59e0b"},
)
monatsdiagramm.update_traces(texttemplate="%{y:.2f}", textposition="outside")
# Teilmonate schraffieren; die Farbe bleibt dem jeweiligen Jahr zugeordnet.
for spur in monatsdiagramm.data:
    status = dfMonatsvergleich.loc[
        dfMonatsvergleich["Jahr"] == spur.name, "Datenstand"
    ]
    spur.marker.pattern.shape = [
        "/" if wert == "Unvollständiger Monat" else "" for wert in status
    ]

hinweise = ["Schraffiert = unvollständiger Monat"]
for jahr in ["2020", "2026"]:
    fehlende_monate = dfMonatsvergleich.loc[
        (dfMonatsvergleich["Jahr"] == jahr)
        & (dfMonatsvergleich["Datenstand"] == "Keine Daten"), "Monat"
    ].tolist()
    if fehlende_monate:
        hinweise.append(f"{jahr}: keine Daten für {', '.join(fehlende_monate)}")
monatsdiagramm.update_layout(
    template="plotly_white",
    xaxis=dict(tickmode="array", tickvals=monatsnamen),
    yaxis_rangemode="tozero",
    margin=dict(b=110),
)
monatsdiagramm.add_annotation(
    x=0, y=-0.22, xref="paper", yref="paper",
    text="<br>".join(hinweise), showarrow=False, xanchor="left",
)
monatsdiagramm.show(renderer="browser")



dfTagSommer = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2025-07-01").date(),["Datum von", "Netzlast [MWh] Originalauflösungen"]
].copy()

dfTagHerbst = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2025-10-01").date(),["Datum von", "Netzlast [MWh] Originalauflösungen"]
].copy()

dfTagWinter = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2026-01-01").date(),["Datum von", "Netzlast [MWh] Originalauflösungen"]
].copy()

dfTagFruehling = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2026-04-01").date(),["Datum von", "Netzlast [MWh] Originalauflösungen"]
].copy()


'''
#Diagram für die 4 Tage von chat

# Die Netzlast enthält die verbrauchte Energie je 15-Minuten-Intervall.
tagesdaten = [
    ("Frühling", dfTagFruehling),
    ("Sommer", dfTagSommer),
    ("Herbst", dfTagHerbst),
    ("Winter", dfTagWinter),
]
verbrauchsspalte = "Netzlast [MWh] Originalauflösungen"
# Eine gemeinsame Skala erleichtert den Vergleich der vier Tage.
max_verbrauch = max(dfTag[verbrauchsspalte].max() for _, dfTag in tagesdaten)

for jahreszeit, dfTag in tagesdaten:
    if dfTag.empty:
        print(f"Für {jahreszeit} sind keine Verbrauchsdaten vorhanden.")
        continue

    dfTag = dfTag.sort_values("Datum von")
    tagesbeginn = dfTag["Datum von"].iloc[0].normalize()
    datum = tagesbeginn.strftime("%d.%m.%Y")
    diagramm = px.line(
        dfTag,
        x="Datum von",
        y=verbrauchsspalte,
        markers=True,
        title=f"Stromverbrauch im Tagesverlauf – {jahreszeit}, {datum}",
        labels={
            "Datum von": "Uhrzeit",
            verbrauchsspalte: "Verbrauch je Viertelstunde [MWh]",
        },
    )
    diagramm.update_traces(
        line_color="#2563eb",
        marker_size=4,
        connectgaps=False,
        hovertemplate="%{x|%H:%M} Uhr<br>%{y:,.2f} MWh je Viertelstunde<extra></extra>",
    )
    diagramm.update_layout(
        template="plotly_white",
        xaxis=dict(
            tickformat="%H:%M",
            dtick=2 * 60 * 60 * 1000,
            range=[tagesbeginn, tagesbeginn + pd.Timedelta(days=1)],
        ),
        yaxis=dict(range=[0, max_verbrauch * 1.1]),
    )
    diagramm.show(renderer="browser")
'''



