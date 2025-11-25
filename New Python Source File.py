# ensure we're in the repo root
Set-Location "C:\Users\Owner\Project Freedom Clean"

# create directories
New-Item -ItemType Directory -Path src, warhead, scripts, tests -Force

# create basic package files
@'
# Project Freedom (Warhead) - minimal starter
# Add docs and instructions here.
'@ | Out-File -FilePath README.md -Encoding utf8

# minimal requirements
@'
pytest
black
flake8
coverage
'@ | Out-File -FilePath requirements.txt -Encoding utf8

# .gitignore (Python + venv)
@'
venv/
__pycache__/
*.pyc
.env
.DS_Store
.idea/
.vscode/
'@ | Out-File -FilePath .gitignore -Encoding utf8
