@echo off
setlocal

echo =====================================================================
echo  CropWise - ML-Based Crop Recommendation System [SDG 2: Zero Hunger]
echo =====================================================================
echo.

:: 1. Detect Python command (try 'py' first, then 'python')
set "PYTHON_CMD="
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py"
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        echo [ERROR] Neither 'py' nor 'python' was found in your system PATH.
        echo Please ensure Python 3.9+ is installed and available.
        pause
        exit /b 1
    )
)

echo [*] Detected Python executable: %PYTHON_CMD%

:: 2. Check or create virtual environment (.venv)
if not exist ".venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment in .venv...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [+] Virtual environment created successfully.
) else (
    echo [+] Existing virtual environment found in .venv.
)

:: 3. Activate virtual environment
call .venv\Scripts\activate.bat
echo [+] Virtual environment activated.

:: 4. Install dependencies
echo [*] Checking and installing required dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)

:: 5. Generate synthetic dataset if not already present
if not exist "data\crop_data.csv" (
    echo [*] Generating synthetic agricultural dataset [2200 records]...
    python generate_data.py
    if errorlevel 1 (
        echo [ERROR] Data generation failed.
        pause
        exit /b 1
    )
) else (
    echo [+] Dataset 'data\crop_data.csv' already exists.
)

:: 6. Train Random Forest model if not already trained
if not exist "models\crop_model.joblib" (
    echo [*] Training Random Forest ML model and evaluating test metrics...
    python train_model.py
    if errorlevel 1 (
        echo [ERROR] Model training failed.
        pause
        exit /b 1
    )
) else (
    echo [+] Model artifact 'models\crop_model.joblib' already exists.
)

:: 7. Launch Streamlit Application
echo.
echo =====================================================================
echo  Launching CropWise Streamlit Dashboard...
echo  Local URL: http://localhost:8501
echo  [Press Ctrl+C in this terminal window to stop the server]
echo =====================================================================
echo.
python -m streamlit run app.py

pause
