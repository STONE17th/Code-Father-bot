import asyncio
import random
import discord
import mysql.connector
from discord.ext import commands
import os
import data_base

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

base = quests = quests_id = None

one_level_role =1000730137731551382
guild_id = 996841246016417962
start_channel = 1006321073958166548

status = '/info'
task_string = f'что выведет в консоль этот код:\n'
answer_string = f'\n\nОтвет отправляй так: /answer <твой вариант ответа>'

@bot.event
async def on_ready():
    global dbase, quests, quests_id
    print('On start')
    dbase = data_base.DataBase(
        mysql.connector.connect(user='root', db='cf_bot', passwd=os.getenv('MYSQL_PWD'), host='mysql'))
    if dbase:
        print('DB Connected... OK')
        quests = dbase.get_quest('quest_list')
        quests_id = dbase.get_quest('quest_id')

# [print(task[1]) for task in quests]
# print(random.choice(quests_id))

@bot.event
async def on_member_join(member):
    welcome = bot.get_channel(start_channel)
    embed=discord.Embed(title="Добро пожаловать!", description=f'Эй, народ! Зацените! Кто это тут к нам залетел :)\n\nПривет, {member.mention}. Я бот канала CODE Father\'s. Пока я мало чего умею, но всё впереди...\n\nЗагляни в ЛС, я там тебе кое-чего прислал', color=0xCC974F)
    await welcome.send(embed=embed)
    await member.send(f'Привет, {member.name}! Рады приветствовать тебя на нашем сервере. Чем мы здесь занимаемся?\nМы создаем дружное коммьюнити из единомышленников в IT сфере. Здесь ты сможешь получить помощь с ДЗ, получить консультацию по текущим темам от однокурсников, пообщаться в прямом эфире с крутыми гостями, которые уже работают в IT, обменяться опытом, найти команду для реализации своих идей, да и просто пообщаться :)\nЕсли возникнут вопросы, то пиши кому-нибудь из администараторов и тебе обязательно ответят\n\nНо для начала было бы неплохо получить роль первого уровня (для доступа к голосовому чату и архиву с полезными ссылками)\nДля этого просто введи на канале /access и мы с тобой всё сделаем!\n\nПриятных тебе минут на сервере и удачного обучения!\n\nP.S. Если увидишь Джонна Конора - передай привет')
    new_user(member)

@bot.event
async def on_member_remove(member):
    dbase.delete_item(member.id, 'user_list')

def new_user(member):
    global quests_id
    task = random.choice(quests_id)
    new_user = ((str(member.id), member.name, task))
    dbase.add_item(new_user, 'user_list')

async def delete_message(ctx):
    try:
        await ctx.message.delete()
    except:
        print('Ошибка')

@bot.command()
async def info(ctx):
    await ctx.author.send(f'{ctx.author.mention}, для получения роли GeekBrains (доступ к голосовому каналу и дополнительным материалам) отправьте боту команду /access')

@bot.command()
async def embed(ctx, *args):
    global dbase
    user_status = dbase.get_user('status', ctx.author.id)
    if user_status == 'admin':
        embed = discord.Embed(color=0xff9900, title=f'{args[0]}', description=f'{args[1]}')
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'Ваш статус - {user_status}, только пользователи со статусом admin могут отправлять EMBED сообщения')


@bot.command()
async def access(ctx, *args):
    global dbase, one_level_role
    guild = bot.get_guild(guild_id)
    member = guild.get_member(ctx.message.author.id)
    if not dbase.get_user('user_list', ctx.author.id):
        new_user(ctx.author)
    for role in member.roles:
        if one_level_role == role.id:
            await ctx.send(f"У вас уже есть такая роль")
            break
    else:
        cur_user = dbase.get_user('user_list', ctx.author.id)
        cur_quest = dbase.get_quest('quest_task', cur_user[0][2])
        await ctx.send(f'{ctx.author.mention}, {task_string}{cur_quest[0]}{answer_string}')

@bot.command()
async def answer(ctx, *args):
    global dbase, quest_answers, simple_role
    if not args == ():
        guild = bot.get_guild(guild_id)
        role = guild.get_role(one_level_role)
        member = guild.get_member(ctx.message.author.id)
        task_id = dbase.get_user('user_task', ctx.author.id)
        print(args[0])
        print(dbase.get_quest('quest_answer', task_id[0])[0])
        if str(args[0]) == str(dbase.get_quest('quest_answer', task_id[0])[0]):
            await delete_message(ctx)
            await member.add_roles(role)
            await ctx.send(f"{ctx.author.mention}, поздравляем! Теперь у тебя роль первого уровня!")
        else:
            await delete_message(ctx)
            await ctx.send(f'{ctx.author.mention}, ну чего-то ты не то написал. Разберись для начала с этим, а потом уже роль')

async def game_info():
    global status
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game(status))
        await asyncio.sleep(15)

bot.loop.create_task(game_info())
bot.run(os.getenv('TOKEN'))