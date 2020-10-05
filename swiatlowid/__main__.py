#!/usr/bin/env python3

import sys
import argparse

from . import __version__, Swiatlowid

def main():
    parser = argparse.ArgumentParser(description="Swiatlowid IRC bot {}".format(__version__))
    parser.add_argument("--port", type=int, default=6667, help="server port")
    parser.add_argument("--nickname", default="swiatlowid", help="nickname to be used by bot")
    parser.add_argument("--password", default=None, help="password")
    parser.add_argument("--prefix", default=None, help="command prefix")
    parser.add_argument("server", help="server address")
    parser.add_argument("channel", help="channel on which bot will operate")

    args = parser.parse_args()

    bot = Swiatlowid.Swiatlowid(args.server, args.channel, args.port, 
                     args.nickname, args.password, args.prefix)
    bot.start()


if __name__ == "__main__":
    main()
