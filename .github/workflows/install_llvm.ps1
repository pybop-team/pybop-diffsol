# Define the URL and destination paths
$url = "https://github.com/vovkos/llvm-package-windows/releases/download/llvm-17.0.6/llvm-17.0.6-windows-x86-msvc17-libcmt.7z"
$destinationFolder = "$PSScriptRoot\llvm"
$archivePath = "$destinationFolder\llvm.7z"

# Create destination folder if it doesn't exist
if (-not (Test-Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder | Out-Null
}

# Download the file
Write-Host "Downloading LLVM package..."
Invoke-WebRequest -Uri $url -OutFile $archivePath

# Check if 7z.exe is available
$sevenZip = "7z"
if (-not (Get-Command $sevenZip -ErrorAction SilentlyContinue)) {
    Write-Error "7z.exe not found. Please install 7-Zip and add it to your PATH."
    exit 1
}

# Extract the archive
Write-Host "Extracting archive..."
& $sevenZip x $archivePath -o$destinationFolder -y

Write-Host "Done! Extracted to: $destinationFolder"