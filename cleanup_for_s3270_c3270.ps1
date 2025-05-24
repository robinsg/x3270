# PowerShell script to cleanup x3270 repository for s3270/c3270 only build
# Removes all Windows-specific components, X11 GUI, backend, and other unnecessary parts

Write-Host "Starting cleanup for s3270/c3270 only build..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "configure.in")) {
    Write-Error "Error: Not in x3270 root directory (configure.in not found)"
    exit 1
}

# Directories to completely remove
$RemoveDirs = @(
    # Windows components
    "wc3270",
    "ws3270", 
    "wb3270",
    "wpr3287",
    "wx3270if",
    "wmitm",
    "wplayback",
    
    # X11 GUI
    "x3270",
    
    # Backend
    "b3270",
    
    # TCL integration
    "tcl3270",
    
    # Utilities
    "playback",
    "mitm",
    
    # Development tools
    "VisualStudio",
    "Webpage", 
    "ReleaseTools",
    "ConvTools",
    
    # Test/relay tools
    "st-relay"
)

# Files to remove (Windows-specific or unnecessary)
$RemoveFiles = @(
    "run_windows_tests.py"
)

# Directories to keep (essential for s3270/c3270)
$KeepDirs = @(
    "Common",      # Shared source code
    "s3270",       # s3270 component  
    "c3270",       # c3270 component
    "lib",         # Required libraries
    "include",     # Header files
    "Shared",      # Shared files
    "pr3287",      # Print utility
    "x3270if",     # Interface utility
    "ibm_hosts",   # Host configuration
    ".git",        # Git repository
    ".vscode",     # IDE settings
    ".logs",       # Logs
    ".evfevent"    # Event files
)

$RemovedCount = 0

# Remove unnecessary directories
foreach ($DirName in $RemoveDirs) {
    if (Test-Path $DirName -PathType Container) {
        try {
            Remove-Item $DirName -Recurse -Force
            Write-Host "Removed directory: $DirName" -ForegroundColor Yellow
            $RemovedCount++
        }
        catch {
            Write-Warning "Error removing directory $DirName : $_"
        }
    }
    else {
        Write-Host "Directory not found (already removed?): $DirName" -ForegroundColor Gray
    }
}

# Remove unnecessary files
foreach ($FileName in $RemoveFiles) {
    if (Test-Path $FileName -PathType Leaf) {
        try {
            Remove-Item $FileName -Force
            Write-Host "Removed file: $FileName" -ForegroundColor Yellow
            $RemovedCount++
        }
        catch {
            Write-Warning "Error removing file $FileName : $_"
        }
    }
    else {
        Write-Host "File not found (already removed?): $FileName" -ForegroundColor Gray
    }
}

# Clean up extern/ subdirectories but keep the main extern/ directory
if (Test-Path "extern" -PathType Container) {
    Write-Host "Cleaning extern/ subdirectories..." -ForegroundColor Cyan
    Get-ChildItem "extern" -Directory | ForEach-Object {
        try {
            Remove-Item $_.FullName -Recurse -Force
            Write-Host "Removed extern subdirectory: $($_.Name)" -ForegroundColor Yellow
            $RemovedCount++
        }
        catch {
            Write-Warning "Error removing extern subdirectory $($_.Name) : $_"
        }
    }
}

Write-Host "`nCleanup complete! Removed $RemovedCount items." -ForegroundColor Green
Write-Host "Kept essential directories: $($KeepDirs -join ', ')" -ForegroundColor Green

# List remaining directories
Write-Host "`nRemaining directories:" -ForegroundColor Cyan
Get-ChildItem -Directory | Where-Object { -not $_.Name.StartsWith('.') } | Sort-Object Name | ForEach-Object {
    Write-Host "  $($_.Name)/" -ForegroundColor White
}

Write-Host "`nRepository size has been significantly reduced for s3270/c3270 only build!" -ForegroundColor Green
