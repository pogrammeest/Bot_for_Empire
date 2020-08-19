import discord

helpEmb = discord.Embed(colour=discord.Colour.from_rgb(150, 206, 214))
helpEmb.set_author(name='Список команд',
                   icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
helpEmb.add_field(name='Обычные команды',
                  value="`hello`")
helpEmb.add_field(name="Комманды для игры",
                  value="`register`, `players_list`, `location`, `profile`")

regEmb = discord.Embed(title='Великая GameName', colour=discord.Colour.from_rgb(150, 206, 214))
regEmb.set_author(name="Злой ГМ",
               icon_url='https://clipart-best.com/img/ruby/ruby-clip-art-20.png')
regEmb.add_field(name='Приветствую тебя, дорогой искатель приключений!',
              value="Ты попал в ванильный фэнтезийный бред. Заставим Рому это писать.",
              inline=False)
regEmb.add_field(name="Комманды для игры",
              value="`players_list`, `location`, `profile`")


