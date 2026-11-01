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


#Plotten der Jahressummen mit chat===================================================
'''
# Jahressummen der erneuerbaren Stromerzeugung von 2020 bis 2026.
dfEE = dfJahresStatistik.loc[
    dfJahresStatistik["Datum von"].between(2020, 2026)
].sort_values("Datum von").copy()
dfEE["Jahr"] = dfEE["Datum von"].astype(str)
dfEE["EE-Erzeugung [TWh]"] = dfEE["EE_Erzeugung[MWh]"] / 1_000_000

# Ein Teiljahr darf nicht wie eine vollständige Jahressumme erscheinen.
jahresbeginn = pd.to_datetime(dfEE["Jahr"], format="%Y")
erwarteteViertelstunden = (365 + jahresbeginn.dt.is_leap_year.astype(int)) * 96
dfEE["Datenstand"] = "Vollständiges Jahr"
dfEE.loc[
    dfEE["Anzahl_Viertelstunden"] < erwarteteViertelstunden,
    "Datenstand",
] = "Unvollständiges Jahr"

diagramm = px.bar(
    dfEE,
    x="Jahr",
    y="EE-Erzeugung [TWh]",
    color="Datenstand",
    text="EE-Erzeugung [TWh]",
    title="Erneuerbare Stromerzeugung pro Jahr: 2020–2026",
    category_orders={"Jahr": [str(jahr) for jahr in range(2020, 2027)]},
    color_discrete_map={
        "Vollständiges Jahr": "#16a34a",
        "Unvollständiges Jahr": "#f59e0b",
    },
)
diagramm.update_traces(texttemplate="%{y:.1f}", textposition="outside")
diagramm.update_layout(
    template="plotly_white",
    xaxis_type="category",
    yaxis_rangemode="tozero",
    margin=dict(b=100),
)

hinweise = []
for jahr in dfEE.loc[dfEE["Datenstand"] == "Unvollständiges Jahr", "Datum von"]:
    daten = dfGesamt.loc[dfGesamt["Datum von"].dt.year == jahr, "Datum von"]
    if not daten.empty:
        hinweise.append(
            f"{jahr}: unvollständiges Jahr, Daten bis {daten.max():%d.%m.%Y}"
        )
if hinweise:
    diagramm.add_annotation(
        x=0, y=-0.2, xref="paper", yref="paper",
        text="<br>".join(hinweise), showarrow=False, xanchor="left",
    )

diagramm.show(renderer="browser")
'''

#===============================================================================================

dfGefiltert = dfGesamt.loc[
    dfGesamt["Datum von"].dt.year.isin([2020, 2022, 2025])
].copy()

# Neue Spalten für Jahr und Monat erstellen
dfGefiltert["Jahr"] = dfGefiltert["Datum von"].dt.year
dfGefiltert["Monat"] = dfGefiltert["Datum von"].dt.month

df20_26 = dfGefiltert.groupby(
    ["Jahr", "Monat"], as_index=False
)["EE_Erzeugung"].sum()


'''
# Die bereits berechneten Monatssummen gemeinsam darstellen.
monatsnamen = [
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
]
dfMonatsvergleich = df20_26.sort_values(["Jahr", "Monat"]).copy()
dfMonatsvergleich["EE-Erzeugung [TWh]"] = (
    dfMonatsvergleich["EE_Erzeugung"] / 1_000_000
)
dfMonatsvergleich["Jahr"] = dfMonatsvergleich["Jahr"].astype(str)
dfMonatsvergleich["Monatsname"] = dfMonatsvergleich["Monat"].map(
    dict(enumerate(monatsnamen, start=1))
)
jahre = dfMonatsvergleich["Jahr"].unique().tolist()
monatsdiagramm = px.bar(
    dfMonatsvergleich,
    x="Monat",
    y="EE-Erzeugung [TWh]",
    color="Jahr",
    barmode="group",
    title=f"Monatliche erneuerbare Stromerzeugung: {', '.join(jahre)}",
    labels={"Monat": "Monat"},
    custom_data=["Monatsname", "Jahr"],
)
monatsdiagramm.update_traces(
    hovertemplate=(
        "%{customdata[0]} %{customdata[1]}"
        "<br>EE-Erzeugung: %{y:.2f} TWh<extra></extra>"
    ),
)
monatsdiagramm.update_layout(
    template="plotly_white",
    xaxis=dict(tickmode="array", tickvals=list(range(1, 13)), ticktext=monatsnamen),
    yaxis_rangemode="tozero",
    legend_title_text="Jahr",
)
monatsdiagramm.show(renderer="browser")
'''


#Jahreszeiten Tage

dfTagSommer = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2025-07-01").date(),["Datum von", "EE_Erzeugung"]
].copy()

dfTagHerbst = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2025-10-01").date(),["Datum von", "EE_Erzeugung"]
].copy()

dfTagWinter = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2026-01-01").date(),["Datum von", "EE_Erzeugung"]
].copy()

dfTagFruehling = dfGesamt.loc[
    dfGesamt["Datum von"].dt.date == pd.Timestamp("2026-04-01").date(),["Datum von", "EE_Erzeugung"]
].copy()

'''
# Pro Jahreszeit ein Liniendiagramm mit der Energie je Viertelstunde.
tagesdaten = [
    ("Frühling", dfTagFruehling),
    ("Sommer", dfTagSommer),
    ("Herbst", dfTagHerbst),
    ("Winter", dfTagWinter),
]
max_erzeugung = max(
    (dfTag["EE_Erzeugung"].max() for _, dfTag in tagesdaten if not dfTag.empty),
    default=0,
)

for jahreszeit, dfTag in tagesdaten:
    if dfTag.empty:
        print(f"Für {jahreszeit} sind keine Erzeugungsdaten vorhanden.")
        continue

    dfTag = dfTag.sort_values("Datum von")
    tagesbeginn = dfTag["Datum von"].iloc[0].normalize()
    diagramm = px.line(
        dfTag,
        x="Datum von",
        y="EE_Erzeugung",
        markers=True,
        title=(
            f"Erneuerbare Stromerzeugung im Tagesverlauf – "
            f"{jahreszeit}, {tagesbeginn:%d.%m.%Y}"
        ),
        labels={
            "Datum von": "Uhrzeit",
            "EE_Erzeugung": "EE-Erzeugung je Viertelstunde [MWh]",
        },
    )
    diagramm.update_traces(
        line_color="#16a34a",
        marker_size=4,
        connectgaps=False,
        hovertemplate=(
            "%{x|%H:%M} Uhr<br>EE-Erzeugung: "
            "%{y:,.2f} MWh je Viertelstunde<extra></extra>"
        ),
    )
    diagramm.update_layout(
        template="plotly_white",
        xaxis=dict(
            tickformat="%H:%M",
            dtick=2 * 60 * 60 * 1000,
            range=[tagesbeginn, tagesbeginn + pd.Timedelta(days=1)],
        ),
        # Gleiche Skala für den Vergleich der vier Jahreszeiten.
        yaxis=dict(range=[0, max_erzeugung * 1.1]),
    )
    diagramm.show(renderer="browser")
'''
#======================================================================

dfGesamt["Erzeugung Gesamt"] = dfGesamt["EE_Erzeugung"] + dfGesamt["Braunkohle [MWh] Originalauflösungen"] + dfGesamt["Steinkohle [MWh] Originalauflösungen"] + dfGesamt["Erdgas [MWh] Originalauflösungen"] + dfGesamt["Kernenergie [MWh] Originalauflösungen"] + dfGesamt["Pumpspeicher [MWh] Originalauflösungen_x"] + dfGesamt["Sonstige Konventionelle [MWh] Originalauflösungen"]


# Gesamtproduktion je Jahr berechnen; das Jahr ist der Index.
jahressummen = dfGesamt.groupby(
    dfGesamt["Datum von"].dt.year
)["Erzeugung Gesamt"].sum()

# Jahressummen anhand der Jahreszahl zuordnen.
dfJahresStatistik["Erzeugung Gesamt"] = (
    dfJahresStatistik["Datum von"].map(jahressummen)
)
print(jahressummen.head(10))
print(dfJahresStatistik.head(10))


# Ploten der Gesamt- und EE-Erzeugung Jahresüberblick

# Vergleich der vorhandenen Jahressummen: EE ist Teil der Gesamterzeugung.
dfErzeugungsvergleich = dfJahresStatistik.loc[
    dfJahresStatistik["Datum von"].between(2020, 2026)
].sort_values("Datum von").copy()
dfErzeugungsvergleich["Jahr"] = dfErzeugungsvergleich["Datum von"].astype(str)
dfErzeugungsvergleich["Gesamterzeugung"] = (
    dfErzeugungsvergleich["Erzeugung Gesamt"] / 1_000_000
)
dfErzeugungsvergleich["EE-Erzeugung"] = (
    dfErzeugungsvergleich["EE_Erzeugung[MWh]"] / 1_000_000
)
jahresbeginn = pd.to_datetime(dfErzeugungsvergleich["Jahr"], format="%Y")
erwarteteViertelstunden = (365 + jahresbeginn.dt.is_leap_year.astype(int)) * 96
dfErzeugungsvergleich["Datenstand"] = "Vollständiges Jahr"
dfErzeugungsvergleich.loc[
    dfErzeugungsvergleich["Anzahl_Viertelstunden"] < erwarteteViertelstunden,
    "Datenstand",
] = "Unvollständiges Jahr"

dfVergleichLang = dfErzeugungsvergleich.melt(
    id_vars=["Jahr", "Datenstand"],
    value_vars=["Gesamterzeugung", "EE-Erzeugung"],
    var_name="Erzeugungsart",
    value_name="Erzeugung [TWh]",
)
vergleichsdiagramm = px.bar(
    dfVergleichLang,
    x="Jahr",
    y="Erzeugung [TWh]",
    color="Erzeugungsart",
    barmode="group",
    text="Erzeugung [TWh]",
    hover_data=["Datenstand"],
    title="Gesamterzeugung und erneuerbare Stromerzeugung: 2020–2026",
    color_discrete_map={"Gesamterzeugung": "#2563eb", "EE-Erzeugung": "#16a34a"},
)
for spur in vergleichsdiagramm.data:
    spur.marker.pattern.shape = [
        "/" if status == "Unvollständiges Jahr" else ""
        for status in dfErzeugungsvergleich["Datenstand"]
    ]
vergleichsdiagramm.update_traces(texttemplate="%{y:.1f}", textposition="outside")
vergleichsdiagramm.update_layout(
    template="plotly_white",
    xaxis_type="category",
    yaxis_rangemode="tozero",
    legend_title_text="Erzeugungsart",
    margin=dict(b=110),
)
hinweise = ["Die Gesamterzeugung enthält die EE-Erzeugung."]
for jahr in dfErzeugungsvergleich.loc[
    dfErzeugungsvergleich["Datenstand"] == "Unvollständiges Jahr", "Datum von"
]:
    daten = dfGesamt.loc[dfGesamt["Datum von"].dt.year == jahr, "Datum von"]
    if not daten.empty:
        hinweise.append(
            f"{jahr}: unvollständig (schraffiert), Daten bis {daten.max():%d.%m.%Y}"
        )
vergleichsdiagramm.add_annotation(
    x=0, y=-0.2, xref="paper", yref="paper",
    text="<br>".join(hinweise), showarrow=False, xanchor="left",
)
vergleichsdiagramm.show(renderer="browser")
