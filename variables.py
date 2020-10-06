import discord
import sqlite3

helpEmb = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
helpEmb.set_author(name='Список команд',
                   icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
helpEmb.add_field(name='Обычные команды',
                  value="`hello`")
helpEmb.add_field(name="Комманды для игры",
                  value="`crip_battle`, `inventory`, `location`, `players_list`, `profile`, `register`, `rest`")

regEmb = discord.Embed(title='Великая GameName', colour=discord.Colour.from_rgb(150, 206, 214))
regEmb.set_author(name="Злой ГМ",
                  icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
regEmb.add_field(name='Приветствую тебя, дорогой искатель приключений!',
                 value="Ты попал в ванильный фэнтезийный бред. Заставим Рому это писать.",
                 inline=False)
regEmb.add_field(name="Комманды для игры",
                 value="`crip_battle`, `inventory`, `location`, `players_list`, `profile`, `register`, `rest`")

loc_channel = {744484105852551239: 0, 'таверна': 0,
               744948183242637374: 1, 'лес': 1,
               744483452203696160: 2, 'болото': 2,
               744947492923244615: 3, 'могильник': 3,
               744947400489173152: 4, 'цитадель': 4,
               744948528018620547: 5, 'лабиринт': 5,
               744947464448114798: 6, 'зиккурат': 6,
               753268164833443841: -1} #канал регистрации
