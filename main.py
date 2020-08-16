''' Основной файл в который будем импортировать sql'''

import discord, os
from discord.ext import commands
from discord.utils import get
import variables
from variables import *

import sqlite3


class Base(commands.Cog):
    def __init__(self, bot):  # Иницилизация для работы регистра
        self.dictin = {}
        self.i = 0
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.message.author.mention}!')

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=helpEmb)


class Game(commands.Cog):
    def __init__(self, bot):  # Иницилизация для работы регистра
        self.dictin = {}
        self.i = 0
        self.bot = bot

    def check_category(ctx):  # функция для декоратора проверки категории
        return ctx.channel.category.id == 744483296032981093

    @commands.command()
    @commands.check(check_category)
    async def players_list(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        await ctx.send(f'OK, {ctx.message.author.mention} Вот твои пользователи:\n {self.dictin}')

    @commands.command()
    @commands.check(check_category)
    async def register(self, ctx):  # Пример регистрации пользователей.В дальнейшем заменим!
        member = ctx.message.author
        role = get(member.guild.roles, name="test_role")  # получаем нужную роль

        if get(member.roles, name='test_role'):  # проверка существует ли у этого пользователя роль
            await ctx.send(f'{member.mention} - ты уже зарегистрирован!')

        else:
            self.dictin[self.i] = f'{member}'
            self.i += 1

            print(f'Роль {role} добавленна юзеру {member}!')
            await member.add_roles(role)
            await member.create_dm()
            await member.dm_channel.send(embed=regEmb)

            await ctx.send(f'{member.mention} - тебя зарегистрировали!')


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
