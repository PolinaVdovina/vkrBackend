cd ..\..\..\

venv\Scripts\sqlacodegen postgresql+pg8000://postgres:polina1234@localhost/vkrDatabase --outfile %~dp0models_gen.py --schema public
pause