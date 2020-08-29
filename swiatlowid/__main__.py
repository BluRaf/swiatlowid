#!/usr/bin/env python3

import sys
import argparse

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

from . import plugin

class Swiatlowid(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
            self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("Napisałeś: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmdline):
        c = self.connection

        cmd_list = cmdline.split()
        cmd = cmd_list[0]

        if cmd in plugin.plugins.keys():
            cmd_func = plugin.plugins[cmd]
            cmd_func(self, c, e, cmd_list[1:])
        else:
            c.notice(e.source.nick, "Not understood: " + cmd)


def main():
    parser = argparse.ArgumentParser(description="IRC bot.")
    parser.add_argument("server", help="server[:port]")
    parser.add_argument("channel", help="channel on which bot will operate")
    parser.add_argument("nickname", help="nickname to be used by bot")

    args = parser.parse_args()

    s = args.server.split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            parser.print_help()
            sys.exit(1)
    else:
        port = 6667
    channel = args.channel
    nickname = args.nickname

    plugin.scan('swiatlowid.plugins')

    bot = Swiatlowid(channel, nickname, server, port)
    bot.start()


if __name__ == "__main__":
    main()
