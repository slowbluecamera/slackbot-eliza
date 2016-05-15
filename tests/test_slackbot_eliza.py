# -*- coding: utf-8 -*-


import sys
from importlib import import_module
import pytest
from helper import MockBot

not_implemented = pytest.mark.xfail(reason="test not implemented/complete")

def test_hello(monkeypatch):

    bot = MockBot()

    monkeypatch.setattr('slackbot.bot.listen_to', bot.mock_listen_to)
    monkeypatch.setattr('slackbot.bot.respond_to', bot.mock_respond_to)
    monkeypatch.setattr('slackbot.bot.default_reply', bot.mock_default_reply)

    sys.path.append("slackbot-eliza")
    import_module("slackbot-eliza")

    r = bot.respond("Hello")
    assert r[0]['msg'] == 'reply'
    assert (r[0]['text'] == "Hello... I'm glad you could drop by today." or
            r[0]['text'] == "Hi there... how are you today?" or
            r[0]['text'] == "Hello, how are you feeling today?")

    r = bot.respond("Yes")
    assert r[0]['msg'] == 'reply'
    assert (r[0]['text'] == "You seem quite sure." or
            r[0]['text'] == "OK, but can you elaborate a bit?")

    r = bot.respond("Why not")
    assert r[0]['msg'] == 'reply'
    assert (r[0]['text'] == "Why don't you tell me the reason why not?" or
            r[0]['text'] == "Why do you think not?")
