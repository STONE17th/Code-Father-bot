import os
from datetime import datetime
import asyncio
import random
import mysql.connector
import data_base
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# dbase = quests = quests_id = None

admin = 669628282756530207

cf_role = {996841246016417962: -1,
           1010186572156641290: 0,
           1000730137731551382: 1,
           1009910414961811486: 2,
           1009928506966290442: 3,
           1001397006993985646: 4}

vpb_role = 1008289239210938518
guild_id = 996841246016417962
start_channel = 1006321073958166548
adv_channel = 996841247446683752

status = '/info'
task_string = f'что выведет в *консоль* этот код:\n'
answer_string = f'\n\nОтвет отправляй так: **/answer** *<твой вариант ответа>*'

adv_timer = 0
adv_title = 'На правах рекламы'
adv_text = f'Не дадим технологиям захватить мир! Машины должны батрачить на людей, а не наоборот. Вступай в ряды ' \
           f'ботоводов ✊\nКурсы по телеграм-ботоводству на базе библиотеки AIOgram языка Python\nЗа подробностями в ' \
           f'личку '


async def db_connection():
    global dbase
    try:
        dbase = data_base.DataBase(
            mysql.connector.connect(user='root', db='cf_bot', passwd='CodeFather17', host='glt.ekolenko.ru'))
        print('DB Connected... OK!')
        return dbase
    except:
        print('DB Connected... failed')
        await send_message_to_admin("База данных отвалилась")


@bot.event
async def on_ready():
    global quests, quests_id, dbase
    print('On start')
    dbase = await db_connection()
    if dbase:
        print('DB Connected... OK')
        quests = dbase.get_quest('all', '', 0)
        quests_id = dbase.get_quest('id', '', 0)


@bot.event
async def on_member_join(member):
    guild = bot.get_guild(guild_id)
    embed = discord.Embed(title="Добро пожаловать!",
                          description=f'Эй, народ! Нас теперь {guild.member_count} :)\n\nПривет, {member.mention}. Я '
                                      f'бот канала CODE Father\'s. Пока я мало чего умею, '
                                      f'но всё впереди...\n\nЗагляни в ЛС, я там тебе кое-чего прислал',
                          color=0xCC974F)
    await bot.get_channel(start_channel).send(embed=embed)
    await member.send(
        f'Привет, {member.name}! Рады приветствовать тебя на нашем сервере. Чем мы здесь занимаемся?\nМы создаем '
        f'дружное коммьюнити из единомышленников в IT сфере. Здесь ты сможешь получить помощь с ДЗ, '
        f'получить консультацию по текущим темам от однокурсников, пообщаться в прямом эфире с крутыми гостями, '
        f'которые уже работают в IT, обменяться опытом, найти команду для реализации своих идей, да и просто '
        f'пообщаться :)\nЕсли возникнут вопросы, то пиши кому-нибудь из администараторов и тебе обязательно '
        f'ответят\n\nНо для начала было бы неплохо получить роль первого уровня (для доступа к голосовому чату и '
        f'архиву с полезными ссылками)\nДля этого просто введи на канале /access и мы с тобой всё '
        f'сделаем!\n\nПриятных тебе минут на сервере и удачного обучения!\n\nP.S. Если увидишь Джонна Конора - '
        f'передай привет')
    await send_message_to_admin(f'У нас новый участник - {member.name}!')
    await new_user(member)

@bot.command(aliases=['реклама'])
async def adverstiment(ctx, time: int):
    global dbase, adv_timer
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        adv_timer = time
    else:
        await ctx.send(f'Эта команда для тебя недоступна')
    while (adv_timer):
        guild = bot.get_guild(guild_id)
        member = guild.get_member(admin)
        atext = adv_text + f'{member.mention}'
        embed = discord.Embed(title=adv_title,
                              description=atext,
                              color=0x00ff7b)
        await bot.get_channel(adv_channel).send(embed=embed)
        await asyncio.sleep(adv_timer)


@bot.command(aliases=['таймер'])
async def set_adv_timer(ctx, time: int):
    global dbase, adv_timer
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        adv_timer = time
    else:
        await ctx.send(f'Эта команда для тебя недоступна')


@bot.command()
async def tyu0(ctx):
    embed = discord.Embed(title="Манифест сервера CODE Father`s",
                          description="Основная тематика сервера **CODE Fathers's** (далее CF) - IT-технологии, "
                                      "а именно направление '*Разработчик*' (кодинг, тестирование, аналитика, "
                                      "проджект и продукт менеджмент). Если тебе это знакомо - *welcome*.\nСервер "
                                      "создан студентами **GeekBrains** и изначально нацелен на обсуждение процесса "
                                      "обучения и сопутствующих тем, однако *тематика продолжает расширяться*. Свежие "
                                      "идеи по развитию контентной нагрузки *приветствуются*.\nНазвание '**CODE "
                                      "Father's**' результат игры слов от '*GodFather*' (Крестный отец) и никак не "
                                      "претендует на '*отцовство*' в сфере кодинга. На сервере присутствует "
                                      "достаточно много отсылок к тематике '*Крестоного отца*'.\nТак же на сервере "
                                      "присутствует достаточно много '*игровых*' моментов, что привносит интересные "
                                      "механики и разбавляет серые будни. Эти правила придется принять или нам с "
                                      "тобой не по пути.\n\nОбщие правила поведения.\n\n    **1. Основные "
                                      "принципы.**\n    **2. Оформление аккаунта.**\n    **3. Публикации.**\n    **4. "
                                      "Общение в голосовых каналах.**\n    **5. Роли на сервере. Получение первой "
                                      "роли.**\n    **6. Семья.**\n    **7. Бот CODE Father.**\n    **8. Кары, "
                                      "ответственность.**",
                          color=0x8400ff)
    await ctx.send(embed=embed)


@bot.command()
async def tyu1(ctx):
    embed = discord.Embed(title="1. Основные принципы",
                          description="**1.1 Будьте вежливы**. За грубостями и оскорблениями последует кара вплоть до "
                                      "прощания с сервером.\n    **1.2 Мат не воспрещается**, но старайтесь держаться "
                                      "в рамках, не надо '*разговаривать матом*'.\n    **1.3** Старайтесь "
                                      "использовать **общепринятую техническую терминологию** (или общепринятый "
                                      "сленг), ясно и четко излагать суть проблемы.\n    **1.4** При ответе на "
                                      "какой-либо вопрос или высказывание, именно отвечайте, кликнув '*ответить*' на "
                                      "исходном сообщении.\n    **1.5** При ответе на вопрос старайтесь "
                                      "придерживаться тех же правил - техническая терминология, ясность, четкость, "
                                      "суть. Не стоит сразу отправлять вопрошающего в *гугл* (там он, видимо, "
                                      "уже был), а вот ссылка на ресурс с ответом/документацией приветствуется, "
                                      "не стесняйтесь уточнить куда смотреть в первую очередь.\n    **1.6** Задавая "
                                      "вопрос по ошибке интерпретатора приводите **скриншот** (или *листинг*) ошибки "
                                      "и, желательно, соответствующий фрагмент кода (скриншот/листинг).",
                          color=0x00ff7b)
    await ctx.send(embed=embed)


@bot.command()
async def tyu2(ctx):
    embed = discord.Embed(title="2. Оформление аккаунта",
                          description="**2.1.1 Ник-нейм**. Крайне приветствуются реальные имена или же псевдонимы "
                                      "исключающие *двусмысленность*. Недопустимы **шовинистические** или "
                                      "**радикальные** псевдонимы. По-возможности избегайте привязывать ник к "
                                      "*политике* или *религии*.\n    **2.1.2 Служебные символы** - @, #, $, %, ^, &, "
                                      "*, ?, |, /, , а также *эмодзи* и подобное недопустимы в следствие технических "
                                      "ограничений базы данных, вы будете вне базы и покинете сервер.\n    **2.2 "
                                      "Аватар**. Мы всегда будем рады видеть Вашу улыбку в наших рядах, если же Вы "
                                      "желаете ее скрыть - это *Ваш выбор*. **Недопустимы**: порнография, мертвечина "
                                      "и прочее так-называемое гуро.\n    **2.3 Пользовательский статус**. По вкусу. "
                                      "Недопустимы *оскорбления*, *радикальные*, *экстремистские высказывания*.",
                          color=0xb00e6a)
    await ctx.send(embed=embed)


@bot.command()
async def tyu3(ctx):
    embed = discord.Embed(title="3. Публикации",
                          description="**3.1** Публикуемые материал должны соответствовать *основной тематике "
                                      "сервера* - IT.\n    **3.2** Для отвлеченных рассуждений предусмотрена "
                                      "*флудильня*.\n    **3.3** При публикации сторонних материалов, соблюдайте "
                                      "*копирайт авторов*. Проверяйте, разрешил ли атор публикацию на других "
                                      "ресурсах, нежели исходный, обязательно оставляйте **ссылку на оригинал**. В "
                                      "случае бумажного исходника - *автор, название, год издания, страница*.\n    "
                                      "**3.4** **Запрещается** публиковать материалы, представляющие собой "
                                      "*коммерческую тайну*!\n    **3.5** Публикация материалов, являющихся чьей-либо "
                                      "*интеллектуальной собственностью* допустима с **только согласия атора** ("
                                      "*владельца*) с явным указанием данного согласия.\n    **3.6** Публикация "
                                      "материалов находящихся в открытом (*бесплатном*) доступе (документы pdf, doc, "
                                      "txt, электронные/сканированные книги, статьи) допускается только в виде "
                                      "**ссылки на исходный ресурс**.\n    **3.7** **Запрещается** публикация "
                                      "*экстремистских* и *радикальных* материлов! За нарушения будет вынесен "
                                      "**БАН**.\n    **3.8** Публикация *политических/религиозных* материалов, "
                                      "а также *обсуждения* на данные темы **ЗАПРЕЩАЮТСЯ** в с связи со "
                                      "складывающейся ситацией в стране. *Данная тематика не соответствует тематике "
                                      "данного сервера*. За нарушения будет вынесен **БАН**.",
                          color=0xfff200)
    await ctx.send(embed=embed)


@bot.command()
async def tyu4(ctx):
    embed = discord.Embed(title="4. Общение в голосовых каналах. Подкасты",
                          description="**4.1** На мероприятиях присутствуют *докладчик* и *ведущий*. Вопросы "
                                      "докладчику задаются *письменно* через ведущего. В конце мероприятия допустима "
                                      "*открытая голосовая сессия* вопросов к докладчику.\n    **4.2** **Недопустимы "
                                      "оскорбления** в адрес *докладчиков* и *участников* на голосовых "
                                      "мероприятиях.\n    **4.3** Общение в голосовых каналах свободное в отсутствие "
                                      "плановых мероприятий в рамках обозначенной *тематики канала*. **Будьте взаимно "
                                      "вежливы**.",
                          color=0x00ffee)
    await ctx.send(embed=embed)


@bot.command()
async def tyu5(ctx):
    embed = discord.Embed(title="5. Роли сервера",
                          description="**5.1** На сервере предусмотрена иерархия *ролей* с различным *уровнем "
                                      "доступа* текстовым и голосовым каналам сервера **CF**.\n    **5.2** Каждый "
                                      "новый участник сервера *не имеет никакой роли* и имеет минимальный доступ ("
                                      "*общеинформационные каналы, флудильня и общий голосовой канал*). Участник в "
                                      "**течение трех дней** (с момента вступления на сервер) не получивший роли - "
                                      "**удаляется с сервера**.\n    **5.3 Серая роль - 'NPC'**. Получается "
                                      "*автоматически* после принятия данного манифеста. Для принятия - в любом "
                                      "голосовом чате (в том числе и в личных сообщениях с ботом CF) надо отправить "
                                      "команду **/access**\n    **5.4 Зеленая роль - 'NewCoder'**. Дает доступ к "
                                      "*полезным голосовым и текстовым каналам* сервера CF. Выдается ботом CF.\n    "
                                      "**5.5 Синяя роль - 'CapoCoder'**. Обладает *расширенным функционалом* и "
                                      "выдается участникам которые хотят создать '*семью*' (подробнее о 'семьях' "
                                      "можно прочитать в 6 пункте). Заявку на создание 'семьи' можно подать через "
                                      "*бота*.\n    **5.6 Фиолетовая роль - 'UnderCode'**. Выдается *крайне полезным* "
                                      "людям, которые активно участвуют в жизни сервера и помогают остальным жителям. "
                                      "Выдается админами или при достижении *CF-рейтинга 100*.\n    **5.7 Оранжевая "
                                      "роль - 'CODE Father'**. Макисмальная (почти :)) по функционалу и значимости "
                                      "роль на сервере CF. К обладателям этой роли *всегда можно обратиться за "
                                      "помощью* или с вопросом/предложением относительно сервера. Выдается "
                                      "**исключительно админами**, является повышением от роли '*UnderCode*'",
                          color=0xff8c00)
    await ctx.send(embed=embed)


@bot.command()
async def tyu6(ctx):
    embed = discord.Embed(title="6. Семья",
                          description="**6.1** '**Семья**' - команда *единомышленников* трудящихся над одним "
                                      "проектом.\n    **6.2** Семье выдается *именной скрытый голосовые чат* (чтоб "
                                      "никто не мешал), доступ к эти каналам имеют только члены семьи.\n    **6.3** В "
                                      "семью может принять (выдать роль) *глава семьи* путем команды **CF боту**.\n   "
                                      " **6.4** Объединение в семьи **крайне приветствуется** на просторах **сервера "
                                      "CF**.",
                          color=0x0400ff)
    await ctx.send(embed=embed)


@bot.command()
async def tyu8(ctx):
    embed = discord.Embed(title="7. Бот 'CODE Father'",
                          description="**7.1** На сервере **24/7** несет свою службу **Code Father бот**, написанный "
                                      "админами сервера для автоматизации процессов.\n    **7.2** *Предложения по "
                                      "расширению функционала бота* - направлйте в личку **админам**. Это очень "
                                      "приветствуется.\n    **7.3** Более подробную информацию можно получить по "
                                      "команде **/info**",
                          color=0xff00fb)
    await ctx.send(embed=embed)


@bot.command()
async def tyu9(ctx):
    embed = discord.Embed(title="8. Кары, ответственность",
                          description="**8.1** На сервере предусмотренно *2 вида* пресечения свободы действий:\n    "
                                      "**8.2.1 Бан на общение**. Длительность бана зависит от тяжести "
                                      "'*преступления*'.\n    **8.2.2 Удаление с сервера** и занесение *ID в черный "
                                      "список*.\n    **8.3** После получения **8.2.1** рейтинг участника *обнуляется* "
                                      "и роль сбрасывается до *первого уровня*.\n    **8.4** После *трехкратного* "
                                      "получения **8.2.1** участник получает **8.2.2**",
                          color=0xff0000)
    await ctx.send(embed=embed)


async def new_user(member):
    global quests_id
    date = datetime.now()
    user = ((member.id, member.name, 0, 10, 0, date))
    dbase = await db_connection()
    dbase.add_item('new_user', user)


async def check_user(ctx):
    global dbase
    user = dbase.get_user('user', ctx.author.id)
    await delete_message(ctx)
    if not user: await new_user(ctx.author)
    return True


async def check_member(member):
    global dbase
    try:
        user = dbase.get_user('user', member.id)
        if not user: await new_user(member)
    except:
        await member.send(
            f'{member.mention}, твой никнейм содержит недопустимые символы. Измени никнейм, иначе мы не сможем внести '
            f'тебя в БД')
    return True


@bot.event
async def on_member_remove(member):
    global dbase
    dbase.delete_item(member.id, 'user_list')
    await send_message_to_admin(f'Нас покинул {member.name}!')


def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k


async def send_message_to_admin(text):
    guild = bot.get_guild(guild_id)
    member = guild.get_member(admin)
    await member.send(text)


async def get_user_roles(ctx):
    member_roles = [role.id for role in bot.get_guild(guild_id).get_member(ctx.message.author.id).roles]
    await delete_message(ctx)
    return member_roles


async def remove_role(member, role):
    await member.remove_roles(role)


async def delete_message(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command()
async def mailing(ctx, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        users = dbase.get_user('user_id', "*")
        text = ''
        for word in args:
            text += f'{word} '
        for user in users:
            guild = bot.get_guild(guild_id)
            member = guild.get_member(int(user[0]))
            await member.send(text)
    else:
        await ctx.send(f'Эта команда для тебя недоступна')




@bot.command()
async def info(ctx):
    global dbase
    await check_user(ctx)
    user_date = dbase.get_user('date', ctx.author.id)
    guild = bot.get_guild(guild_id)
    roles = []
    [roles.append(guild.get_role(x).name) for x in await get_user_roles(ctx)]
    txt_role = ''
    txt_txt_channels = 'Текстовые каналы **Прихожая**, **Манифест**, **Важная информация**, **Флудильня**'
    txt_voice_channels = 'Голосовые каналы **Переговорная**'
    txt_advanced = ''
    txt_commands = '**/info** - помощь по боту канала CODE Father\'s\n'
    for role in roles:
        txt_role += f'{role}, '
    for role in await get_user_roles(ctx):
        match cf_role.get(role):
            case -1:
                txt_commands += '**/access** - для принятия правил(манифеста) сервера и получения серой роли\n'
            case 0:
                txt_commands += '**/task** *<выбор языка>* - для получения зеленой роли путем решения задачи на выбранном языке\n'
                txt_commands += '**/answer** *<твой ответ>* - для отправки ответа на полученную задачу *(**Важно!** Ответы False и false - разные вещи. Вводи именно так, как требует задача.)*\n'
            case 1:
                txt_txt_channels += ', **Полезные ссылки**, **Документация**, **Podcasts**, **Вопросы для гостя**'
                txt_voice_channels += ', **Кабинеты языков**, **Podcast**'
                pass
            case 2:
                txt_advanced += 'Создавать свою **Семью** и получаешь доступ к текстовому и голосовму каналу своей семьи '
            case 3:
                print('Третий')
                pass
            case 4:
                txt_txt_channels += ', **Штаб**'
                txt_voice_channels += ', **Штаб**'
                txt_advanced += ', выдавать и снимать роли, участвовать в совещании штаба CF '
                txt_commands += '**/embed** *<Цвет> <Заголовок> <Текст сообщения>* - цвет в HEX формате, если в заголовке больше одного слова, то обязательно в двойных кавычках, текст сообщения - сколько угодно\n'
                txt_commands += '**/poll** *<Цвет> <Вопрос> <Варианты ответов>* - цвет в HEX формате, если в вопросе больше одного слова, то обязательно в двойных кавычках, варианты ответов одним словом\n'
                txt_commands += '**/set_task** *<пользователь> <номер задачи>* - выдать пользователю новую задачу, пользователя можно задать кликнув по нему правой кнопкой и выбрать *Упомянуть*'
    await ctx.author.send(
        f'{(ctx.author.mention)}, на сервере CODE Father\'s ты провел {str(datetime.now() - user_date[0])[:-7]}\nУ тебя есть роли:\n{txt_role[:-2]}.\n\n**Тебе доступно:**\n{txt_txt_channels}\n{txt_voice_channels}\n{txt_advanced}\n\n**И ты можешь использовать следующие команды бота:**\n{txt_commands}')


@bot.command()
async def set_task(ctx, stat_name: str, stat):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        dbase.update_item('set_task', stat_name[2:-1], stat)
        await ctx.send(
            f'У пользователя {stat_name} теперь {stat} задача')
    else:
        await ctx.send(f'Эта команда для тебя недоступна')


@bot.command()
async def family(ctx, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        dbase.update_item('set_family', args[0][2:-1], args[1])
        guild = bot.get_guild(guild_id)
        role = guild.get_role(int(args[1]))
        role2 = guild.get_role(int(get_key(cf_role, 4)))
        member = guild.get_member(int(str(args[0])[2:-1]))
        await member.add_roles(role)
        await member.add_roles(role2)
        await ctx.send(
            f'Поздравляю, {member}! Теперь ты глава семьи {role}!')
    elif int(dbase.get_user('family', ctx.author.id)[0]) in await get_user_roles(ctx):
        guild = bot.get_guild(guild_id)
        role = guild.get_role(int(dbase.get_user('family', ctx.author.id)[0]))
        member = guild.get_member(int(str(args[0])[2:-1]))
        await member.add_roles(role)
        await ctx.send(
            f'Поздравляю, {member}! Теперь ты в семье {role}!')
    else:
        await ctx.send(f'Эта команда для тебя недоступна')


@bot.command()
async def embed(ctx, color, title, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        text = ''
        for word in args:
            text += f'{word} '
        await check_user(ctx)
        col = int(str(color).replace('#', ''), 16)
        embed = discord.Embed(color=col, title=title, description=f'{text}')
        await ctx.send(embed=embed)
        await delete_message(ctx)
    else:
        await ctx.send(f"У тебя нет доступа к этой команде")


@bot.command(aliases=["голосование", "голос"])
async def poll(ctx, color, question, *args):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        numbers = []
        [numbers.append(f'{i}\uFE0F\u20E3') for i in range(1, 11)]
        if len(args) <= 10:
            col = int(str(color).replace('#', ''), 16)
            embed = discord.Embed(title="Голосование", description=question, color=col)
            fields = [("Варианты:", "\n".join([f'{numbers[idx]} - {option}' for idx, option in enumerate(args)]), True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            message = await ctx.send(embed=embed)
            for emoji in numbers[:len(args)]:
                await message.add_reaction(emoji)
        await delete_message(ctx)
    else:
        await ctx.send(f"У тебя нет доступа к этой команде")


@bot.command()
async def add_all_user_to_db(ctx, *args, **kwargs):
    guild = bot.get_guild(guild_id)
    members = guild.members
    for each in members:
        await check_member(each)


@bot.command()
async def clear_all_users_role(ctx, *args, **kwargs):
    global dbase
    await delete_message(ctx)
    if get_key(cf_role, 4) in await get_user_roles(ctx):
        guild = bot.get_guild(guild_id)
        role = guild.get_role(get_key(cf_role, int(args[0])))
        members = guild.members
        for each in members:
            if role in each.roles:
                await each.remove_roles(role)
    else:
        await ctx.send(f'{ctx.author.mention}, у тебя нет прав для использования этой команды')


@bot.command()
async def access(ctx, *args, **kwargs):
    global dbase
    await check_user(ctx)
    if get_key(cf_role, 0) in await get_user_roles(ctx):
        await ctx.send(
            f'{ctx.author.mention}, ты уже принял правила сервера. Для помощи по командам бота используй **/info**')
    else:
        guild = bot.get_guild(guild_id)
        npc_role = guild.get_role(get_key(cf_role, 0))
        member = guild.get_member(ctx.message.author.id)
        await member.add_roles(npc_role)
        await ctx.send(
            f'{ctx.author.mention}, поздравляем! Теперь у тебя роль первого уровня! Командой **/info** можешь узнать свои новые возможности')


@bot.command()
async def task(ctx, *args, **kwargs):
    global dbase
    dbase = await db_connection()
    await check_user(ctx)
    if args == ():
        user_task = dbase.get_user('task', ctx.author.id)
        if not user_task[0] == str(0):
            user_quest = dbase.get_quest('task', user_task[0][0], int(user_task[0][1]))
            await ctx.send(f'{ctx.author.mention}, {task_string}{user_quest[0]}{answer_string}')
        else:
            await ctx.send(
                f'{ctx.author.mention}, для начала тебе нужно взять задачу при помощи команды **/task** *<язык>*, языки p - Python, j - Java, c - C#')
    else:
        if get_key(cf_role, 1) in await get_user_roles(ctx):
            await ctx.send(
                f'{ctx.author.mention}, у тебя уже есть роль первого уровня. Для помощи по командам бота используй **/info**')
        elif args[0] not in ('p', 'j', 'c'):
            await ctx.send(f'{ctx.author.mention}, введи язык корректно.  p - Python, j - Java, c - C#')
        else:
            letter = args[0]
            number = random.choice([1, 2, 3, 4, 5])
            dbase.update_item('set_task', ctx.author.id, str(letter) + str(number))
            user_quest = dbase.get_quest('task', letter, int(number))
            await ctx.send(f'{ctx.author.mention}, {task_string}{user_quest[0]}{answer_string}')


@bot.command()
async def answer(ctx, *args, **kwargs):
    global dbase, quest_answers
    dbase = await db_connection()
    await check_user(ctx)
    if not args == ():
        guild = bot.get_guild(guild_id)
        new_role = guild.get_role(get_key(cf_role, 1))
        old_role = guild.get_role(get_key(cf_role, 0))
        member = guild.get_member(ctx.message.author.id)
        task = dbase.get_user('task', ctx.author.id)
        if str(args[0]) == str(dbase.get_quest('answer', task[0][0], task[0][1])[0]):
            await delete_message(ctx)
            await member.add_roles(new_role)
            await ctx.send(
                f"{ctx.author.mention}, поздравляем! Теперь у тебя роль первого уровня! Командой **/info** можете узнать свои новые возможности")
            await remove_role(member, old_role)
        else:
            await delete_message(ctx)
            await ctx.send(
                f'{ctx.author.mention}, ну чего-то ты не то написал. Разберись для начала с этим, а потом уже роль')


async def game_info():
    global status
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Game('/info'))
        await asyncio.sleep(15)


# bot.loop.create_task(game_info())
bot.run('MTAxMDY5NTY1NTIyNTgxOTE3Ng.GITVkS.owkrA4OPIk8OkI5Bw_oU0w4o1qn-ly6Z0qdt4Q')
