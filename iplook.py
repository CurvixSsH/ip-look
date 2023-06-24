import discord
from discord.ext import commands
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

API_KEY = 'APY_KEY' # Reemplaza con tu clave API de (ipgeolocation.io) https://ipgeolocation.io

# Aquí definimos la función para guardar las IP con un nombre en el archivo host.txt
""" La función recibe 2 argumentos: el nombre y la dirección IP,
    usamos el modo append (a) para que no borre los datos anteriores. (sin este modo hay errores) """
def save_ip(name, address):
    with open('host.txt', 'a') as f:
        f.write(f'{name}:{address}\n')

# Esta es la función para buscar una IP por su nombre en el archivo host.txt
""" Esta función busca línea por línea hasta encontrar una coincidencia y devuelve el nombre y la IP,
    si no encuentra el nombre devolverá None """
def search_ip(name):
    with open('host.txt', 'r') as f:
        for line in f:
            if name in line:
                return line.strip().split(':')[1]
    return None

# Comando para buscar información de una IP a través de la API ipgeolocation 
""" Esto lo que hace es extraer la información relevante de la respuesta JSON
utilizando las claves correspondientes en el diccionario json_data
La información extraída incluye el nombre del país, la ciudad, el proveedor de servicios de Internet (ISP), la latitud y longitud de la ubicación. 
También se genera un enlace de comprobación de host utilizando la dirección IP especificada """

@bot.command(name="ip")
async def ip_command(ctx, address):
    print(f"Comando recibido: {ctx.message.content}")
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={address}'
                

    response = requests.get(api_url)


    json_data = response.json()

    country = json_data['country_name']
    city = json_data['city']
    isp = json_data['isp']
    lat = json_data['latitude']
    lon = json_data['longitude']
    link = "https://check-host.net/ip-info?host=" + address

    # Verificación si existe un guardado del nombre de la IP en el archivo .txt
    """ Lo que hace es primero abrir el archivo .txt
        y verificar si está almacenado el nombre de la IP. Si no se encuentra una coincidencia para la dirección IP buscada,
        se muestra la información detallada sin el nombre asociado."""
    with open('host.txt', 'r') as f:
        hosts = f.readlines()
        for host in hosts:
            parts = host.strip().split(':')
            if len(parts) > 1 and parts[1] == address:
                name = parts[0]
                await ctx.send(f"```Información de la dirección IP {address} ({name}): \nPaís: {country} \nCiudad: {city} \nISP: {isp} \nLatitud: {lat} \nLongitud: {lon}``` Enlace: {link} \nhttps://cdn.discordapp.com/attachments/983911867401527316/1059354893690880052/tenor.gif")
                return

  
    await ctx.send(f"```Información de la dirección IP {address}: \nPaís: {country} \nCiudad: {city} \nISP: {isp} \nLatitud: {lat} \nLongitud: {lon}``` Enlace: {link} \nhttps://cdn.discordapp.com/attachments/983911867401527316/1059354893690880052/tenor.gif")

# Comando para guardar IP
@bot.command(name="host")
async def host_command(ctx, name, address):
    print(f"Comando recibido: {ctx.message.content}")
    save_ip(name, address)
    await ctx.send(f"La dirección IP {address} ha sido guardada con el nombre {name}.")

# Comando para buscar una  IP por su nombre
@bot.command(name="search")
async def search_command(ctx, name):
    print(f"Comando recibido: {ctx.message.content}")
    address = search_ip(name)
    if address:
        await ctx.send(f"La dirección IP para {name} es: {address}")
    else:
        await ctx.send(f"No se encontró ninguna dirección IP con el nombre {name}.")

bot.run('BOT_TOKEN') # Inserta tu token de bot de Discord 
 # https://discord.com/developers/applications

 
