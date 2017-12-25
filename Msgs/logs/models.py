# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from mongoengine import Document, EmbeddedDocument, fields


# class Action(EmbeddedDocument):
#     description = fields.StringField(required=False, null=True)


class Log(Document):
    title = fields.StringField(required=True, max_length=200)
    posted = fields.DateTimeField(default=datetime.datetime.utcnow)
    # actions = fields.EmbeddedDocumentListField(Action)
