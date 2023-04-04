import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='/', intents=intents)

API_KEY = 'API_KEY' # Remplaza con tu clave api de (ipgeolocation.io) https://ipgeolocation.io

# Aca definimos la función para guardar las IP con un nombre en el archivo host.txt (debes especificar la ruta correcta del archivo)
""" la funcion recive 2 argumentos el nombre y la direccion ip,
    usamos el modo append (a) para que no borre los datos anteriores. (sin este modo hay errores) """
def save_ip(name, address):
    with open('C:\\INSERTE_RUTA\\host.txt', 'a') as f:
        f.write(f'{name}:{address}\n')

# esta es la función para buscar una IP por su nombre en el archivo host.txt (debes especificar la misma ruta que antes)
""" esta funcion busca linea por linea hasta encontrar una coincidencia y devuelve el nombre y la ip,
    si no encuentra el nombre devolvera none """
def search_ip(name):
    with open('C:\\INSERTE_RUTA\\host.txt', 'r') as f:
        for line in f:
            if name in line:
                return line.strip().split(':')[1]
    return None

# Comando para buscar información de una IP atraves de la api ipgeolocation 
""" esto lo que hace es xtrae la información relevante de la respuesta JSON
utilizando las claves correspondientes en el diccionario json_data
La información extraída incluye el nombre del país, la ciudad, el proveedor de servicios de Internet (ISP), la latitud y longitud de la ubicación. 
También se genera un enlace de comprobación de host utilizando la dirección IP especificada """
@bot.command(name="ip")
async def ip_command(ctx, address):
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={address}'
                

    response = requests.get(api_url)


    json_data = response.json()

    country = json_data['country_name']
    city = json_data['city']
    isp = json_data['isp']
    lat = json_data['latitude']
    lon = json_data['longitude']
    link = "https://check-host.net/ip-info?host=" + address

    #verificacion si exixte un guardado del nombre de la ip en el archivo .txt (insertar ruta)
    """ Lo que hace es primero abrir el archivo.text
        y verificar si esta almacenada el nombre de la ip Si no se encuentra una coincidencia para la dirección IP buscada,
        se muestra la información detallada sin el nombre asociado."""
    with open('C:\\INSERTE_RUTA\\host.txt', 'r') as f:
        hosts = f.readlines()
        for host in hosts:
            parts = host.strip().split(':')
            if parts[1] == address:
                name = parts[0]
                await ctx.send(f"```Información de la dirección IP {address} ({name}): \nPaís: {country} \nCiudad: {city} \nISP: {isp} \nLatitud: {lat} \nLongitud: {lon}``` Enlace: {link} \nhttps://cdn.discordapp.com/attachments/983911867401527316/1059354893690880052/tenor.gif")
                return

  
    await ctx.send(f"```Información de la dirección IP {address}: \nPaís: {country} \nCiudad: {city} \nISP: {isp} \nLatitud: {lat} \nLongitud: {lon}``` Enlace: {link} \nhttps://cdn.discordapp.com/attachments/983911867401527316/1059354893690880052/tenor.gif")

#comando para guardar ip
@bot.command(name="host")
async def host_command(ctx, name, address):
    save_ip(name, address)
    await ctx.send(f"La dirección IP {address} ha sido guardada con el nombre {name}.")

# Comando para buscar una  IP por su nombre
@bot.command(name="search")
async def search_command(ctx, name):
    address = search_ip(name)
    if address:
        await ctx.send(f"La dirección IP para {name} es: {address}")
    else:
        await ctx.send(f"No se encontró ninguna dirección IP con el nombre {name}.")

bot.run('TOKEN_BOT') #inserta tu token de bot de discord 
 #https://discord.com/developers/applications
