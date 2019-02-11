python -m venv flask
python -m venv checkEnv
flask\Scripts\pip install flask
mkdir checkEnv\codeToCheck
copy NUL checkEnv\codeToCheck\input.py
copy NUL checkEnv\codeToCheck\input.dfy
go.bat