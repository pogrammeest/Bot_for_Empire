''' Основной файл в который будем импортировать sql'''

import discord, os
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

    def check_reg_channel():  # функция для декоратора проверки канала регистрации
        def predicate(ctx):
            return ctx.guild is not None and ctx.channel.id == 753268164833443841

        return commands.check(predicate)

    def check_tav_channel():  # функция для декоратора проверки канала тавнерны
        def predicate(ctx):
            return ctx.guild is not None and loc_channel(ctx.channel.id) == 0

        return commands.check(predicate)

    def check_battle_channel():  # функция для декоратора проверки канала боевых лок
        def predicate(ctx):
            return ctx.guild is not None and loc_channel(ctx.channel.id) in [1, 2, 3, 4, 5, 6]

        return commands.check(predicate)

    @commands.command()
    @commands.check_any(check_reg_channel(), check_tav_channel())
    async def players_list(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        data = self.read_db('*', 'person')
        await ctx.send(
            'OK, {0}. Вот твои пользователи:\n {1}'.format(ctx.message.author.mention, data))

    @commands.command()
    @commands.check_any(check_reg_channel())
    async def register(self, ctx):  # Регистрация пользователей
        try:
            member = ctx.message.author
            mainRole = get(member.guild.roles, name="игрок")
            role = get(member.guild.roles, name="таверна")  # получаем нужную роль

            if get(member.roles, name='игрок'):  # проверка существует ли у этого пользователя роль
                await ctx.send(f'{member.mention} - ты уже зарегистрирован!')

            else:
                self.enter_db('person(id,name,HP,LVL,curent_loc,inventory_weapons,inventory_armor,in_hand,on_body,XP)',
                              (int(member.id), member.name, 10, 1, 1, '1', '1', 1, 1, 0))
                print(f'Роль {role} добавленна юзеру {member}!')
                await member.add_roles(mainRole)
                await member.add_roles(role)
                await member.create_dm()
                await member.dm_channel.send(embed=regEmb)
                await ctx.send(f'{member.mention} - тебя зарегистрировали!')
        except Exception as err:
            print(err)

    @commands.command()
    @commands.check_any(check_tav_channel(), check_battle_channel())
    async def location(self, ctx, *args):
        try:
            member = ctx.message.author

            if not args:
                await ctx.send(
                    'Твоя локация - ' + self.read_db('curent_loc', f'person where id = {ctx.message.author.id}')[0])
            elif args[0] in self.location:
                self.update_db('person', 'curent_loc', f'{args[0]}', f'id={ctx.message.author.id}')
                unnecessaryRole = get(member.guild.roles, name=locations[loc_channel(ctx.channel.id)])
                role = get(member.guild.roles, name=args[0])
                await member.remove_roles(unnecessaryRole)
                await member.add_roles(role)
                await ctx.send(f'Локация изменина на {args[0]}')
            else:

                temp_for_writing = ''
                for i in range(len(self.location)):
                    temp_for_writing += f'\n {i + 1}.' + self.location[i]
                await ctx.send('Нет такой локации, список доступных локаций:' + temp_for_writing)
        except Exception as err:
            print(err)

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
    @commands.check_any(check_battle_channel())
    async def crip_battle(self, ctx):  # недоделанно
        try:
            count = 1
            display_battle = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
            display_battle.set_author(name="Злой ГМ", icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')

            data = self.read_db('*', f'person where id = {ctx.message.author.id}')

            person_LVL = data[0][3]
            person_HP = data[0][2]

            person_weapon = data[0][7]
            damage = self.read_db('damage', f'weapons where id = {person_weapon}')[0]

            person_armor = data[0][8]
            protection = self.read_db('protection', f'armor where id = {person_armor}')[0]

            crip_LVL = person_LVL - 1

            description = self.read_db('description', 'mobs')

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

                person_HP -= round(damage_itog_person, 2)

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
                            name=f'Ты проиграл',
                            value=f" Оставшеесе хп крипа: `{crip_HP}`",
                            inline=False)
                        break
                await ctx.send(embed=display_battle)
            # нужно реалезовать синхронную функцию боя

        except Exception as err:
            print(err)


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
