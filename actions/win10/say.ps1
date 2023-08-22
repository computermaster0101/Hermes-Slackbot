# Extract the string after "say"
$argument = $args -replace '^say\s*', ''

# Capitalize the first letter of the extracted argument
$capitalizedArgument = $argument -replace '^(.)(.*)$', '$1'.ToUpper() + '$2'

# Check if the extracted argument is empty
if ($capitalizedArgument -ne '') {
    # Display the extracted argument in a message box
    powershell.exe -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('$capitalizedArgument','Hermes Said','OK','Information')"
} else {
    # Display an error message if no argument is provided after "say"
    powershell.exe -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('No message provided.','Hermes Said','OK','Error')"
}
