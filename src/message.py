#   Copyright (C) 2015 Chen Chin Jieh <cchen@hsr.ch>
#
#   This file is part of mugenplcfg.
#
#   mugenplcfg is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   mugenplcfg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with mugenplcfg.  If not, see <http://www.gnu.org/licenses/>.


# Module to contain functions to handle messages
import sys
import customExceptions
import textwrap

textWrapper = textwrap.TextWrapper(
    break_long_words=False, replace_whitespace=False)


class Message():
    shortname = "message(s)"
    "Class that describes messages displayed at end of program"

    def __init__(self, msg):
        self.msg = msg
        addToCount(Message)

    def display(self):
        print textWrapper.fill(self.msg)


class WarningMessage(Message):
    shortname = "warning(s)"

    def __init__(self, msg):
        self.msg = msg
        addToCount(WarningMessage)

    def display(self):
        print textWrapper.fill("* WARNING *: %s" % self.msg)


class ErrorMessage(Message):
    shortname = "error(s)"

    def __init__(self, msg, forcequit=False):
        self.msg = msg
        addToCount(ErrorMessage)

    def display(self):
        print textWrapper.fill("** ERROR **: %s" % self.msg)


def addToCount(classname):
    if classname not in messagecount:
        messagecount[classname] = 1
    else:
        messagecount[classname] += 1


def printMessages():
    for message in messagequeue:
        message.display()
        print ""


def add(Message):
    exists = False
    for message in messagequeue:
        if Message.msg == message.msg:
            exists = True
            break

    if not exists:
        messagequeue.append(Message)


def addWarning(msg):
    add(WarningMessage(msg))


def addMessage(msg):
    add(Message(msg))


def addError(msg, forcequit=True):
    """
    Adds Error Message class to messagequeue; Sets flag to end program if
    "forcequit is True"""
    add(ErrorMessage(msg))
    if forcequit:
        forceQuit()


def forceQuit():
    raise customExceptions.ForceQuit()


def reset():
    globals()["messagequeue"] = []
    globals()["messagecount"] = {}

messagecount = {}  # Message, count
messagequeue = []
