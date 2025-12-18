
# AirBnB Analysis Pipeline Runner
# Usage: ./run_analysis_pipeline.ps1

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   AirBnB Data Pipeline & ML Analysis " -ForegroundColor Cyan
Write-Host "============================================="

# 0. Configuration
$CondaPython = "C:\Users\Shaur\anaconda3\python.exe"
if (-not (Test-Path $CondaPython)) {
    # Try finding it in path if hardcoded path fails
    $CondaPython = (Get-Command python -ErrorAction SilentlyContinue).Source
}

if (-not $CondaPython) {
    Write-Error "Python executable not found. Please ensure Conda is installed."
    exit 1
}
Write-Host "Using Python: $CondaPython" -ForegroundColor Gray

# 1. Credentials Setup
if (-not $env:DB_PASSWORD) {
    Write-Host "`n[Configuration Required]" -ForegroundColor Yellow
    $pass = Read-Host "Enter PostgreSQL Password for user 'postgres' (leaving blank uses default)" -AsSecureString
    if ($pass) {
        $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)
        $env:DB_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    }
}

# 2. Dependency Check
Write-Host "`n[1/5] Checking Dependencies..."
try {
    # Using the specific python executable to install libs
    & $CondaPython -m pip install scikit-learn pandas numpy sqlalchemy psycopg2-binary matplotlib seaborn | Out-Null
    Write-Host "   Dependencies verified." -ForegroundColor Green
}
catch {
    Write-Host "   Warning: Dependency check noticed issues. Proceeding anyway..." -ForegroundColor Yellow
}

# 3. Data Transformation (SQL + Outlier Removal)
Write-Host "`n[2/5] Running Transformation (ELT + Statistical Cleaning)..."
& $CondaPython transform_data.py
if ($LASTEXITCODE -ne 0) { 
    Write-Error "Transformation failed. Check database credentials in config.py or the password provided."
    exit 1 
}

# 4. Data Export
Write-Host "`n[3/5] Exporting Clean Data for Visualization..."
& $CondaPython export_extended.py
if ($LASTEXITCODE -ne 0) { Write-Error "Export failed."; exit 1 }

# 5. Visualization (Charts)
Write-Host "`n[4/5] Generating Visualizations (Heatmaps, Distributions)..."
& $CondaPython visualize_results.py
if ($LASTEXITCODE -ne 0) { Write-Error "Visualization failed."; exit 1 }

# 6. Machine Learning Analysis
Write-Host "`n[5/5] Running ML Price Driver Analysis..."
& $CondaPython analyze_ml.py
if ($LASTEXITCODE -ne 0) { Write-Error "ML Analysis failed."; exit 1 }

Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "   ✅ PIPELINE COMPLETE " -ForegroundColor Green
Write-Host "   Check 'assets/' folder for new charts:" -ForegroundColor White
Write-Host "   - 11_feature_importance.png"
Write-Host "   - 12_correlation_matrix.png"
Write-Host "============================================="
Pause
