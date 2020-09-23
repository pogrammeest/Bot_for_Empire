import discord
import sqlite3

helpEmb = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
helpEmb.set_author(name='Список команд',
                   icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
helpEmb.add_field(name='Обычные команды',
                  value="`hello`")
helpEmb.add_field(name="Комманды для игры",
<<<<<<< HEAD
                  value="`register`, `players_list`, `location`, `profile`")
=======
                  value="`register`, `players_list`")
>>>>>>> 3462ac52d5fc3c7b55a5a11109b7a7f03f3f227e

regEmb = discord.Embed(title='Великая GameName', colour=discord.Colour.from_rgb(150, 206, 214))
regEmb.set_author(name="Злой ГМ",
                  icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
regEmb.add_field(name='Приветствую тебя, дорогой искатель приключений!',
                 value="Ты попал в ванильный фэнтезийный бред. Заставим Рому это писать.",
                 inline=False)
regEmb.add_field(name="Комманды для игры",
                 value="`players_list`, `location`, `profile`")


def loc_channel(id):
    if id == 744484105852551239:  # таверня
        return 0
    elif id == 744948183242637374:  # лес
        return 1
    elif id == 744483452203696160:  # болота
        return 2
    elif id == 744947492923244615:  # могильник
        return 3
    elif id == 744947400489173152:  # цитадель
        return 4
    elif id == 744948528018620547:  # лабиринт
        return 5
    elif id == 744947464448114798:  # зиккурат
        return 6


locations = ['таверна', 'лес', 'болото', 'могильник', 'цитадель', 'лабиринт', 'зиккурат']
