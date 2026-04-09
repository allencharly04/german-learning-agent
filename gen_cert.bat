@echo off
echo Generating self-signed SSL certificate...
echo.

openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=192.168.0.35"

if exist cert.pem (
    echo.
    echo SUCCESS! cert.pem and key.pem created.
    echo.
    echo Now run:  python launch.py
    echo Then open:  https://192.168.0.35:8764  on your phone
    echo.
    echo Your browser will show a security warning - tap Advanced then Proceed. That is safe.
) else (
    echo.
    echo FAILED. Make sure openssl is available.
    echo Run:  conda install openssl -y
    echo Then try this file again.
)

pause
