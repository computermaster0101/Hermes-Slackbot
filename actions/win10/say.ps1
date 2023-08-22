# Extract the string after "say"
$argument = $args -replace '^say\s*', ''
$capitalizedString = "$($argument.Substring(0,1).ToUpper())$($argument.Substring(1))"
$capitalizedStringWithExclamation = $capitalizedString + "!"
powershell.exe -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('$capitalizedStringWithExclamation','Hermes Said','OK','Information')"