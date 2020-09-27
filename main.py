''' Основной файл в который будем импортировать sql'''

import discord, os, time
from discord.ext import commands
from discord.utils import get
import variables
from variables import *
from SQLite import WWDB
import random
import sqlite3


class Base(commands.Cog):
    def __init__(self, bot):  # Иницилизация для работы регистра
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.message.author.mention}!')

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=helpEmb)


class Game(commands.Cog, WWDB):
    def __init__(self, bot):  # Иницилизация для работы регистра
        self.conn = sqlite3.connect('sql.sqlite')
        self.curs = self.conn.cursor()
        self.bot = bot
        self.location = [i[1] for i in self.read_db('*', 'locations')]

    def check_battle_channel():  # функция для декоратора проверки канала боевых лок
        def predicate(ctx):
            return ctx.guild is not None and loc_channel(ctx.channel.id) in [1, 2, 3, 4, 5, 6]

        return commands.check(predicate)

    def check_on_rest():  # функция для декоратора проверки спит персонаж или нет
        def predicate(ctx):
            member = ctx.message.author
            sleepRole = get(ctx.guild.roles, name='сон')
            return ctx.guild is not None and sleepRole not in member.roles

        return commands.check(predicate)

    def check_reg_channel():  # функция для декоратора проверки канала регистрации
        def predicate(ctx):
            return ctx.guild is not None and ctx.channel.id == 753268164833443841

        return commands.check(predicate)

    def check_tav_channel():  # функция для декоратора проверки канала тавнерны
        def predicate(ctx):
            return ctx.guild is not None and loc_channel(ctx.channel.id) == 0

        return commands.check(predicate)

    @commands.command()
    @check_on_rest()
    @commands.check_any(check_battle_channel())
    async def crip_battle(self,
                          ctx):  # НЕ ставить в таблице armor protection - "1"! Максимум - "0.25",  и то только для лучшей брони !
        try:
            count = 1
            display_battle = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
            display_battle.set_author(name="Злой ГМ", icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')

            data = self.read_db('*', f'person where id = {ctx.message.author.id}')

            person_LVL = data[0][3]
            person_HP = data[0][2]
            crip_LVL = person_LVL - 1

            person_weapon = data[0][7]
            damage = self.read_db('damage', f'weapons where id = {person_weapon}')[0]

            person_armor = data[0][8]
            protection = self.read_db('protection', f'armor where id = {person_armor}')[0]

            description = self.read_db('description', f'mobs where id = {crip_LVL + 1}')[0]
            if person_HP < 0:
                await ctx.send('Вы мерты, отдохните в таверне!')
            else:
                if crip_LVL == 0:
                    crip_damage = 1
                    crip_HP = int(person_HP / 2)

                    display_battle.add_field(
                        name=f'Характеристики преред игрой:',
                        value=f"Твоё хп: `{person_HP}`\nХп крипа: `{crip_HP}`",
                        inline=False)

                    damage_itog = round(random.uniform(0.5, 2.0) * damage, 2)

                    damage_itog_person = round(
                        (round(random.uniform(0.5, 2.0), 2) * crip_damage) - (protection * damage_itog), 2)

                    display_battle.add_field(
                        name=f'Характеристики на ход {count}:',
                        value=f"Твоё хп: `{person_HP}` - `{damage_itog_person}`:drop_of_blood:\nХп крипа: `{crip_HP}`-`{damage_itog}`:drop_of_blood:",
                        inline=False)

                    crip_HP -= damage_itog

                    person_HP -= damage_itog_person
                    person_HP = round(person_HP, 2)

                    while True:
                        count += 1
                        damage_itog_person = round(
                            (round(random.uniform(0.5, 2.0), 2) * crip_damage) - (protection * damage_itog), 2)
                        damage_itog = round(random.uniform(0.5, 2.0) * damage, 2)

                        display_battle.add_field(
                            name=f'Характеристики на ход {count}:',
                            value=f"Твоё хп: `{person_HP}`-`{damage_itog_person}`:drop_of_blood:\nХп крипа: `{crip_HP}`-`{damage_itog}`:drop_of_blood:",
                            inline=False)

                        person_HP -= damage_itog_person
                        person_HP = round(person_HP, 2)

                        crip_HP -= damage_itog
                        crip_HP = round(crip_HP, 2)

                        if crip_HP < 0:
                            display_battle.add_field(
                                name=f'Ты выиграл! \n {description}',
                                value=f"Твоё хп оставшеесе хп: `{person_HP}`",
                                inline=False,
                            )
                            break
                        elif person_HP < 0:
                            display_battle.add_field(
                                name=f'Ты проиграл и остался в этой локации, как призрак. Отнеси своё тело в таверну и отдохни',
                                value=f" Оставшеесе хп крипа: `{crip_HP}`",
                                inline=False)
                            break
                    self.update_db('person', 'HP', person_HP,
                                   f'id={ctx.message.author.id}')  # обновление HP после битвы
                    await ctx.send(embed=display_battle)
            # нужно реалезовать синхронную функцию боя

        except Exception as err:
            print(err)

    @commands.command()
    @commands.check_any(check_reg_channel(), check_tav_channel(), check_battle_channel())
    async def inventory(self, ctx, *args):
        in_hand_temp = self.read_db('in_hand', f'person where id = {ctx.message.author.id}')[0]  # id оружия в руках
        on_body_temp = self.read_db('on_body', f'person where id = {ctx.message.author.id}')[0]  # id вещи на теле
        in_hand = self.read_db('name', f'weapons where id = {in_hand_temp}')[0]  # имя оружия в руках
        on_body = self.read_db('name', f'armor where id = {on_body_temp}')[0]  # имя вещи на теле

        weapons_inventory_temp = self.read_db('inventory_weapons', f'person where id = {ctx.message.author.id}')[
            0].split(', ')  # массив со всеми оружиями игрока
        weapons_inventory = ''
        for i in range(len(weapons_inventory_temp)):  # создание инвентаря для отображения юзеру
            weapon_data = self.read_db('*', f'weapons where id = {weapons_inventory_temp[i]}')[0]
            weapons_inventory += f'\n {i + 1}. {weapon_data[1]}: урон - {weapon_data[3]}'

        armor_inventory_temp = self.read_db('inventory_armor', f'person where id = {ctx.message.author.id}')[
            0].split(', ')  # массив со всеми вещами игрока
        armor_inventory = ''
        for i in range(len(armor_inventory_temp)):  # создание инвентаря для отображения юзеру
            armor_data = self.read_db('*', f'armor where id = {armor_inventory_temp[i]}')[0]
            armor_inventory += f'\n {i + 1}. {armor_data[1]}: защита - {armor_data[4]}'

        if not args:
            await ctx.send(f'В вашей руке сейчас {in_hand} и надето {on_body}\n'
                           f'Для изменения сета выберете вкладку инвентаря:\n '
                           f'1.weapon (t! inventory weapons)\n'
                           f'2.armor (t! inventory armor)')
        elif args[0] == 'weapons' and len(args) == 1:
            await ctx.send(f'Ваше оружие {weapons_inventory}')
        elif args[0] == 'armor' and len(args) == 1:
            await ctx.send(f'Ваша броня {armor_inventory}')

        elif args[0] == 'weapons' and int(args[1]) <= len(

                weapons_inventory_temp):  # изменение экипированного оружия

            new_in_hand = int(weapons_inventory_temp[int(args[1]) - 1])

            new_in_hand_name = self.read_db('name', f'weapons where id = {new_in_hand}')[0]

            self.update_db('person', 'in_hand', new_in_hand, f'id={ctx.message.author.id}')

            await ctx.send(f'Вместо {in_hand} теперь экипирован {new_in_hand_name}')

        elif args[0] == 'armor' and int(args[1]) <= len(armor_inventory_temp):  # изменение экипированной вещи
            new_on_body = int(armor_inventory_temp[int(args[1]) - 1])
            print(armor_inventory_temp)
            new_on_body_name = self.read_db('name', f'armor where id = {new_on_body}')[0]
            self.update_db('person', 'on_body', new_on_body, f'id={ctx.message.author.id}')
            await ctx.send(f'Вместо {on_body} теперь экипирован {new_on_body_name}')

        else:
            await ctx.send(
                f'Вы ввели значение на языке древних эльфов. Пожалуйста, обратитесь по одной из этих комманд:\n'
                f'1.weapon (t! inventory weapons)\n'
                f'2.armour (t! inventory armor)')

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
    @commands.check_any(check_reg_channel(), check_tav_channel())
    async def players_list(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        data = self.read_db('*', 'person')
        await ctx.send(
            'OK, {0}. Вот твои пользователи:\n {1}'.format(ctx.message.author.mention, data))

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
                await member.dm_channel.send(embed=regEmb)
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
