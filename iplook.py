import discord 
from discord import Embed
from discord.ext import commands
import requests
from ipaddress import ip_address
from config import API_KEY, BOT_TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

bot.remove_command("help")

def save_ip(name, address):
    with open('host.txt', 'a') as f:
        f.write(f'{name}:{address}\n')

def search_ip(name):
    with open('host.txt', 'r') as f:
        for line in f:
            if name in line:
                return line.strip().split(':')[1]
    return None

@bot.command(name="ip")
async def ip_command(ctx, address):
    print(f"Comando recibido: {ctx.message.content}")
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={address}'
    response = requests.get(api_url)
    json_data = response.json()
    country = json_data['country_name']
    country_flag = json_data['country_flag']
    city = json_data['city']
    isp = json_data['isp']
    lat = json_data['latitude']
    lon = json_data['longitude']
    link = "https://check-host.net/ip-info?host=" + address
    gif_url = "https://cdn.discordapp.com/attachments/983911867401527316/1059354893690880052/tenor.gif"
    with open('host.txt', 'r') as f:
        hosts = f.readlines()
        for host in hosts:
            parts = host.strip().split(':')
            if len(parts) > 1 and parts[1] == address:
                name = parts[0]
                embed = Embed(title=f"Información de la dirección IP {address} ({name})", color=0x00ff00)
                embed.set_thumbnail(url=country_flag)
                embed.add_field(name="País", value=country, inline=False)
                embed.add_field(name="Ciudad", value=city, inline=False)
                embed.add_field(name="ISP", value=isp, inline=False)
                embed.add_field(name="Latitud", value=lat, inline=False)
                embed.add_field(name="Longitud", value=lon, inline=False)
                embed.add_field(name="Enlace", value=link, inline=False)
                embed.set_image(url=gif_url)
                await ctx.send(embed=embed)
                return
    embed = Embed(title=f"Información de la dirección IP {address}", color=0x00ff00)
    embed.set_thumbnail(url=country_flag)
    embed.add_field(name="País", value=country, inline=False)
    embed.add_field(name="Ciudad", value=city, inline=False)
    embed.add_field(name="ISP", value=isp, inline=False)
    embed.add_field(name="Latitud", value=lat, inline=False)
    embed.add_field(name="Longitud", value=lon, inline=False)
    embed.add_field(name="Enlace", value=link, inline=False)
    embed.set_image(url=gif_url)
    await ctx.send(embed=embed)

@bot.command(name="label")
async def label_command(ctx, name, address):
    print(f"Comando recibido: {ctx.message.content}")
    try:
        ip_address(address)
    except ValueError:
        embed = Embed(title="La dirección IP no es válida.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    if len(name) > 20:
        embed = Embed(title="El nombre no puede tener más de 20 caracteres.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    save_ip(name, address)
    embed = Embed(title=f"La dirección IP {address} ha sido guardada con el nombre {name}.", color=0xFFFF00)
    await ctx.send(embed=embed)

@bot.command(name="search")
async def search_command(ctx, name):
    print(f"Comando recibido: {ctx.message.content}")
    address = search_ip(name)
    if address:
        link = f"https://check-host.net/ip-info?host={address}"
        embed = Embed(title=f"Resultado de la búsqueda", color=0x0000FF)
        embed.add_field(name="Nombre", value=name, inline=True)
        embed.add_field(name="Dirección IP", value=address, inline=True)
        embed.add_field(name="Enlace", value=link, inline=False)
        await ctx.send(embed=embed)
    else:
        embed = Embed(title=f"No se encontró ninguna dirección IP con el nombre {name}.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(name="help")
async def help_command(ctx):
    print(f"Comando recibido: {ctx.message.content}")
    embed = Embed(title="Comandos disponibles", color=0xFFA500) 
    embed.add_field(name="/ip [dirección IP]", value="Muestra información sobre la dirección IP especificada.", inline=False)
    embed.add_field(name="/label [nombre] [dirección IP]", value="Guarda la dirección IP con el nombre especificado.", inline=False)
    embed.add_field(name="/search [nombre]", value="Busca una dirección IP por nombre y muestra la dirección IP encontrada.", inline=False)
    embed.add_field(name="/help", value="Muestra esta lista de comandos disponibles.", inline=False)
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
