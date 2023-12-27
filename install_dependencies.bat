@echo off

REM Обновление pip
python -m pip install --upgrade pip

REM Обновление wheel
python -m pip install --upgrade wheel

REM Обновление setuptools
python -m pip install --upgrade setuptools

REM Установка/обновление библиотек из requirements.txt
python -m pip install -r requirements.txt

REM Установка pre-commit
pre-commit install

REM Удаление текущего бат-файла
del %0