from swiatlowid import plugin

@plugin.command
def jeszczejak(bot, client, event, args):
    client.privmsg(bot.channel, "Jeszcze jak, {}!".format(event.source.nick))

@plugin.command
def elementy(bot, client, event, args):
    client.privmsg(bot.channel, "{}: {}".format(event.source.nick, str(args).strip('[]')))

@plugin.command
def rozlacz(bot, client, event, args):
    bot.disconnect()

@plugin.command
def padnij(bot, client, event, args):
    bot.die()

@plugin.command
def statystyki(bot, client, event, args):
    for chname, chobj in bot.channels.items():
        client.notice(nick, "Kanał: " + chname)
        users = sorted(chobj.users())
        client.notice(nick, "Użytkownicy: " + ", ".join(users))
        opers = sorted(chobj.opers())
        client.notice(nick, "Operatorzy: " + ", ".join(opers))
        voiced = sorted(chobj.voiced())
        client.notice(nick, "Z prawem głosu: " + ", ".join(voiced))

@plugin.command
def dcc(bot, client, event, args):
    dcc = bot.dcc_listen()
    client.ctcp(
        "DCC",
        event.source.nick,
        "CHAT chat %s %d"
        % (ip_quad_to_numstr(dcc.localaddress), dcc.localport),
    )
