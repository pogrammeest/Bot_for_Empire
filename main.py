''' Основной файл в который будем импортировать sql'''

import discord, os
from discord.ext import commands
from discord.utils import get

import sqlite3


class Base(commands.Cog):
    def __init__(self, bot):  # Иницилизация для работы регистра
        self.dictin = {}
        self.i = 0
        self.bot = bot
        self.botName = 'Список комманд'
        self.botIconUrl = "https://clipart-best.com/img/ruby/ruby-clip-art-20.png"

    @commands.command()
    async def register(self, ctx):  # Пример регистрации пользователей.В дальнейшем заменим!
        member = ctx.message.author
        role = get(member.guild.roles, name="test_role")

        if get(member.roles, name='test_role'):
            await ctx.send(f'{member.mention} - ты уже зарегистрирован!')

        else:
            self.dictin[self.i] = f'{member}'
            self.i += 1

            print(f'Роль {role} добавленна юзеру {member}!')
            await member.add_roles(role)

            emb = discord.Embed(title='Великая GameName', colour=discord.Colour.from_rgb(150, 206, 214))
            emb.set_author(name="Злой ГМ",
                           icon_url=self.botIconUrl)
            emb.add_field(name='Приветствую тебя, дорогой искатель приключений!',
                          value="Ты попал в ванильный фэнтезийный бред. Заставим Рому это писать.",
                          inline=False)
            emb.add_field(name="Комманды для игры",
                          value="`register`, `players_list`")
            await member.create_dm()
            await member.dm_channel.send(embed=emb)

            await ctx.send(f'{member.mention} - тебя зарегистрировали!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.message.author.mention}!')

    @commands.command()
    async def players_list(self, ctx):  # Пример просмотра листа зарегестрированных пользователей
        await ctx.send(f'OK, {ctx.message.author.mention} Вот твои пользователи:\n {self.dictin}')

    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
        emb.set_author(name=self.botName,
                       icon_url=self.botIconUrl)
        emb.add_field(name='Обычные команды',
                      value="`hello`")
        emb.add_field(name="Комманды для игры",
                      value="`register`, `players_list`")
        await ctx.send(embed=emb)



def main():
    TOKEN = os.environ.get('TOKEN_FOR_BOT')
    bot = commands.Bot(command_prefix='t! ')
    bot.remove_command(name='help')

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=discord.Embed(
                description=f'**{ctx.author.name}**, данной команды не существует. Пожалуйста воспользуйтесь команндой **help** для полного списка команд.',
                color=discord.Colour.from_rgb(191, 56, 74)))

    bot.add_cog(Base(bot))

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
