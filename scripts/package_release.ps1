Param(
    [string]$Out = "release.zip"
)

Write-Output "Creating release package $Out"

# Build list of files to include, excluding common heavy/local dirs
$excludeNames = @('.git', '.vagrant', '.venv', '.pytest_cache', '.env', 'rocky-labs')
$all = Get-ChildItem -Path . -Force
$paths = @()
foreach ($item in $all) {
    if ($excludeNames -contains $item.Name) { continue }
    $paths += $item.FullName
}

if ($paths.Count -eq 0) {
    Write-Error "No items to package"
    exit 1
}

# Ensure destination is a full path under current directory
$OutFull = [System.IO.Path]::GetFullPath((Join-Path -Path (Get-Location) -ChildPath $Out))
$paths = $paths | Where-Object { $_ -ne $OutFull }
Compress-Archive -Path $paths -DestinationPath $OutFull -Force
if (Test-Path $OutFull) {
    Write-Output "Package created: $OutFull"
} else {
    Write-Error "Packaging failed"
    exit 1
}
