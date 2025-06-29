# ==============================================================================
# PowerShell Installer for Logg Generator
# ==============================================================================

# ====== KONFIGURASJON ======
$AppName       = "Logg Generator"
$Publisher     = "Aleksander B. Reitan"
$InstallFolder = "$env:USERPROFILE\Documents\$AppName"
$ShortcutPath  = "$env:USERPROFILE\Desktop\$AppName.lnk"
$UninstallReg  = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"
# ===========================

# ⚠️ Sjekk om scriptet kjøres som administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "❌ Dette skriptet må kjøres som administrator." -ForegroundColor Red
    Read-Host "Trykk Enter for å avslutte."
    exit
}

# 🔎 Hent siste release fra GitHub
Write-Host "🔍 Henter siste versjon fra GitHub..." -ForegroundColor Cyan
try {
    $apiUrl = "https://api.github.com/repos/Aleksander-B-Reitan/Logg-Generator/releases/latest"
    $response = Invoke-RestMethod -Uri $apiUrl -Headers @{"User-Agent"="PowerShell-Installer"}
    $DownloadUrl = ($response.assets | Where-Object { $_.name -like "*.exe" }).browser_download_url
    $AppVersion = $response.tag_name.TrimStart("v")
    $ExeName = ($DownloadUrl -split "/")[-1]
    $ExePath = Join-Path $InstallFolder $ExeName
} catch {
    Write-Host "❌ Kunne ikke hente siste versjon. Sjekk internettforbindelsen eller GitHub API-status." -ForegroundColor Red
    Read-Host "Trykk Enter for å avslutte."
    exit
}

# ✨ [ENHANCEMENT] Sjekk om applikasjonen allerede kjører
$ProcessName = $ExeName -replace '\.exe$'
if (Get-Process -Name $ProcessName -ErrorAction SilentlyContinue) {
    Write-Host "⚠️ $AppName kjører allerede. Lukk programmet og kjør skriptet på nytt for å oppdatere." -ForegroundColor Yellow
    Read-Host "Trykk Enter for å avslutte."
    exit
}

# 📥 Last ned nyeste .exe
Write-Host "📥 Laster ned versjon $AppVersion..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $InstallFolder -Force | Out-Null
try {
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $ExePath -UseBasicParsing
} catch {
    Write-Host "❌ Nedlastingen feilet." -ForegroundColor Red
    Read-Host "Trykk Enter for å avslutte."
    exit
}

if (-not (Test-Path $ExePath)) {
    Write-Host "❌ Nedlastingen feilet. Finner ikke filen." -ForegroundColor Red
    Read-Host "Trykk Enter for å avslutte."
    exit
}

Write-Host "✅ Lastet ned til: $ExePath" -ForegroundColor Green

# 🖇 Lag snarvei
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $ExePath
$Shortcut.WorkingDirectory = $InstallFolder
$Shortcut.Description = "Start $AppName"
$Shortcut.Save()

Write-Host "📌 Snarvei opprettet: $ShortcutPath" -ForegroundColor Green

# ✨ [ENHANCEMENT] Lag en selvstendig avinstalleringsskript
$UninstallScriptPath = Join-Path $InstallFolder "uninstall.ps1"
$UninstallScriptContent = @"
# Automatisk generert skript for å avinstallere $AppName
Write-Host "Avinstallerer $AppName..." -ForegroundColor Yellow

# Stopp prosessen hvis den kjører
`$proc = Get-Process -Name '$ProcessName' -ErrorAction SilentlyContinue
if (`$proc) {
    Stop-Process -Id `$proc.Id -Force
    Start-Sleep -Seconds 1
}

# Fjern installasjonsmappen
if (Test-Path -Path "$InstallFolder") {
    Remove-Item -Path "$InstallFolder" -Recurse -Force
    Write-Host "✅ Fjerne installasjonsmappe." -ForegroundColor Green
}

# Fjern snarvei på skrivebordet
if (Test-Path -Path "$ShortcutPath") {
    Remove-Item -Path "$ShortcutPath" -Force
    Write-Host "✅ Fjerne snarvei." -ForegroundColor Green
}

# Fjern registeroppføringen for Avinstallering
if (Test-Path -Path "$UninstallReg") {
    Remove-Item -Path "$UninstallReg" -Recurse -Force
    Write-Host "✅ Fjerne registeroppføring." -ForegroundColor Green
}

Write-Host "🎉 $AppName er nå avinstallert." -ForegroundColor Cyan
Read-Host "Trykk Enter for å lukke dette vinduet."
"@
# Skriv avinstalleringsskriptet til installasjonsmappen
$UninstallScriptContent | Out-File -FilePath $UninstallScriptPath -Encoding utf8 -Force


# 📝 Legg til som installert program
# ✨ [ENHANCEMENT] Beregn filstørrelsen dynamisk
$fileSizeBytes = (Get-Item $ExePath).Length
$fileSizeKB = [math]::Ceiling($fileSizeBytes / 1KB)

New-Item -Path $UninstallReg -Force | Out-Null
Set-ItemProperty -Path $UninstallReg -Name "DisplayName" -Value $AppName
Set-ItemProperty -Path $UninstallReg -Name "DisplayVersion" -Value $AppVersion
Set-ItemProperty -Path $UninstallReg -Name "Publisher" -Value $Publisher
Set-ItemProperty -Path $UninstallReg -Name "InstallLocation" -Value $InstallFolder
Set-ItemProperty -Path $UninstallReg -Name "DisplayIcon" -Value $ExePath
# ✨ [ENHANCEMENT] Bruk det nye avinstalleringsskriptet og den beregnede størrelsen
Set-ItemProperty -Path $UninstallReg -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"$UninstallScriptPath`""
Set-ItemProperty -Path $UninstallReg -Name "EstimatedSize" -Value $fileSizeKB -Type DWord


Write-Host "🧾 Registrert som installert program i Windows" -ForegroundColor Yellow
Write-Host "🎉 Installasjonen av versjon $AppVersion er fullført!" -ForegroundColor Cyan
