from discord import utils
import asyncio
import random
import discord
import mysql.connector
from discord.ext import commands
import os
import data_base

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# dbase = quests = quests_id = None

cf_role = {1010186572156641290 : 0,
           1000730137731551382 : 1,
           1009910414961811486 : 2,
           1009928506966290442 : 3,
           1001397006993985646 : 4}
vpb_role = 1008289239210938518
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
        quests = dbase.get_quest('all')
        quests_id = dbase.get_quest('id')

@bot.event
async def on_member_join(member):
    embed=discord.Embed(title="Добро пожаловать!", description=f'Эй, народ! Зацените! Кто это тут к нам залетел :)\n\nПривет, {member.mention}. Я бот канала CODE Father\'s. Пока я мало чего умею, но всё впереди...\n\nЗагляни в ЛС, я там тебе кое-чего прислал', color=0xCC974F)
    await bot.get_channel(start_channel).send(embed=embed)
    await member.send(f'Привет, {member.name}! Рады приветствовать тебя на нашем сервере. Чем мы здесь занимаемся?\nМы создаем дружное коммьюнити из единомышленников в IT сфере. Здесь ты сможешь получить помощь с ДЗ, получить консультацию по текущим темам от однокурсников, пообщаться в прямом эфире с крутыми гостями, которые уже работают в IT, обменяться опытом, найти команду для реализации своих идей, да и просто пообщаться :)\nЕсли возникнут вопросы, то пиши кому-нибудь из администараторов и тебе обязательно ответят\n\nНо для начала было бы неплохо получить роль первого уровня (для доступа к голосовому чату и архиву с полезными ссылками)\nДля этого просто введи на канале /access и мы с тобой всё сделаем!\n\nПриятных тебе минут на сервере и удачного обучения!\n\nP.S. Если увидишь Джонна Конора - передай привет')
    new_user(member)

def new_user(member):
    global quests_id
    task = random.choice(quests_id)
    user = ((str(member.id), member.name, task, 10, 0))
    dbase.add_item('new_user', user)
    await member.add_roles(get_key(cf_role, 4))

async def check_user(ctx):
    global dbase
    user = dbase.get_user('user', ctx.author.id)
    await delete_message(ctx)
    if not user: new_user(ctx.author)
    return True

@bot.event
async def on_member_remove(member):
    dbase.delete_item(member.id, 'user_list')

def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k

async def get_user_roles(ctx):
    global dbase
    member_roles = [role.id for role in bot.get_guild(guild_id).get_member(ctx.message.author.id).roles if role.mentionable]
    await delete_message(ctx)
    return member_roles

async def delete_message(ctx):
    try:
        await ctx.message.delete()
    except:
        print('Ошибка')

@bot.command()
async def info(ctx):
    # global dbase
    # await delete_message(ctx)
    # member_roles = [role.id for role in bot.get_guild(guild_id).get_member(ctx.message.author.id).roles if role.mentionable]
    info_message = ''
    for role in await get_user_roles(ctx):
        match cf_role.get(role):
            case 0:
                await ctx.author.send(f'{ctx.author.mention}, для получения роли первого уровня (доступ к голосовому каналу и дополнительным материалам) отправьте боту команду /access')
            case 1:
                print('Первый')
                # await ctx.author.send(f'{ctx.author.mention}, для получения роли первого уровня (доступ к голосовому каналу и дополнительным материалам) отправьте боту команду /access')
                # await ctx.author.send(f'{ctx.author.mention}, для получения роли первого уровня (доступ к голосовому каналу и дополнительным материалам) отправьте боту команду /access')
            case 2:
                print('Второй')
                pass
            case 3:
                print('Третий')
                pass
            case 4:
                print('Четвертый')
                await ctx.author.send(f'{ctx.author.mention}, у вас статус admin и вы можете:\n\n/embed <Заголовок> <Текст сообщения> - Загловок из одного слова, текст сообщения - сколько угодно\n\n/set_task <пользователь> <номер задачи> - выдать пользователю новую задачу, пользователя можно задать кликнув по нему правой кнопкой и выбрать Упомянуть')

@bot.command()
async def set_task(ctx, stat_name: str, stat):
    global dbase
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        print('Можно')
        dbase.update_item('set_task', stat_name[2:-1], stat)
        await ctx.send(
            f'У пользователя {stat_name} теперь {stat} задача')
    else:
        print('Нельзя')
        await ctx.send(f'Эта команда для вас недоступна')

@bot.command()
async def embed(ctx, title, *args):
    global dbase
    text = ''
    for word in args:
        text += word + ' '
    if await get_user_roles(ctx) == 4:
        embed = discord.Embed(color=0xff9900, title=f'{title}', description=f'{text}')
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'Эта команда для вас недоступна')


@bot.command()
async def access(ctx, *args, **kwargs):
    global dbase, one_level_role
    guild = bot.get_guild(guild_id)
    member = guild.get_member(ctx.message.author.id)
    await check_user(ctx)
    for role in member.roles:
        if one_level_role == role.id:
            await ctx.send(f"У вас уже есть такая роль")
            break
    else:
        cur_user = dbase.get_user('user', ctx.author.id)
        cur_quest = dbase.get_quest('task', cur_user[0][2])
        await ctx.send(f'{ctx.author.mention}, {task_string}{cur_quest[0]}{answer_string}')

@bot.command()
async def answer(ctx, *args, **kwargs):
    global dbase, quest_answers, simple_role
    await check_user(ctx)
    if not args == ():
        guild = bot.get_guild(guild_id)
        role = guild.get_role(cf_role[1])
        member = guild.get_member(ctx.message.author.id)
        task_id = dbase.get_user('task', ctx.author.id)
        if str(args[0]) == str(dbase.get_quest('answer', task_id[0])[0]):
            await delete_message(ctx)
            await member.add_roles(role)
            await ctx.send(f"{ctx.author.mention}, поздравляем! Теперь у тебя роль первого уровня!")
        else:
            await delete_message(ctx)
            await ctx.send(f'{ctx.author.mention}, ну чего-то ты не то написал. Разберись для начала с этим, а потом уже роль')

@bot.command()
async def adduser(ctx, user_id):
    await delete_message(ctx)
    if ctx.author.id == 1004464010189623296 or ctx.author.id == 669628282756530207:
        guild = bot.get_guild(guild_id)
        role = guild.get_role(vpb_role)
        member = guild.get_member(int(user_id[2:-1]))
        await member.add_roles(role)
        await ctx.send(f"Пользователь {user_id}, получил роль {role}!")

async def game_info():
    global status
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game('/info'))
        await asyncio.sleep(15)

bot.loop.create_task(game_info())
bot.run(os.getenv('TOKEN'))