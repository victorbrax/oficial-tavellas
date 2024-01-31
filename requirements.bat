:: Criação e ativação do ambiente virtual
python -m venv venv
call venv\Scripts\activate.bat

:: Atualização de pip
python.exe -m pip install --upgrade pip

:: Instalação dos requisitos
pip install -r requirements.txt

:: Desativação do ambiente virtual
call deactivate