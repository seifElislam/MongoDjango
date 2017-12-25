# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet

from serializers import *


@permission_classes((AllowAny,))
class LogsViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = LogsSerializer

    def get_queryset(self):
        return Log.objects.all()