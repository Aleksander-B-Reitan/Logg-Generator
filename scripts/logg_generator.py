import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Frame, Label, Entry, Text, Button, LabelFrame, Checkbutton, BooleanVar
from tkinter import filedialog
import datetime
from docxtpl import DocxTemplate
import os
import urllib.request
import urllib.error
import json # <--- NY IMPORT for lagring/lasting

def check_and_download_template():
    template_filename = "CCNA Logg Mal v1.0.docx"
    template_url = "https://github.com/Aleksander-B-Reitan/Logg-Generator/raw/refs/heads/main/Maler/CCNA%20Logg%20Mal%20v1.0.docx"
    if not os.path.exists(template_filename):
        messagebox.showinfo("Mangler Mal", f"Mal-filen '{template_filename}' ble ikke funnet.\n\nProgrammet vil nå forsøke å laste den ned.")
        try:
            urllib.request.urlretrieve(template_url, template_filename)
            messagebox.showinfo("Suksess", f"Malen '{template_filename}' ble lastet ned. Programmet kan nå fortsette.")
            return True
        except Exception as e:
            messagebox.showerror("Feil ved nedlasting", f"Kunne ikke laste ned malen fra nettet.\n\nSjekk internettforbindelsen din, eller last ned filen manuelt fra:\n{template_url}\n\nFeilmelding: {e}")
            return False
    return True

def fullstendig_logg_generator():
    SETTINGS_FILE = 'logg_settings.json'

    competency_goals = {
        # ... (all competency goals remain here, cut for brevity) ...
        "1- Planlegge, innføre og dokumentere IT-systemer slik at de er stabile, sikre og effektive gjennom hele livssyklusen": ["Planlegge implementering av ny server", "Utarbeide en retningslinje for passordpolitikk", "Gjennomføre en sårbarhetsvurdering", "Lage en beredskapsplan", "Oppdatere programvare", "Overvåke ytelse", "Sikkerhetskopieringsstrategi", "Dokumentere systemarkitektur", "Etablere rutiner for brukeradministrasjon", "Sikkerhetsopplæring", "Generell - Planlegge, innføre og dokumentere IT-systemer slik at de er stabile, sikre og effektive gjennom hele livssyklusen", "Serverlab Oppgave 02 b) - Hypervisor - Beregne lisenskostnad", "Serverlab Oppgave 03 e) - IP-adresser - fast IP", "Serverlab Oppgave 09 g) - Nettverk & DHCP - IP-adressekonflikt", "Serverlab Oppgave 09 h) - Nettverk & DHCP - 169.254.x.x", "Serverlab Oppgave 12 g) - Windows Klienter - Lisens", "Serverlab Oppgave 13 f) - DNS del 2 - Hva er DNS?", "Serverlab Oppgave 14 b) - Filserver med rettigheter fra AD - Rollekonflikter", "Serverlab Oppgave 14 L) - Filserver med rettigheter fra AD - Sikkerhetsgrupper", "Serverlab Oppgave 15 L) - Group Policy - Hva er det?", "Serverlab Oppgave 16 i) - Backup - Ivareta ACL", "Serverlab Oppgave 16 j) - Backup - Papirkurv", "Serverlab Oppgave 16 k) - Backup - Farer", "Serverlab Oppgave 18 - Systemdokumentasjon", "Serverlab Oppgave 19 b) - Lifehack for sysadmin", "Serverlab Oppgave 20 - Instruktør kontrollerer LAB"],
        "2- Bruke og gjøre rede for rutiner og systemer for avviksrapportering og vurdere tiltak for håndtering av avvik": ["Avviksrapporteringssystem", "Avviksrapportøvelse", "Avviksanalyse", "Tiltaksevaluering", "Rutiner for avvikshåndtering", "Foreslå forbedringer", "Samarbeid med andre avdelinger", "Opplæring og bevissthet", "Evaluering av konsekvenser", "Periodisk revisjon", "Generell - Bruke og gjøre rede for rutiner og systemer for avviksrapportering og vurdere tiltak for håndtering av avvik"],
        "3- Reflektere over og anvende virksomhetens retningslinjer for datasikkerhet og personvern i virksomheten": ["Gjennomgang av virksomhetens retningslinjer", "Opplæringsprogram", "Rapportering av brudd", "Nanolearning - Ikke bli offer for svindel", "Nanolearning - Tilgang og passord", "Nanolearning - Repetisjon"],
        "4- Vurdere og gjøre rede for konsekvensene ved sikkerhetsbrudd for virksomheten, samfunnet og individet og foreslå tiltak": ["Sikkerhetsbruddsanalyse", "Sikkerhetsbrudds simulering", "Konsekvensvurdering for samfunnet", "Individuelle konsekvenser", "Varsling og kommunikasjon", "Gjenopprettingstiltak", "Kommunikasjon med tilsynsmyndigheter", "Økonomisk konsekvensanalyse", "Opplærings- og bevissthetsprogram", "Beredskapsøvelse", "Generell - Vurdere og gjøre rede for konsekvensene ved sikkerhetsbrudd for virksomheten, samfunnet og individet og foreslå tiltak"],
        "5- Bruke verktøy for å automatisere og effektivisere driftsoppgaver": ["Get started with Windows PowerShell", "Automate administrative tasks by using PowerShell", "Automatisering av oppdateringsprosesser", "Sikkerhetsautomatisering", "Konfigurasjonsadministrasjon", "Overvåkingsautomatisering", "Sikkerhetskopieringsautomatisering", "Patchhåndtering", "Bearbeiding av skyressurser", "Kontinuerlig integrering og kontinuerlig distribusjon (CI/CD)", "Automatisert ytelsestesting", "Selfservice portal", "Generell - Bruke verktøy for å automatisere og effektivisere driftsoppgaver"],
        "6- Utarbeide bestillinger og anbud knyttet til innkjøp av løsninger, systemer og tjenester og vurdere tekniske, økonomiske og bærekraftige forhold ved tilbudene": ["Anbudsprosess for programvarelisensiering", "Innkjøp av maskinvare", "Outsourcing av IT-tjenester", "Vurdering av leverandører", "Kostnadsanalyse", "Energiforbruk og bærekraft", "Teknisk vurdering", "Kontraktsforhandlinger", "Evaluering av tilbud", "Innkjøpspolitikk og retningslinjer", "Generell - Utarbeide bestillinger og anbud knyttet til innkjøp av løsninger, systemer og tjenester og vurdere tekniske, økonomiske og bærekraftige forhold ved tilbudene"],
        "7- Gjøre rede for og følge virksomhetens rutiner knyttet til anskaffelser, implementering, oppsett, drift og avhending av utstyr": ["Anskaffelsesprosess", "Implementering og oppsett", "Driftsprosedyrer", "Sikkerhetsaspekter", "Avhending og resirkulering", "Kvalitetssikring og dokumentasjon", "Evaluering og forbedring", "Regelverk og lover", "Generell - Gjøre rede for og følge virksomhetens rutiner knyttet til anskaffelser, implementering, oppsett, drift og avhending av utstyr"],
        "8- Dokumentere og reflektere over hvordan eget utført arbeid understøtter virksomhetens drift, tjenester og produkter": ["Dokumentasjon av arbeid", "Refleksjon over påvirkning", "Sammenligning med forventninger", "Samsvar med standarder og retningslinjer", "Kontinuerlig forbedring", "Samsvar med virksomhetens mål", "Kommunikasjon og rapportering", "Selvrefleksjon", "Generell - Dokumentere og reflektere over hvordan eget utført arbeid understøtter virksomhetens drift, tjenester og produkter", "Kompetanseprøve"],
        "9- Planlegge, gjennomføre og dokumentere brukerstøtte tilpasset oppdrag, målgruppe, kanal og teknologi": ["Brukerstøtte", "Generell - Planlegge, gjennomføre og dokumentere brukerstøtte tilpasset oppdrag, målgruppe, kanal og teknologi"],
        "10- Gjennomføre opplæring og veiledning i relevante IT-løsninger tilpasset oppdrag, målgruppe, kanal og teknologi": ["Planlegging av kommunikasjonsløsninger", "Gjennomføring av veiledning", "Dokumentasjon av veiledning", "Tilpasning til målgruppe", "Generell - Gjennomføre opplæring og veiledning i relevante IT-løsninger tilpasset oppdrag, målgruppe, kanal og teknologi"],
        "11- Lese, forstå og utforme dokumentasjon og spesifikasjoner": ["Sammenligning av dokumentasjon", "Oversettelse av spesifikasjoner", "Forståelse av teknisk dokumentasjon", "Bruk av flerspråklige ressurser", "Generell - Lese, forstå og utforme dokumentasjon og spesifikasjoner"],
        "12- Gjøre rede for og reflektere over hvordan gjeldende lover og regler i arbeidslivet og etiske retningslinjer påvirker eget arbeid": ["Etisk bevissthet for IT-personell", "Etiske retningslinjer i FRID-iks", "Etiske dilemmaer i arbeidslivet", "Case-studie om personvern", "Generell - Gjøre rede for og reflektere over hvordan gjeldende lover og regler i arbeidslivet og etiske retningslinjer påvirker eget arbeid"],
        "13- Anvende gjeldende regelverk for personvern og informasjonssikkerhet i eget arbeid og reflektere over konsekvensene hvis regelverket ikke følges": ["Personvern", "Personvern og informasjonssikkerhet i FRID-iks", "Generell - Anvende gjeldende regelverk for personvern og informasjonssikkerhet i eget arbeid og reflektere over konsekvensene hvis regelverket ikke følges"],
        "14- Utforske og bruke metoder for feilsøking, utføre utbedringer og dokumentere løsninger": ["Feilsøking på nettverk og maskin", "Feilsøkingsmetodikk", "Feilsøking av nettverksproblemer", "Feilsøking av maskinvareproblemer", "Feilsøking av programvareproblemer", "Feilsøking av sikkerhetsproblemer", "Generell - Utforske og bruke metoder for feilsøking, utføre utbedringer og dokumentere løsninger"],
        "15- Gjøre rede for hvilke krav og forventninger som stilles til et likeverdig og inkluderende yrkesfellesskap, og reflektere over hvilke plikter og rettigheter arbeidsgiver og arbeidstaker har i lærebedriften": ["Arbeidsmiljø og HMS", "Case-studie om plikter og rettigheter", "Utvikling av retningslinjer for inkludering", "Generell - Gjøre rede for hvilke krav og forventninger som stilles til et likeverdig og inkluderende yrkesfellesskap, og reflektere over hvilke plikter og rettigheter arbeidsgiver og arbeidstaker har i lærebedriften"]
    }

    laeringspunkt_widgets = []

    # --- NYE HJELPEFUNKSJONER FOR LAGRING/LASTING ---
    def save_settings():
        settings = {
            'forfatter': forfatter_entry.get(),
            'modul_nr': modul_nr_entry.get(),
            'modul_navn': modul_navn_entry.get()
        }
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Kunne ikke lagre innstillinger: {e}")

    def load_settings():
        if not os.path.exists(SETTINGS_FILE):
            return # Gjør ingenting hvis filen ikke finnes
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Tøm eksisterende felt før innsetting
            forfatter_entry.delete(0, tk.END)
            modul_nr_entry.delete(0, tk.END)
            modul_navn_entry.delete(0, tk.END)

            # Sett inn lagrede verdier
            forfatter_entry.insert(0, settings.get('forfatter', ''))
            modul_nr_entry.insert(0, settings.get('modul_nr', ''))
            modul_navn_entry.insert(0, settings.get('modul_navn', ''))
        except Exception as e:
            print(f"Kunne ikke laste innstillinger: {e}")


    # --- GAMLE HJELPEFUNKSJONER (uendret) ---
    def add_laeringspunkt():
        punkt_frame = Frame(laeringspunkter_frame)
        punkt_frame.pack(fill='x', pady=2)
        entry = ttk.Entry(punkt_frame, width=75)
        entry.pack(side='left', fill='x', expand=True)
        remove_button = ttk.Button(punkt_frame, text="Fjern", command=lambda f=punkt_frame: remove_laeringspunkt(f))
        remove_button.pack(side='right', padx=5)
        laeringspunkt_widgets.append(punkt_frame)

    def remove_laeringspunkt(frame_to_remove):
        frame_to_remove.destroy()
        laeringspunkt_widgets.remove(frame_to_remove)

    def on_hovedmaal_selected(event):
        selected_hovedmaal = hovedmaal_combo.get()
        undermal_list = competency_goals.get(selected_hovedmaal, [])
        undermaal_combo['values'] = undermal_list
        undermaal_combo.set('')
        if undermal_list:
            undermaal_combo.config(state='readonly')
        else:
            undermaal_combo.config(state='disabled')

    def toggle_exam_fields():
        if include_exam.get():
            forrige_modul_entry.config(state='normal')
            resultat_entry.config(state='normal')
        else:
            forrige_modul_entry.config(state='disabled')
            resultat_entry.config(state='disabled')
            forrige_modul_entry.delete(0, tk.END)
            resultat_entry.delete(0, tk.END)

    def generer_logg():
        laeringspunkter = []
        for frame in laeringspunkt_widgets:
            entry = frame.winfo_children()[0]
            text = entry.get().strip()
            if text:
                laeringspunkter.append(text)
        
        template_filename = "CCNA Logg Mal v1.0.docx"
        try:
            doc = DocxTemplate(template_filename)
        except Exception as e:
            messagebox.showerror("Feil", f"Kunne ikke finne malen '{template_filename}'.\n{e}")
            return

        context = {
            'UkeNummer': uke_entry.get(), 'ModulNummer': modul_nr_entry.get(), 'ModulNavn': modul_navn_entry.get(), 'Forfatter': forfatter_entry.get(), 'ForrigeModulNummerOgNavn': forrige_modul_entry.get(), 'CheckpointExamResultat': resultat_entry.get(), 'HvaSomBleGjortMandag': mandag_text.get("1.0", tk.END).strip(), 'HvaSomBleGjortTirsdag': tirsdag_text.get("1.0", tk.END).strip(), 'HvaSomBleGjortOnsdag': onsdag_text.get("1.0", tk.END).strip(), 'HvaSomBleGjortTorsdag': torsdag_text.get("1.0", tk.END).strip(), 'HvaSomBleGjortFredag': fredag_text.get("1.0", tk.END).strip(), 'LæringsPunktFraUkasHendelser': laeringspunkter, 'hovedmaal': hovedmaal_combo.get(), 'undermaal': undermaal_combo.get(),
        }
        
        uke = uke_entry.get()
        if not uke:
            messagebox.showwarning("Mangler info", "Vennligst fyll ut ukenummer.")
            return

        doc.render(context)
        
        suggested_filename = f"CCNA_Logg_Uke_{uke}.docx"
        
        filnavn = filedialog.asksaveasfilename(
            initialfile=suggested_filename, title="Lagre loggfil som...", defaultextension=".docx", filetypes=(("Word-dokument", "*.docx"), ("Alle filer", "*.*"))
        )
        if not filnavn:
            return

        try:
            doc.save(filnavn)
            messagebox.showinfo("Suksess", f"Logg er generert og lagret som:\n{filnavn}")
            save_settings() # <--- KALLER LAGRE-FUNKSJONEN ETTER SUKSESS
            if messagebox.askyesno("Åpne Fil", "Vil du åpne den genererte filen nå?"):
                try:
                    os.startfile(filnavn)
                except Exception as e:
                    messagebox.showerror("Feil ved åpning", f"Kunne ikke åpne filen.\n{e}")
        except Exception as e:
            messagebox.showerror("Feil ved lagring", f"Kunne ikke lagre filen.\n{e}")

    # --- GUI-OPPSETT ---
    root = tk.Tk()
    root.title("CCNA Logg Generator")
    main_frame = Frame(root, padx=10, pady=10)
    main_frame.pack()

    # ... (resten av GUI-oppsettet er likt) ...
    info_frame = LabelFrame(main_frame, text="Generell Informasjon")
    info_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    Label(info_frame, text="Uke:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    uke_entry = Entry(info_frame, width=10)
    uke_entry.grid(row=0, column=1, sticky="w", padx=5)
    uke_entry.insert(0, str(datetime.date.today().isocalendar()[1]))
    Label(info_frame, text="Forfatter:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
    forfatter_entry = Entry(info_frame, width=40)
    forfatter_entry.grid(row=0, column=3, sticky="ew", padx=5)
    Label(info_frame, text="Modul Nr:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    modul_nr_entry = Entry(info_frame, width=10)
    modul_nr_entry.grid(row=1, column=1, sticky="w", padx=5)
    Label(info_frame, text="Modul Navn:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
    modul_navn_entry = Entry(info_frame, width=40)
    modul_navn_entry.grid(row=1, column=3, sticky="ew", padx=5)
    exam_frame = LabelFrame(main_frame, text="Checkpoint Exam")
    exam_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    include_exam = BooleanVar(value=True)
    exam_check = Checkbutton(exam_frame, text="Inkluder Checkpoint Exam denne uken?", variable=include_exam, command=toggle_exam_fields)
    exam_check.grid(row=0, column=0, columnspan=4, sticky="w", padx=5)
    Label(exam_frame, text="Forrige Modul:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    forrige_modul_entry = Entry(exam_frame)
    forrige_modul_entry.grid(row=1, column=1, sticky="ew", padx=5)
    Label(exam_frame, text="Resultat (%):").grid(row=1, column=2, sticky="w", padx=5, pady=2)
    resultat_entry = Entry(exam_frame, width=10)
    resultat_entry.grid(row=1, column=3, sticky="w", padx=5)
    dager_frame = LabelFrame(main_frame, text="Daglige Aktiviteter")
    dager_frame.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    fields = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag"]
    daily_entries = {}
    for i, day in enumerate(fields):
        Label(dager_frame, text=f"{day}:").grid(row=i, column=0, sticky="nw", padx=5, pady=2)
        daily_entries[day] = Text(dager_frame, height=2, width=80)
        daily_entries[day].grid(row=i, column=1, padx=5, pady=2)
    mandag_text = daily_entries["Mandag"]
    tirsdag_text = daily_entries["Tirsdag"]
    onsdag_text = daily_entries["Onsdag"]
    torsdag_text = daily_entries["Torsdag"]
    fredag_text = daily_entries["Fredag"]
    laering_frame = LabelFrame(main_frame, text="Læring og Kompetansemål")
    laering_frame.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
    Label(laering_frame, text="Hva lærte jeg:").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
    laeringspunkter_frame = Frame(laering_frame)
    laeringspunkter_frame.grid(row=0, column=1, sticky="ew", padx=5)
    add_button = ttk.Button(laering_frame, text="+ Legg til læringspunkt", command=add_laeringspunkt)
    add_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)
    Label(laering_frame, text="Hovedmål:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    hovedmaal_combo = ttk.Combobox(laering_frame, values=list(competency_goals.keys()), state='readonly', width=78)
    hovedmaal_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    hovedmaal_combo.bind('<<ComboboxSelected>>', on_hovedmaal_selected)
    Label(laering_frame, text="Undermål:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    undermaal_combo = ttk.Combobox(laering_frame, state='disabled', width=78)
    undermaal_combo.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
    generer_knapp = Button(main_frame, text="Generer Logg", command=generer_logg, font=('Helvetica', 10, 'bold'), bg="#4CAF50", fg="white")
    generer_knapp.grid(row=5, column=0, pady=10)

    # --- INITIALISERING ---
    toggle_exam_fields()
    add_laeringspunkt()
    load_settings() # <--- KALLER LASTE-FUNKSJONEN VED OPPSTART
    
    root.mainloop()

if __name__ == "__main__":
    if check_and_download_template():
        fullstendig_logg_generator()