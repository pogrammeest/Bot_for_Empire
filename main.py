''' Основной файл в который будем импортировать sql'''

import discord, os
from discord.ext import commands
import sqlite3


class Base(commands.Cog):
    def __init__(self, ctx):  # Иницилизация для работы регистра
        self.dictin = {}
        self.i = 0

    @commands.command()
    async def register(self, ctx):  # Пример регистрации пользователей.В дальнейшем заменим!
        self.dictin[self.i] = f'{ctx.message.author}'
        self.i += 1

        await ctx.send(f'{ctx.message.author.mention} - тебя зарегистрировали!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.message.author.mention}!')

    @commands.command()
    async def inventory(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        await ctx.send(f'OK, {ctx.message.author.mention} Вот твои пользователи:\n {self.dictin}')


def main():
    bot = commands.Bot(command_prefix='t! ')

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    bot.add_cog(Base(bot))

    bot.run('token')


if __name__ == '__main__':
    main()
