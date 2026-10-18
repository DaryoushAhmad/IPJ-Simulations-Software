cd "C:\Users\Kai Damerius\Desktop\GitHub\IPJ-Simulations-Software"


#nacheinander ausführen, um zu prüfen, ob die dateien gleiche zeilenanzahl haben





$e = (Get-Content "data/raw/Realisierte_Erzeugung_202001010000_202610160000_Viertelstunde.csv" | Measure-Object -Line).Lines
$v = (Get-Content "data/raw/Realisierter_Stromverbrauch_202001010000_202610160000_Viertelstunde.csv" | Measure-Object -Line).Lines

"Erzeugung: $e"
"Verbrauch: $v"
"Gleiche Zeilenanzahl: $($e -eq $v)"