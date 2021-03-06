import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.http import JsonResponse
from models import Message
from serializers import MessageSerializer
from rest_framework import status
from rest_framework.response import Response
from logs.models import Log, Action


@csrf_exempt
def login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            print(200)
            add_log("new login", "%s has login at %s" %(username, str(datetime.datetime.now)))
            return JsonResponse({'msg': 'hello '+username}, status=200)
        else:
            print(403)
            return JsonResponse({'msg': 'not allowed'}, status=403)


@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication))
@permission_classes((AllowAny,))
def message_list(request):
    """
    List all messages, or create a new message.
    """
    if request.method == 'GET':
        snippets = Message.objects.all()
        serializer = MessageSerializer(snippets, many=True)
        add_log('get all msgs', " list method")
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            add_log('new post', "user created a new post")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((AllowAny,))
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a message instance.
    """
    try:
        snippet = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        add_log('retrieve msg with id=%s'%(str(pk)))
        serializer = MessageSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            add_log('put msg with id=%s' % (str(pk)))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        add_log('delete msg with id=%s' % (str(pk)))
        return Response(status=status.HTTP_204_NO_CONTENT)


def add_log(title, description=''):
    action = Action()
    action.description = description
    log = Log()
    log.title = title
    log.actions.append(action)
    log.save()