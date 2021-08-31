import discord
from discord.ext import commands
from random import choice
from os import chdir
import asyncio
import logging as log

log.basicConfig(filename="/home/pi/Bot/logbot.log",
filemode='w',format='%(asctime)s::%(levelname)s::%(message)s',level=log.INFO)


bot = commands.Bot(command_prefix = "p!", description = "Bot fun du serveur L'Arche")
bot.remove_command('help')
log.info("Compiling joke...")
chdir("/home/pi/Bot/data")
fic = open("blagues.txt", "r")
bla = fic.read().splitlines()
for nb in range(len(bla)):
 bla[nb] = bla[nb].split("==")
log.info(bla)
fic.close()
num=0

@bot.event
async def on_ready():
 log.info("Pikasso is ready!")
 await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="une blague"))

@bot.command()
async def joke(ctx):
 global bla, num
 act = bla[num]
 num=num+1
 if num==len(bla):
  num=0
 embed=discord.Embed(title=act[0], description="||"+act[1]+"||", color=0xFF5733)
 embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
 await ctx.send(embed=embed)

@bot.command()
async def addjoke(ctx,*args):
 global bla
 chdir("/home/pi/Bot/data")
 fic = open("blagues.txt", "a")
 fic.write(args[0]+"=="+args[1]+"\r\n")
 fic.close()
 bla.append([args[0],args[1]])
 embed=discord.Embed(title="Votre blague a  bien été ajoutée!", color=0xFF5733)
 embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
 await ctx.send(embed=embed)

@bot.command()
async def jokelist(ctx):
 global bla
 temp = []
 for x in bla:
  temp.append('\n'.join(x))
 nb = 0
 embed=discord.Embed(title="Liste des blagues:",description=temp[0], color=0xFF5733)
 embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
 msg = await ctx.send(embed=embed)
 await msg.add_reaction('⏭️')
 def check(reaction,user):
  return user == ctx.author and reaction.emoji=='⏭️'
 for x in range(len(temp)-1):
  try:
   reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
  except asyncio.TimeoutError:
   embed=discord.Embed(title="Votre commande a été annulée", color=0xFF5733)
   embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
   await ctx.send(embed=embed)
  else:
   nb = nb+1
   embed=discord.Embed(title="Liste des blagues:",description=temp[nb], color=0xFF5733)
   embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
   await msg.edit(embed=embed)

@bot.command()
async def embed(ctx, *args):
    aut = ctx.message.author
    if ctx.channel.permissions_for(aut).manage_messages:
     embed=discord.Embed(title=args[0], description=args[1], color=0xFF5733)
    else:
     embed=discord.Embed(title="Vous n'êtes pas autorisé à utiliser cette commande", color=0xFF5733)
    embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
    msg = await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed=discord.Embed(title="Le ping est de "+str(round(bot.latency*1000))+" millisecondes" , color=0xFF5733)
    embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
    msg = await ctx.send(embed=embed)


@bot.command()
async def help(ctx, comm=None):
    if comm == None:
     embed=discord.Embed(title="Liste des commandes :", description=
"""**Général**\n  ***help*** : Montre ce message\n  ***embed*** : Crée un message à contenu riche\n
**Blagues**\n  ***joke*** : Affiche une blague\n  ***addjoke*** : Ajouter une blague\n  ***jokelist*** : Affiche une liste de toutes les blagues""", color=0xFF5733)
    elif comm == "joke":
      embed=discord.Embed(title="La commande joke",description="Affiche une blague\nUtilisation : *p!joke*", color=0xFF5733)
    elif comm == "addjoke":
      embed=discord.Embed(title="La commande addjoke",description=
'Ajoute une blague\nUtilisation : *p!addjoke "Quel est la couleur du cheval blanc d\'Henri 4?" "Blanc !"*', color=0xFF5733)
    elif comm == "jokelist":
      embed=discord.Embed(title="La commande jokelist",description=
'Affiche la liste des blagues\nUtilisation : *p!jokelist\n(Réagir à l\'émoji permet de passer à la prochaine blague)*', color=0xFF5733)
    elif comm == "embed":
      embed=discord.Embed(title="La commande embed",description=
'Envoie un message à contenu riche personnalisé\nUtilisation : *p!embed "titre de votre message" "description de votre message"*', color=0xFF5733)

    embed.set_author(name="Pikasso", icon_url="https://cdn.discordapp.com/attachments/805834898040291438/821137637486100509/Pikasso.png")
    msg = await ctx.send(embed=embed)


bot.run('ODMzNzIyMTYzMTMxMzE4Mjgz.YH2eRQ.nzJ9Y3F3QJmsl0rSIyJ68D9pH_c')

