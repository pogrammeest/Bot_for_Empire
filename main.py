''' Основной файл в который будем импортировать sql'''

import discord, os
from discord.ext import commands
from discord.utils import get
import variables
from variables import *
from SQLite import WWDB

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

    def check_category(ctx):  # функция для декоратора проверки категории
        return ctx.channel.category.id == 744483296032981093

    @commands.command()
    @commands.check(check_category)
    async def players_list(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        try:
            data = self.read_db('*', 'person')
            await ctx.send(
                'OK, {0}. Вот твои пользователи:\n {1}'.format(ctx.message.author.mention, data))
        except Exception as e:
            print(e)

    @commands.command()
    @commands.check(check_category)
    async def register(self, ctx):  # Пример регистрации пользователей.В дальнейшем заменим!
        member = ctx.message.author

        role = get(member.guild.roles, name="test_role")  # получаем нужную роль

        if get(member.roles, name='test_role'):  # проверка существует ли у этого пользователя роль
            await ctx.send(f'{member.mention} - ты уже зарегистрирован!')

        else:

            self.enter_db('person(id,name,HP,LVL,curent_loc,inventory_weapons,inventory_armor,in_hand,on_body)',
                          (int(member.id), member.name, 10, 1, 'таверня', '1', '1', 1, 1))
            print(f'Роль {role} добавленна юзеру {member}!')
            await member.add_roles(role)
            await member.create_dm()
            await member.dm_channel.send(embed=regEmb)

            await ctx.send(f'{member.mention} - тебя зарегистрировали!')

    @commands.command()
    @commands.check(check_category)
    async def location(self, ctx, *args):
        try:
            if not args:
                await ctx.send('Твоя локация')
            elif args[0] in self.location:
                await ctx.send(f'Локация изменина на {args[0]}' )
            else:
                await ctx.send('Нет такой локации, и ты лох')
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
                description=f'**{ctx.author.name}**, вы используете команду не в той категории какналов. Пожалуйста воспользуйтесь команндой **help** для определения необходимой категории.',
                color=discord.Colour.from_rgb(191, 56, 74)))

    bot.add_cog(Base(bot))
    bot.add_cog(Game(bot))

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
