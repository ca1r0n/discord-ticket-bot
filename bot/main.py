import discord
import asyncio
from asyncio import sleep
from discord.ext import commands
from discord.utils import get
from config import settings
import datetime

bot = commands.Bot(settings['prefix'])
bot.remove_command("help")

@bot.event
async def on_ready():
    print("BOT STARTED") 
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Жизнь...")) 
        await sleep(1200)

@bot.event
async def on_raw_reaction_add(payload):
    #канал для юзеров
    if payload.message_id == settings['id_message_with_reacton'] and payload.member.bot==False:
        if payload.emoji.id == settings['emoji_id_creat']:
            #удаление и создания реакции
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(settings['id_message_with_reacton'])
            emoji = bot.get_emoji(settings['emoji_id_creat'])
            await message.remove_reaction(emoji, payload.member)

            
            #проверка на уже созданный от этого человека канал
            channels=await payload.member.guild.fetch_channels()
            for name_channels in channels:
                #если тикет был уже создан
                if str(name_channels)==("билет-{}".format(payload.member.name).lower()):
                    answer = await message.channel.send(f"<@{payload.user_id}>, вы уже создали канал.")
                    await sleep(5)
                    await answer.delete()
                    break
            else:
                #добавление текстового канала + права
                ticket_channel = await payload.member.guild.create_text_channel(name=f'билет {payload.member.name}',category=payload.member.guild.get_channel(settings['category']))
                await ticket_channel.set_permissions(payload.member.guild.get_role(payload.member.guild.id), send_messages=False, read_messages=False)
                role = payload.member.guild.get_role(settings['role_id_helper'])
                await ticket_channel.set_permissions(role, send_messages=True, read_messages=True)
                await ticket_channel.set_permissions(bot.get_user(payload.user_id), send_messages=True, read_messages=True)
                #отправление в созданый текстовый канал  c инструкцией
                emb_panel=discord.Embed(title="Инструкция по панели для админов",color = discord.Color.blue())
                emb_panel.add_field(name=f"{settings['emoji_id_delete_full_name']}", value="Удалить тикет",inline=False)
                emb_panel.add_field(name=f"{settings['emoji_id_agree_full_name']}", value="Подтверждение удаления тикета",inline=False)
                emb_panel.add_field(name=f"{settings['emoji_id_disagree_full_name']}", value="Отмена удаления тикета",inline=False)
                emb_panel = await ticket_channel.send(embed=emb_panel)
                emoji = bot.get_emoji(settings['emoji_id_delete'])
                await emb_panel.add_reaction(emoji=emoji)
                #отправление в созданый текстовый канал  с основной инофрмацией
                now_date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                emb=discord.Embed(title="Можешь теперь писать свой вопрос.",description=f'Время создания тикета {now_date}',color=discord.Color.blue())
                emb = await ticket_channel.send(embed=emb)
        #если поставили другой смайлик,а не тот который нужен
        else:
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            emoji = bot.get_emoji(payload.emoji.id)
            await message.remove_reaction(emoji, payload.member)
    #реакции в созданных каналах
    elif (payload.member.bot==False) and payload.channel_id!=settings['id_channel_log'] and payload.channel_id!=settings['id_message_with_reacton']:
        channel = (bot.get_channel(payload.channel_id))
        if str(channel)[0:6]=='билет-':
            #проверка что это был тот кому можно было
            for role in payload.member.roles:
                if (role.name) in settings['role_with_permisions']:
                    #удаление канала
                    if payload.emoji.id == settings['emoji_id_delete']:
                        message = await channel.fetch_message(payload.message_id)
                        emoji = bot.get_emoji(settings['emoji_id_delete'])
                        await message.remove_reaction(emoji, payload.member)
                        emb=discord.Embed(title='Подтвердите удаление канала', color=discord.Color.red())
                        message_agree = await channel.send(embed=emb)
                        emoji=bot.get_emoji(settings['emoji_id_agree'])
                        emoji2=bot.get_emoji(settings['emoji_id_disagre'])
                        await message_agree.add_reaction(emoji=emoji)
                        await message_agree.add_reaction(emoji=emoji2)
                        await sleep(5)
                        await message_agree.delete()
                    #подтверждение удаление канала + отправка в log
                    elif payload.emoji.id == settings['emoji_id_agree']:
                        await channel.delete()
                        channel_log = (bot.get_channel(settings['id_channel_log']))
                        now_date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                        emb=discord.Embed(title=f'Тикет {(channel.name)[6:]}-а был закрыт {payload.member.name}-ом',color=discord.Color.green())
                        emb.add_field(name='Время:', value=f"{now_date}",inline=False)
                        await channel_log.send(embed=emb)
                    #отмена удаления + чистка сообщения
                    elif payload.emoji.id == settings['emoji_id_disagre']:
                        message = await channel.fetch_message(payload.message_id)
                        await message.delete()


#команда хелп ми обычная
@bot.command()
async def help(ctx):
    emb=discord.Embed(title="",color = discord.Color.from_rgb(250,250,0)  )
    emb.add_field(name='Описание системы тикетов', value="Теперь Вы можее спросить о чем-либо через бота, где вам ответит администрация (на данный момент это тех. админ и хелперы)",inline=False)
    emb.add_field(name='P.S', value="Когда открываете тикет, сразу пишите, какой у Вас вопрос, не ждите, пока тикет возьмет кто-то из администрации. Если я вижу пустые открытые тикеты в течении минут 10 - я считаю этот тикет недействительным",inline=False)
    emb.set_author(name=settings['bot'],icon_url=bot.user.avatar_url)
     
    emb2=discord.Embed(title="",color = discord.Color.blue()  )
    emb2.add_field(name='Создать', value=f"Поставь на это сообщение реакию {settings['emoji_id_creat_full_name']}, чтобы создать тикет.",inline=False)

    await ctx.send(embed=emb)
    emb2 = await ctx.send(embed=emb2)
    emoji = bot.get_emoji(settings['emoji_id_creat'])
    await emb2.add_reaction(emoji=emoji)
    #сохранение сообщения(основного)
    settings['id_message_with_reacton']=int(emb2.id)
    #сохранение категории
    settings['category']=int(discord.utils.get(ctx.guild.channels, name="TicketBot").id)
    #сохранение лог канал
    log_channel = await ctx.guild.get_channel(settings['category']).create_text_channel("log")
    await log_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
    settings['id_channel_log']=int(log_channel.id)
bot.run(settings['token'])

#url=https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions=8.format(setting[id])

#TIME
#import datetime
#now_date=datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

#emb creat
#emb=discord.Embed(title='Описание системы тикетов')
#emb.add_field(name='', value="",inline=False)
#await ctx.send(embed=emb)

#Author in emb massage
#emb.set_author(name=bot.user.name,icon_url=bot.user.avatar_url)
#emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

#Status bot(not can have custon predix)
#await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Говно из жопы"))   