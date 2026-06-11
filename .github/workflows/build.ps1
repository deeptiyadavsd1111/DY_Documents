param(
    [string]$Target = "Help"
)
 
# --- Helper: Show help ---
function Help {
    Write-Host ""
    Write-Host "Build Script Help"
    Write-Host "====================="
    Write-Host "Usage:"
    Write-Host "  pwsh ./build.ps1 -Target [TaskName]"
    Write-Host ""
    Write-Host "Available Tasks:"
    Write-Host "  Help       Show this help menu (default)"
    Write-Host "  Install    Run 'npm install'"
    Write-Host "  Start      Run 'npm run start'"
    Write-Host "  Default    Runs Install + Start"
    Write-Host "  Clean      Remove node_modules, build, and .docusaurus directories"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  pwsh ./build.ps1                 (shows help)"
    Write-Host "  pwsh ./build.ps1 -Target Install (installs packages)"
    Write-Host "  pwsh ./build.ps1 -Target Start   (starts the app)"
    Write-Host "  pwsh ./build.ps1 -Target Default (install + start)"
    Write-Host "  pwsh ./build.ps1 -Target Clean   (cleans project directories)"
    Write-Host ""
}
 
# --- Check prerequisites ---
function Check-Prereqs {
    Write-Host "Checking prerequisites..."
 
    $node = Get-Command node -ErrorAction SilentlyContinue
    if (-not $node) {
        Write-Error "Node.js is not installed. Download it from https://nodejs.org/"
        exit 1
    }
 
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if (-not $npm) {
        Write-Error "npm is not installed or not in PATH. Install Node.js to get npm."
        exit 1
    }
 
    Write-Host "Node.js version: $(node -v)"
    Write-Host "npm version: $(npm -v)"
}
 
function Install {
    Check-Prereqs
    Write-Host "Installing npm packages..."
    npm install
}
 
function Start {
    Check-Prereqs
    Write-Host "Starting the app..."
    npm run start
}
 
function Default {
    Install
    Start
}
 
function Clean {
    Write-Host "Cleaning project directories..."
    
    $dirsToRemove = @("node_modules", "build", ".docusaurus")
    
    foreach ($dir in $dirsToRemove) {
        if (Test-Path $dir) {
            Write-Host "Removing $dir..."
            Remove-Item $dir -Recurse -Force
            Write-Host "Removed $dir"
        } else {
            Write-Host "$dir not found, skipping..."
        }
    }
    
    Write-Host "Clean completed!"
}

# --- Execute task ---
Write-Host "▶️ Running target: $Target"
Write-Host ""

switch ($Target.ToLowerInvariant()) {
    "help" { Help }
    "install" { Install }
    "start" { Start }
    "default" { Default }
    "clean" { Clean }
    default {
        Write-Host "❌ Unknown target: $Target"
        Help
    }
}
