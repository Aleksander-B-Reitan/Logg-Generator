# Logg Generator v1.0

Dette er et Python-program med et grafisk grensesnitt (GUI) laget for å forenkle og standardisere utfyllingen av ukentlige logger, spesifikt for CCNA-studier, men kan tilpasses. Programmet genererer et ferdig utfylt Word-dokument (`.docx`) basert på input fra brukeren.

## Funksjoner

* **Grafisk Brukergrensesnitt (GUI):** Et enkelt og intuitivt vindu for all datainntasting.
* **Dynamisk Mal-håndtering:** Hvis mal-filen (`CCNA Logg Mal v1.0.docx`) ikke finnes, vil programmet automatisk forsøke å laste den ned fra GitHub.
* **Strukturert Datalagring:** Inneholder en komplett, hardkodet liste med 15 hovedmål og tilhørende undermål for enkel utfylling.
* **"Lagre som..." Dialog:** Lar brukeren selv velge filnavn og lagringssted for den genererte loggen.
* **Åpne Fil etter Lagring:** Spør brukeren om de vil åpne den nylig lagrede filen direkte i Word.
* **Lagring av Innstillinger:** Programmet husker automatisk "Forfatter", "Modul Nr" og "Modulnavn" mellom hver gang det kjøres, ved å lagre disse i en `logg_settings.json`-fil.
* **Valgfri Eksamensseksjon:** En avkrysningsboks lar brukeren velge om eksamensresultater skal inkluderes i loggen for den gitte uken.
* **Dynamiske Læringspunkter:** Brukeren kan legge til og fjerne input-felt for læringspunkter etter behov, noe som gir en ryddig og strukturert liste i det endelige dokumentet.
* **Cascading Dropdowns:** "Undermål"-menyen oppdateres automatisk basert på hvilket "Hovedmål" som er valgt, noe som gjør det raskt og enkelt å finne riktig kompetansemål.

## Bruk

Programmet kan kjøres på to måter:

#### 1. Via `.exe`-filen (Anbefalt)
-   Dobbeltklikk på `logg_generator.exe`.
-   Ingen installasjon av Python eller andre biblioteker er nødvendig.
-   Fyll ut feltene i programmet.
-   Trykk på "Generer Logg"-knappen.
-   Velg hvor du vil lagre filen i "Lagre som..."-vinduet.
-   Svar "Ja" eller "Nei" på om du vil åpne filen etterpå.

#### 2. Via Python-skriptet
-   Krever at Python 3 er installert.
-   Installer nødvendige biblioteker ved å kjøre `pip install docxtpl` i terminalen.
-   Kjør skriptet fra terminalen med `python logg_generator.py`.

## Filer i Prosjektet

-   `logg_generator.py`: Selve Python-kildekoden for programmet.
-   `logg_generator.exe`: Den kompilerte, frittstående Windows-applikasjonen (ligger i `dist`-mappen etter kompilering).
-   `CCNA Logg Mal v1.0.docx`: Word-malen som programmet bruker for å generere logger. Lastes ned automatisk hvis den mangler.
-   `logg_settings.json`: En fil som automatisk opprettes for å lagre innstillinger mellom økter.

## Forfatter

Aleksander B. Reitan
