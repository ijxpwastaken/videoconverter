# Terminal ASCII Video Player - Windows Installation Script
# Run this in PowerShell as Administrator

Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Terminal ASCII Video Player - Installation" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ ERROR: Please run PowerShell as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Steps:" -ForegroundColor Yellow
    Write-Host "  1. Right-click PowerShell" -ForegroundColor Yellow
    Write-Host "  2. Select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "  3. Run this script again" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Running as Administrator" -ForegroundColor Green
Write-Host ""

# Step 1: Install Python via Chocolatey
Write-Host "STEP 1: Installing Python..." -ForegroundColor Yellow
$pythonCheck = python --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python already installed: $pythonCheck" -ForegroundColor Green
} else {
    Write-Host "Installing Python with Chocolatey..." -ForegroundColor Cyan

    # Check if Chocolatey is installed
    $chocoCheck = choco --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Chocolatey not found. Installing Chocolatey first..." -ForegroundColor Yellow
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Host "✓ Chocolatey installed" -ForegroundColor Green
    }

    choco install python -y
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python installed successfully" -ForegroundColor Green
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } else {
        Write-Host "❌ Failed to install Python" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Step 2: Install Python packages
Write-Host "STEP 2: Installing Python packages..." -ForegroundColor Yellow
$packages = @("yt-dlp", "opencv-python", "Pillow", "colorama")

foreach ($pkg in $packages) {
    Write-Host "  Installing $pkg..." -ForegroundColor Cyan
    pip install $pkg
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠ Warning: Failed to install $pkg" -ForegroundColor Yellow
    }
}

Write-Host "✓ Python packages installed" -ForegroundColor Green
Write-Host ""

# Step 3: Optional FFmpeg
Write-Host "STEP 3: FFmpeg (optional but recommended)" -ForegroundColor Yellow
$ffmpegCheck = ffmpeg -version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ FFmpeg already installed" -ForegroundColor Green
} else {
    Write-Host "Would you like to install FFmpeg for better quality videos?" -ForegroundColor Cyan
    $response = Read-Host "Install FFmpeg? (y/n)"

    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Installing FFmpeg..." -ForegroundColor Cyan
        choco install ffmpeg -y
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ FFmpeg installed" -ForegroundColor Green
        } else {
            Write-Host "⚠ FFmpeg installation skipped or failed" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Skipping FFmpeg (video quality may be limited)" -ForegroundColor Yellow
    }
}

Write-Host ""

# Step 4: Verify installation
Write-Host "STEP 4: Verifying installation..." -ForegroundColor Yellow
python verify_install.py

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open a YouTube/X/Twitch video link" -ForegroundColor Cyan
Write-Host "  2. Run: python vidterm.py 'VIDEO_URL'" -ForegroundColor Cyan
Write-Host ""
Write-Host "Examples:" -ForegroundColor Cyan
Write-Host "  python vidterm.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'" -ForegroundColor Green
Write-Host "  python vidterm.py 'https://x.com/user/status/000000000'" -ForegroundColor Green
Write-Host "  python vidterm.py 'https://www.twitch.tv/videos/000000000'" -ForegroundColor Green
Write-Host ""
Write-Host "Enjoy! 🎬" -ForegroundColor Cyan
