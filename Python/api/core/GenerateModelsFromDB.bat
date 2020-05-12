cd ..\..\

venv\Scripts\sqlacodegen postgresql+pg8000://postgres:123qweasdZXC@localhost/how_to_build --outfile %~dp0models_gen.py --schema public
pause