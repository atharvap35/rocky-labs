Write-Host "Checking prerequisites..."

function Check-Command($name, $friendlyName, $suggestUrl) {
    $path = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $path) {
        Write-Host "$friendlyName not found." -ForegroundColor Yellow
        if ($suggestUrl) { Write-Host "Download: $suggestUrl" }
        return $false
    } else {
        try {
            $ver = (& $name --version) -join ' '
        } catch {
            $ver = "(version unknown)"
        }
        Write-Host "${friendlyName}: OK $ver"
        return $true
    }
}

$allOk = $true
$allOk = (Check-Command git "Git" "https://git-scm.com/") -and $allOk
$allOk = (Check-Command vagrant "Vagrant" "https://www.vagrantup.com/") -and $allOk
$allOk = (Check-Command vboxmanage "VirtualBox (VBoxManage)" "https://www.virtualbox.org/") -and $allOk
$allOk = (Check-Command python "Python 3" "https://www.python.org/") -and $allOk

if (-not $allOk) {
    Write-Host "One or more prerequisites are missing. Please install the suggested software and re-run this script." -ForegroundColor Red
    exit 2
} else {
    Write-Host "All prerequisites found."
}
