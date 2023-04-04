# ip-geolocalizacion 
Este código es un bot de Discord que permite buscar información sobre una dirección IP utilizando una API de geolocalización y guardar direcciones IP con un nombre asociado en un archivo de texto. También permite buscar una dirección IP por su nombre y mostrar su información.

# API IPGEO Y TOKEN BOT DISCORD

crear cuenta y obtener clave luego remplazala en el codigo linea 11 (API_KEY) https://ipgeo.io

crear un bot de discord invitarlo a tu servidor luego obtener token y remplazarlo en la linea 83 del codigo 
(TOKEN_BOT) https://discord.com/developers/applications

# INSTALACION

pip install discord

pip install requests

git clone

cd ip-look

python iplook.py

# COMANDOS

los comandos deben ejecutarse en el canal de discord con el bot 

/ip 192.168.1.17  (esto buscara informacion de esa direccion ip)

/host ip_privada 192.168.1.17  (esto guardara esa direccion ip con ese nombre)

/search ip_privada  (esto buscara la direccion ip por el nombre)
