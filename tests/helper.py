# -*- coding: utf-8 -*-

import re

class MockBot(object):
    _commands = {
        'respond_to': {},
        'listen_to': {},
        'default_reply': {}
    }

    @classmethod
    def mock_respond_to(cls, matchstr, flags=0):
        def wrapper(func):
            cls._commands['respond_to'][re.compile(matchstr, flags)] = func
            return func
        return wrapper

    @classmethod
    def mock_listen_to(cls, matchstr, flags=0):
        def wrapper(func):
            cls._commands['listen_to'][re.compile(matchstr, flags)] = func
            return func
        return wrapper

    @classmethod
    def mock_default_reply(cls, matchstr=r'^.*$', flags=0):
        def wrapper(func):
            cls._commands['default_reply'][re.compile(matchstr, flags)] = func
            return func
        return wrapper

    def listen(self, text):
        return self._dispatch('listen_to', text)

    def respond(self, text):
        return self._dispatch('respond_to', text)

    def _dispatch(self, command, text):
        message = MockMessage(text)
        responded = False
        for matcher in self._commands[command]:
            m = matcher.search(text)
            if m:
                responded = True
                self._commands[command][matcher](message, *m.groups())

        if not responded:
            for matcher in self._commands['default_reply']:
                m = matcher.search(text)
                if m:
                    self._commands['default_reply'][matcher](message, *m.groups())
        return message.getHistory()

class MockMessage(object):
    _history = []
    _body = {}

    def __init__(self, text=None):
        self._history = []
        self._body['text'] = text

    def getHistory(self):
        return self._history

    #@unicode_compact
    def gen_reply(self, text):
        self._history.append({
            'msg': 'gen_reply',
            'text': text
        })

    #@unicode_compact
    def reply_webapi(self, text, attachments=None, as_user=True):
        self._history.append({
            'msg': 'reply_webapi',
            'text': text,
            'attachments': attachments,
            'as_user': as_user
        })

    #@unicode_compact
    def send_webapi(self, text, attachments=None, as_user=True):
        self._history.append({
            'msg': 'send_webapi',
            'text': text,
            'attachments': attachments,
            'as_user': as_user
        })

    #@unicode_compact
    def reply(self, text):
        self._history.append({
            'msg': 'reply',
            'text': text
        })

    #@unicode_compact
    def send(self, text):
        self._history.append({
            'msg': 'send',
            'text': text
        })

    def react(self, emojiname):
        self._history.append({
            'msg': 'react',
            'emojiname': emojiname
        })

    @property
    def channel(self):
        pass

    @property
    def body(self):
        return self._body

    def docs_reply(self):
        pass
