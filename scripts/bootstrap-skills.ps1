<#
.SYNOPSIS
  Restore the two pinned development tools into src/skills/.

.DESCRIPTION
  AgentCity does not vendor the ADK Agent Builder or SkillBridge source in Git.
  This script clones them from a URL you supply, or copies them from a local
  checkout, then checks out the pinned commit recorded in the project docs.

  Repository URLs are intentionally NOT hardcoded. Pass them explicitly, or use
  -FromLocal with an existing checkout.

.EXAMPLE
  pwsh -File scripts/bootstrap-skills.ps1 `
    -AdkRepoUrl "https://example.invalid/your-adk-builder" `
    -SkillsRepoUrl "https://example.invalid/your-skills-bridge"

.EXAMPLE
  pwsh -File scripts/bootstrap-skills.ps1 `
    -AdkFromLocal "C:\src\adk-agent-builder" `
    -SkillsFromLocal "C:\src\skills-bridge"
#>
[CmdletBinding(DefaultParameterSetName = 'Remote')]
param(
    [Parameter(ParameterSetName = 'Remote')]
    [string]$AdkRepoUrl,

    [Parameter(ParameterSetName = 'Remote')]
    [string]$SkillsRepoUrl,

    [Parameter(ParameterSetName = 'Local')]
    [string]$AdkFromLocal,

    [Parameter(ParameterSetName = 'Local')]
    [string]$SkillsFromLocal,

    [string]$Root,

    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'

if (-not $Root) {
    $Root = Split-Path -Parent $PSScriptRoot
}
$Root = (Resolve-Path -LiteralPath $Root).Path

$AdkSha = 'a74d73b20447c8d9beab999bbfa5ddb7d6d748b4'
$SkillsSha = '25c352e6219e0f9ca45bdbc9a2ff0bafae4ddb06'

$AdkTarget = Join-Path $Root 'src/skills/adk-agent-builder'
$SkillsTarget = Join-Path $Root 'src/skills/skills-bridge'

function Assert-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

function Get-HeadSha([string]$Path) {
    return (git -C $Path rev-parse HEAD).Trim()
}

function Install-Tool {
    param(
        [string]$Name,
        [string]$Target,
        [string]$Sha,
        [string]$RepoUrl,
        [string]$FromLocal,
        [string]$ParamBase
    )

    if (Test-Path (Join-Path $Target '.git')) {
        $current = Get-HeadSha $Target
        if ($current -eq $Sha) {
            Write-Host "[ok] $Name already at $Sha" -ForegroundColor Green
            return
        }
        if ($VerifyOnly) {
            throw "$Name is at $current, expected $Sha (verify-only mode)."
        }
        Write-Host "[update] $Name is at $current; checking out $Sha" -ForegroundColor Yellow
        git -C $Target fetch --quiet --all
        git -C $Target checkout --quiet $Sha
        $verified = Get-HeadSha $Target
        if ($verified -ne $Sha) { throw "$Name checkout failed: expected $Sha, got $verified" }
        return
    }

    if ($VerifyOnly) {
        throw "$Name is missing at $Target (verify-only mode)."
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Target) | Out-Null

    if ($FromLocal) {
        if (-not (Test-Path (Join-Path $FromLocal '.git'))) {
            throw "Local source for $Name has no Git repository: $FromLocal"
        }
        Write-Host "[copy] $Name from $FromLocal"
        git clone --quiet $FromLocal $Target
    }
    elseif ($RepoUrl) {
        Write-Host "[clone] $Name"
        git clone --quiet $RepoUrl $Target
    }
    else {
        throw "No source supplied for $Name. Pass -${ParamBase}RepoUrl or -${ParamBase}FromLocal. See docs/runbooks/dev-setup.md."
    }

    git -C $Target checkout --quiet $Sha
    $verified = Get-HeadSha $Target
    if ($verified -ne $Sha) {
        throw "$Name checkout failed: expected $Sha, got $verified"
    }
    Write-Host "[ok] $Name pinned at $Sha" -ForegroundColor Green
}

Assert-Command git
Assert-Command python

Write-Host "AgentCity skill bootstrap"
Write-Host "Root: $Root"
Write-Host ""

if ($PSCmdlet.ParameterSetName -eq 'Local' -and ($AdkFromLocal -or $SkillsFromLocal)) {
    Install-Tool -Name 'ADK Agent Builder' -Target $AdkTarget -Sha $AdkSha -FromLocal $AdkFromLocal -ParamBase 'Adk'
    Install-Tool -Name 'SkillBridge' -Target $SkillsTarget -Sha $SkillsSha -FromLocal $SkillsFromLocal -ParamBase 'Skills'
}
else {
    Install-Tool -Name 'ADK Agent Builder' -Target $AdkTarget -Sha $AdkSha -RepoUrl $AdkRepoUrl -ParamBase 'Adk'
    Install-Tool -Name 'SkillBridge' -Target $SkillsTarget -Sha $SkillsSha -RepoUrl $SkillsRepoUrl -ParamBase 'Skills'
}

Write-Host ""
Write-Host "Tool verification"
$env:PYTHONPATH = Join-Path $SkillsTarget 'src'
$skillbridgeVersion = python -m skillbridge --version 2>&1
if ($LASTEXITCODE -ne 0) { throw "SkillBridge failed to start: $skillbridgeVersion" }
Write-Host "  SkillBridge: $skillbridgeVersion"

$adkVersion = python -c "import importlib.metadata as m; print(m.version('google-adk'))" 2>&1
if ($LASTEXITCODE -ne 0) { throw "google-adk is not installed in the active Python environment." }
Write-Host "  google-adk:  $adkVersion"

Write-Host ""
Write-Host "Done. SkillBridge runtime path: src/skills/skills-bridge/src"
