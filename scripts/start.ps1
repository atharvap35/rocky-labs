Write-Host "Starting the filesystem lab VM using Vagrant..."

$env:VAGRANT_PREFERRED_POWERSHELL = "powershell"
Push-Location d:\RHCSA\labs\filesystem
vagrant up
vagrant ssh -c 'echo "VM is up"'
Pop-Location
