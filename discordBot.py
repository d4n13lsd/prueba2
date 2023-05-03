import json, os
from discord.ext import commands
import discord
from discord.ext.commands import has_any_role, has_permissions


class Welcome_Embed():
	def __init__(self,member):
		#member es elnickname
		self.member = member

	@property
	def enviar(self):
		self.embed = discord.Embed(title=f"Hola {self.member}. para unirte debes aceptar las siguientes reglas...", colour=int("DC75FF",16))
		self.embed.add_field(name="Reglas:",value= "1) ser respetuoso. / 2) no contarle a nadie / #)pruena de regla", inline= False)
		self.embed.add_field(name="Escribe el siguiente comando si estas deacuerdo:",value= "!acepto", inline= False)
		return self.embed
	


class crear_respuesta():
	def __init__(self,title,content):
		self.title = title
		self.content = content

		self.respuesta = discord.Embed(
			title = self.title,description=self.content,
			colour=int("00D8FF",16)
		)

	@property
	def enviar(self):
		return self.respuesta
	
def main():

	def create_config_archive():
		template = {
		'prefix': '!', 
		'token': "introduce tu token", 
		}
		with open('config.json', 'w') as f:
			json.dump(template, f)


	def read_config_archive():
		with open('config.json') as f:
			config_data = json.load(f)
		return config_data


	if not os.path.exists('config.json'):
		print('Creando archivo de configuración')
		create_config_archive()

	
	# Parametros iniciales
	
	config_data = read_config_archive()
	prefix = config_data["prefix"]
	token = config_data["token"]
	intents = discord.Intents.all()
	bot = commands.Bot(
		command_prefix = prefix, 
		intents = intents, 
		description = "Bot moderador")
	
	
	# Comandos
	@bot.command(name="saludar", help="El bot saludara")
	async def saludar(ctx):
		await ctx.reply(f'Hola {ctx.author}, como vas?')

	@bot.command(name="sumar", help="El bot sumara")
	async def sumar(ctx, num1:int, num2:int):
		suma = num1 + num2
		respuesta = crear_respuesta('La suma es:',suma)
		await ctx.reply(embed =  respuesta.enviar)
	
	@bot.command(name='acepto', help='Te agrega el rol usuario')
	async def add_user_role(ctx):
		#condicional para que funcione solo por mensaje directo
		if isinstance(ctx.channel, discord.channel.DMChannel):
			#obtenemos nuestro servidor mediante la ID
			server = bot.get_guild(1101343689852321803)
			#obtenemos el rol del usuario de nuestro server
			rol = server.get_role(1101710230359920720)
			#obtenemos al usuario mediante su id  en el contexto
			member = server.get_member(ctx.message.author.id)
			#le asignamos el rol
			await member.add_roles()
			#le mandamos unmensaje explicandole que ya se unio al server
			await ctx.author.send('Has pasado los requisitos para entrar a la guarida')


	# Eventos
	@bot.event
	async def on_member_join(member):
		#id del canal de bienvenida
		welcome_channel = bot.get_channel(1101343690309513268)
		#usamos la plantilla para crear la respuesta 
		welcome_embed = Welcome_Embed(member.name)
		#enviamos el embed
		await member.send(embed= welcome_embed.enviar)
		#damos la bienvenida}
		await welcome_channel.send(f'Bienvenida a la guarida secreta, {str(member.mention)}. Revisa tus mensajes privados para aceptar las reglas')

	@bot.event
	async def on_ready():
		activity = discord.Game(name="Eres una agente secreta")
		await bot.change_presence(activity=activity)
		print('El bot esta funcionando correctamente.')

	bot.run(token)



if __name__ == '__main__':
	main()
