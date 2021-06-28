''' Основной файл в который будем импортировать sql'''

import discord, os, time
from discord.ext import commands
from discord.utils import get
from SQLite import WWDB
import random
import sqlite3


class Base(commands.Cog):
    helpEmb = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
    helpEmb.set_author(name='Список команд',
                       icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
    helpEmb.add_field(name='Обычные команды',
                      value="`hello`")
    helpEmb.add_field(name="Комманды для игры",
                      value="`crip_battle`, `inventory`, `location`, `players_list`, `profile`, `register`, `rest`")

    def __init__(self, bot):  # Иницилизация для работы регистра
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.message.author.mention}!')

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=self.helpEmb)


class Game(commands.Cog, WWDB):

    loc_channel = {744484105852551239: 0, 'таверна': 0,
                        744948183242637374: 1, 'лес': 1,
                        744483452203696160: 2, 'болото': 2,
                        744947492923244615: 3, 'могильник': 3,
                        744947400489173152: 4, 'цитадель': 4,
                        744948528018620547: 5, 'лабиринт': 5,
                        744947464448114798: 6, 'зиккурат': 6,
                        753268164833443841: -1}  # канал регистрации

    regEmb = discord.Embed(title='Великая GameName', colour=discord.Colour.from_rgb(150, 206, 214))
    regEmb.set_author(name="Злой ГМ",
                           icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
    regEmb.add_field(name='Приветствую тебя, дорогой искатель приключений!',
                          value="Ты попал в ванильный фэнтезийный бред. Заставим Рому это писать.",
                          inline=False)
    regEmb.add_field(name="Комманды для игры",
                          value="`crip_battle`, `inventory`, `location`, `players_list`, `profile`, `register`, `rest`")

    def __init__(self, bot):  # Иницилизация для работы регистра
        self.conn = sqlite3.connect('sql.sqlite')
        self.curs = self.conn.cursor()

        self.bot = bot
        self.location = [i[1] for i in self.read_db('*', 'locations')]

    def check_battle_channel():  # функция для декоратора проверки канала боевых лок
        def predicate(ctx):
            return ctx.guild is not None and Game.loc_channel[ctx.channel.id] in [1, 2, 3, 4, 5, 6]

        return commands.check(predicate)

    def check_on_rest():  # функция для декоратора проверки спит персонаж или нет
        def predicate(ctx):
            member = ctx.message.author
            sleepRole = get(ctx.guild.roles, name='сон')
            return ctx.guild is not None and sleepRole not in member.roles

        return commands.check(predicate)

    def check_reg_channel():  # функция для декоратора проверки канала регистрации
        def predicate(ctx):
            return ctx.guild is not None and Game.loc_channel[ctx.channel.id] == -1

        return commands.check(predicate)

    def check_tav_channel():  # функция для декоратора проверки канала тавнерны
        def predicate(ctx):
            return ctx.guild is not None and Game.loc_channel[ctx.channel.id] == 0

        return commands.check(predicate)

    class Character(WWDB):
        def __init__(self, lvl, hp, weapon, armor):
            WWDB.__init__(self)

            self.lvl = lvl
            self.hp = hp
            self.damage = self.read_db('damage', f'weapons where id = {weapon}')[0]
            self.protection = self.read_db('protection', f'armor where id = {armor}')[0]

        def remove_hp(self, damage):
            res_hp = self.hp - damage * (1 - self.protection * 0.1)
            if res_hp < 0:
                self.hp = 0
            else:
                self.hp = round(res_hp, 2)

        def move_damage(self):
            return round(random.uniform(0.7, 1.3) * self.damage, 2)

        def get_loot(self, id):
            category = ['armor', 'weapons']  # список категорий выпадаемого лута
            rareChance = [10, 3, 1]  # редкость предметов
            now_category = random.choice(category)  # выбор категории
            things = self.read_db('*', f'{now_category} where LVL = {self.lvl}')  # выбор предметов необходимого уровня
            reward = random.choices(things, rareChance, k=1)  # выбор награды по редкости

            newInventory = f"{self.read_db(f'inventory_{now_category}', f'person where id = {id}')[0]}, {reward[0][0]}"
            self.update_db('person', f'inventory_{now_category}', newInventory, f'id = {id}')  # обновление инвентаря

            newXP = int(self.read_db(f'XP', f'person where id = {id}')[0]) + self.lvl * 5
            self.update_db('person', f'XP', newXP, f'id = {id}')  # обновление опыта

            if newXP > self.lvl * (self.lvl + 1) / 2 * 100:  # треугольные числа для подсчётна и обновления уровня
                self.update_db('person', f'LVL', self.lvl + 1, f'id = {id}')
            return f'Вы выбили {reward[0][1]} и {self.lvl * 5} опыта. Для дополнительной информации загляните в инвентарь!'

    class Crip(WWDB):
        def __init__(self, lvl, hp, damage, protection=0.1):
            WWDB.__init__(self)

            self.lvl = lvl
            self.hp = hp
            self.damage = damage
            self.protection = protection
            self.description = self.read_db('description', f'mobs where id = {lvl}')

        def remove_hp(self, damage):
            res_hp = self.hp - damage*(1 - self.protection * 0.1)
            if res_hp < 0:
                self.hp = 0
            else:
                self.hp = round(res_hp, 2)

        def move_damage(self):
            return round(random.uniform(0.7, 1.3) * self.damage, 2)

    @commands.command()
    @check_on_rest()
    @commands.check_any(check_battle_channel())
    async def crip_battle(self, ctx):  # НЕ ставить в таблице armor protection - "1"! Максимум - "0.25",  и то только для лучшей брони !
        try:
            count = 1

            display_battle = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
            display_battle.set_author(name="Злой ГМ", icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')

            data = self.read_db('*', f'person where id = {ctx.message.author.id}')

            character = self.Character(data[0][3], data[0][2], data[0][7], data[0][8])
            crip = self.Crip(data[0][3] - 1, data[0][2]/2, 1)

            if character.hp < 0:
                await ctx.send('Вы мерты, отдохните в таверне!')
            else:

                display_battle.add_field(
                    name=f'Характеристики преред игрой:',
                    value=f"Твоё хп: `{character.hp}`\nХп крипа: `{crip.hp}`",
                    inline=False)

                while True:
                    crip_damage = crip.move_damage()
                    character_damage = character.move_damage()

                    character.remove_hp(crip_damage)
                    crip.remove_hp(character_damage)

                    display_battle.add_field(
                        name=f'Итог {count} хода:',
                        value=f"Твоё хп: `{character.hp}`:drop_of_blood:\nХп крипа: `{crip.hp}`:drop_of_blood:",
                        inline=False)

                    if crip.hp <= 0:
                        display_battle.add_field(
                            name=f'Ты выиграл! \n {crip.description}',
                            value=f"Твоё хп оставшеесе хп: `{character.hp}`\n"
                                  f"{character.get_loot(data[0][0])}",  # сообщение о выпавшем луте
                            inline=False,
                        )
                        break
                    elif character.hp <= 0:
                        display_battle.add_field(
                            name=f'Ты проиграл и остался в этой локации, как призрак. Отнеси своё тело в таверну и отдохни',
                            value=f" Оставшеесе хп крипа: `{crip.hp}`",
                            inline=False)
                        break

                    count += 1

                self.update_db('person', 'HP', round(character.hp, 2),
                               f'id={ctx.message.author.id}')  # обновление HP после битвы
                await ctx.send(embed=display_battle)

        except Exception as err:
            print(err)

    @commands.command()
    @commands.check_any(check_reg_channel(), check_tav_channel(), check_battle_channel())
    async def inventory(self, ctx, *args):
        if not args:
            await ctx.send(f'Для изменения и просмотра инвентаря выберете вкладку:\n '
                           f'1.weapons\n'
                           f'2.armor')

        valid_types = ('weapons', '1', 'armor', '2')
        def check_type(m): # функция для проверки необходимого сообщения в wait_for
            return m.channel == ctx.message.channel and m.author == ctx.message.author and m.content in valid_types

        types = {
            'weapons': 'weapons',
            '1': 'weapons',
            'armor': 'armor',
            '2': 'armor'
        }

        # отлов необходимого сообщения и задание вкладки инвентаря
        type_message = await self.bot.wait_for('message', check = check_type, timeout = 30)
        type = type_message.content

        # создание вкладки инвентаря
        inventory_temp = self.read_db(f'inventory_{types[type]}', f'person where id = {ctx.message.author.id}')[0].split(', ')
        inventory_volume = len(inventory_temp)
        inventory_string = ''

        if types[type] in 'weapons':
            for i in range(inventory_volume):  # создание инвентаря для отображения юзеру
                weapon_data = self.read_db('*', f'weapons where id = {inventory_temp[i]}')[0]
                inventory_string += f'\n {i + 1}. {weapon_data[1]}: урон - {weapon_data[3]}'
                equipped_type = 'in_hand'
        elif types[type] == 'armor':
            for i in range(inventory_volume):  # создание инвентаря для отображения юзеру
                armor_data = self.read_db('*', f'armor where id = {inventory_temp[i]}')[0]
                inventory_string += f'\n {i + 1}. {armor_data[1]}: защита - {armor_data[4]}'
                equipped_type = 'on_body'

        equipped_id = self.read_db(equipped_type, f'person where id = {ctx.message.author.id}')[0]
        equipped = self.read_db('name', f'{types[type]} where id = {equipped_id}')[0]

        await ctx.send(f'Ваше снаряжение {inventory_string}\n Для переэкипировки выберете необходимый пункт')

        # ----------Переэкипировка объекта----------
        def check_obj(m): # функция для проверки необходимого сообщения с номером объекта
            return m.channel == ctx.message.channel and m.author == ctx.message.author and 0 < int(m.content) <= inventory_volume

        # отлов сообщения с номером вещи из инвентаря
        obj_message = await self.bot.wait_for('message', check=check_obj, timeout=30)
        obj_num = int(obj_message.content)

        # смена экипированной вещи вещи
        new_equipped = int(inventory_temp[obj_num - 1])
        new_equipped_name = self.read_db('name', f'{types[type]} where id = {new_equipped}')[0]
        self.update_db('person', equipped_type, new_equipped, f'id={ctx.message.author.id}')
        await ctx.send(f'Вместо {equipped} теперь экипирован {new_equipped_name}')

    @commands.command()
    @check_on_rest()
    @commands.check_any(check_tav_channel(), check_battle_channel())
    async def location(self, ctx, *args):
        try:
            member = ctx.message.author
            allLocations = ''
            for i in range(len(self.location)):
                allLocations += f'\n {i + 1}.' + self.location[i]
            nowRole = get(member.guild.roles,
                          name=self.read_db('curent_loc', f'person where id = {ctx.message.author.id}')[0])

            if not args:
                await ctx.send(f'Ваша локация - {nowRole}.\nНо вы можете переместиться в: {allLocations}')
            elif args[0] in self.location:
                needRole = get(member.guild.roles, name=args[0])
                self.update_db('person', 'curent_loc', f'{args[0]}', f'id={ctx.message.author.id}')
                await member.remove_roles(nowRole)  # удаление настоящей роли
                await member.add_roles(needRole)  # добавление новой роли
                await ctx.send(f'Локация изменина на {args[0]}')
            else:
                await ctx.send(f'Нет такой локации, список доступных локаций:{allLocations}')
        except Exception as err:
            print(err)

    @commands.command()
    @commands.check_any(check_reg_channel(), check_tav_channel(), check_battle_channel())
    async def players_list(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        data = self.read_db('*', 'person')
        playersList = ''
        j = 1
        for i in range(len(data)):  # создание списков людей в локациях
            if self.loc_channel[ctx.channel.id] in [0, 1, 2, 3, 4, 5, 6] and self.loc_channel[data[i][4]] == self.loc_channel[ctx.channel.id]:
                playersList += f'{j}. {data[i][1]}, {data[i][3]}LVL.\n'
            elif self.loc_channel[ctx.channel.id] == -1:  # общий канал
                playersList += f'{j}. {data[i][1]}\n'
            else:
                pass
            j += 1
        await ctx.send(
            'OK, {0}. Вот все путешественники в данной локации:\n{1}'.format(ctx.message.author.mention, playersList))

    @commands.command()
    @commands.check_any(check_reg_channel(), check_tav_channel(), check_battle_channel())
    async def profile(self, ctx):
        try:
            data = self.read_db('*', f'person where id = {ctx.message.author.id}')[0]

            person_profile = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
            person_profile.set_author(name=f"{ctx.message.author.name}", icon_url=f'{ctx.message.author.avatar_url}')
            person_profile.add_field(
                name=f'Текущии характеристики:\nHP:  `{data[2]}` \nLVL:  `{data[3]}`\nТекущая локация: `{data[4]}`  ',
                # не забыть дописать!!!!
                value="Какую-нибудь писанину сюда добавте, ото оно без значения не работает",
                inline=False)

            await ctx.send(embed=person_profile)
        except Exception as err:
            print(err)

    @commands.command()
    @commands.check_any(check_reg_channel())
    async def register(self, ctx):  # Регистрация пользователей
        try:
            member = ctx.message.author
            mainRole = get(member.guild.roles, name="игрок")
            role = get(member.guild.roles, name="таверна")  # получаем нужную роль

            if self.check_db('person',
                             f'id = {ctx.message.author.id}') == False:  # проверка существует ли у этот пользователь в базе данных
                await ctx.send(f'{member.mention} - ты уже зарегистрирован!')

            else:
                self.enter_db(
                    'person(id,name,HP,LVL,curent_loc,inventory_weapons,inventory_armor,in_hand,on_body,XP,on_rest)',
                    (int(member.id), member.name, 10, 1, 'таверна', '1', '1', 1, 1, 0,
                     0))  # добавление нового игрока в БД
                print(f'Роль {role} добавленна юзеру {member}!')
                await member.add_roles(mainRole)  # выдача роли "игрок"
                await member.add_roles(role)  # выдача роли начальной локации
                await member.create_dm()  # личные сообщение с пользователем
                await member.dm_channel.send(embed=self.regEmb)
                await ctx.send(f'{member.mention} - тебя зарегистрировали!')
        except Exception as err:
            print(err)

    @commands.command()
    @commands.check_any(check_tav_channel())
    async def rest(self, ctx):
        member = ctx.message.author

        sleepRole = get(member.guild.roles, name="сон")

        data = self.read_db('*', f'person where id = {ctx.message.author.id}')[0]
        player_HP = data[2]
        player_LVL = data[3]

        maxHP = player_LVL * 10

        on_rest = data[10]

        if on_rest == 0:  # первое использование команды - лечь спать
            self.update_db('person', 'on_rest', time.time(), f'id={ctx.message.author.id}')
            await member.add_roles(sleepRole)
            await ctx.send(
                f'Вы легли на отдых в таверне! Отдых полностью залечит раны через {round(maxHP - player_HP)} секунд. Не забудьте сдать ключи перед битвой!')
        else:  # второе использование команды - выйти из режима лечения
            regeneratedHP = time.time() - on_rest + player_HP  # отхиленное HP
            if regeneratedHP > maxHP:  # если реген больше максимального HP
                regeneratedHP = maxHP
            self.update_db('person', 'HP', round(regeneratedHP, 2), f'id={ctx.message.author.id}')  # обновление HP
            self.update_db('person', 'on_rest', 0,
                           f'id={ctx.message.author.id}')  # обнуление on_rest для повторного использования команды
            await ctx.send(f'Вы хорошо поспали, теперь ваши хп равны {round(regeneratedHP, 2)}! Удачи в новом бою!')
            await member.remove_roles(sleepRole)


def main():
    TOKEN = os.environ.get('TOKEN_FOR_BOT')
    bot = commands.Bot(command_prefix='t! ')
    bot.remove_command(name='help')

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):  # отлов ошибки несуществубщей команды
            await ctx.send(embed=discord.Embed(
                description=f'**{ctx.author.name}**, данной команды не существует. Пожалуйста воспользуйтесь команндой **help** для полного списка команд.',
                color=discord.Colour.from_rgb(191, 56, 74)))
        if isinstance(error, commands.CheckFailure):  # отлов ошибки проверки
            await ctx.send(embed=discord.Embed(
                description=f'**{ctx.author.name}**, вы используете команду не в том канале. Пожалуйста воспользуйтесь команндой **help** для определения необходимой категории.',
                color=discord.Colour.from_rgb(191, 56, 74)))

    bot.add_cog(Base(bot))
    bot.add_cog(Game(bot))

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
