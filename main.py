import sqlite3
from random import randint
import discord
from discord.ext import commands
import os
import data_base

bot = commands.Bot(command_prefix='!', Intents=discord.Intents.all)
bot.remove_command('help')
user = data_base.DataBase('disbot.db')
simple_role = 'GeekBrains'

quest = {
    1: 'a = "Python"\nb = "Love"\nres = (a + b) * 2\nprint(res)\n\n перед ответом напишите команду !answer',
    2: 'a = 5 // 2\nb = 5 % 2\nprint(a > b)\n\n перед ответом напишите команду !answer',
    3: 'что будет выведено в консоль в результате кода:\na = 1\nb = a + 4\na = b\nprint(a+b)\n\n перед ответом напишите команду !answer'

}
quest_answers={
    1: 'PythonLovePythonLove',
    2: 'True',
    3: '10'
}


@bot.event
async def on_ready():
    print('On start')

    global base, cur
    base = sqlite3.connect('disbot.db')
    cur = base.cursor()
    if base: print('DB connected')


@bot.command()
async def help(ctx):
    await ctx.send(f'{ctx.author.mention}, для получения роли GeekBrains (доступ к голосовому каналу и дополнительным материалам) отправьте боту команду !access')

@bot.command()
async def access(ctx, *args):
    global user, quest
    if user.get_data(ctx.author.id) and not user.get_data(ctx.author.id)[0][2] == 0:
        cur_user = user.get_data(ctx.author.id)
        task = cur_user[0][2]
        await ctx.send(f"{ctx.author.mention}, {quest.get(task)}")
    else:
        new_user = ((ctx.author.id, ctx.author.name, 0))
        user.add_item(new_user)
        task = randint(1,len(quest))
        await ctx.send(f"{ctx.author.mention}, {quest.get(task)}")
        user.update_item(task, ctx.author.id)

@bot.command()
async def answer(ctx, *args):
    global user, quest_answers, simple_role
    if not args == ():
        role = discord.utils.get(ctx.author.guild.roles, name=simple_role)
        if args[0] == quest_answers.get(user.get_data(ctx.author.id)[0][2]):
            await ctx.message.delete()
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention}, роль выдана!")
        else:
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.mention}, ну чего-то ты не то написал. Разберись для начала с этим, а потом уже роль")

bot.run(os.getenv('TOKEN'))

