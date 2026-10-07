# Install the theme and the snippets into a vault. This is the PowerShell version of install.sh.
#
# Usage: .\scripts\install.ps1 -Vault C:\path\to\vault [-Link]
#
# The vault is the folder that holds the hidden .obsidian folder. The script copies manifest.json
# and theme.css to .obsidian\themes\Lexmechanic and the files of snippets\ to .obsidian\snippets.
# With -Link it makes symbolic links in place of copies. A link needs developer mode or an
# administrator on Windows. The script does not turn the theme on: choose it in
# Settings, Appearance.
param(
    [Parameter(Mandatory = $true)][string]$Vault,
    [switch]$Link
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$obsidian = Join-Path $Vault '.obsidian'
if (-not (Test-Path -LiteralPath $obsidian -PathType Container)) {
    Write-Error "$Vault has no .obsidian folder. Open the vault in Obsidian once, or check the path."
}
$theme = Join-Path $obsidian 'themes\Lexmechanic'
$snippets = Join-Path $obsidian 'snippets'
New-Item -ItemType Directory -Force -Path $theme, $snippets | Out-Null

function Install-One([string]$Source, [string]$Folder) {
    $target = Join-Path $Folder (Split-Path -Leaf $Source)
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Force }
    if ($Link) {
        New-Item -ItemType SymbolicLink -Path $target -Target $Source | Out-Null
    } else {
        Copy-Item -LiteralPath $Source -Destination $target
    }
}

foreach ($name in 'manifest.json', 'theme.css') { Install-One (Join-Path $repo $name) $theme }
foreach ($file in Get-ChildItem -LiteralPath (Join-Path $repo 'snippets') -Filter '*.css') {
    Install-One $file.FullName $snippets
}
$mode = if ($Link) { 'link' } else { 'copy' }
Write-Host "installed into $obsidian ($mode)"
