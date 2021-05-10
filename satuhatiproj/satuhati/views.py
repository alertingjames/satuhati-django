import requests
from django.core.mail import EmailMultiAlternatives

from django.core.files.storage import FileSystemStorage
import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import time

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from random import randint

from satuhati.models import SatuhatiMember, Music, Like
from satuhati.serializers import SatuhatiMemberSerializer, MusicSerializer


def index(request):
    return HttpResponse('<h1>Hello I am Satuhati backend!</h1>')


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def signup(request):

    if request.method == 'POST':

        name = request.POST.get('name', '')
        eml = request.POST.get('email', '')
        password = request.POST.get('password', '')

        users = SatuhatiMember.objects.filter(email=eml)
        count = users.count()
        if count == 0:
            member = SatuhatiMember()
            member.name = name
            member.email = eml
            member.picture_url = settings.URL + '/static/images/2428675.png'
            member.password = password
            member.auth_status = str(random_with_N_digits(5))
            member.registered_time = str(int(round(time.time() * 1000)))
            member.latitude = '0'
            member.longitude = '0'
            member.altitude = '0'
            member.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    member.picture_url = settings.URL + uploaded_url
                    member.save()

            sendcode(member.email, member.auth_status)

            serializer = SatuhatiMemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            users = SatuhatiMember.objects.filter(email=eml, password=password)
            count = users.count()
            if count == 0:
                resp_er = {'result_code': '1'}
                return HttpResponse(json.dumps(resp_er))
            else:
                resp_er = {'result_code': '2'}
                return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



def sendcode(email, code):

    message = 'You signed up with Satuhati app.<br>We want to verify your email by a verification code.<br>Your verification code: ' + code + '<br>Please enter this verification code in your app to validate your email.<br>Satuhati'

    html =  """\
                <html>
                    <head></head>
                    <body>
                        <a href="#"><img src="https://schocher.pythonanywhere.com/static/images/logo.png" style="width:150px;height:120px;border-radius: 8%; margin-left:25px;"/></a>
                        <h2 style="margin-left:10px; color:#02839a;">Satuhati Administrator Authentication</h2>
                        <div style="font-size:14px; word-break: break-all; word-wrap: break-word;">
                            {mes}
                        </div>
                    </body>
                </html>
            """
    html = html.format(mes=message)

    fromEmail = 'admin@satuhati.my'
    toEmailList = []
    toEmailList.append(email)
    msg = EmailMultiAlternatives('SATUHATI OPT Authentication', '', fromEmail, toEmailList)
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def codesubmit(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '')
        code = request.POST.get('code', '')

        resp = {'result_code':'2'}
        users = SatuhatiMember.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            if member.auth_status != 'verified' and member.auth_status == code:
                member.auth_status = 'verified'
                member.save()
                resp = {'result_code':'0'}
            else:
                resp = {'result_code':'1'}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def resendcode(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '')
        resp = {'result_code':'1'}
        users = SatuhatiMember.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            member.auth_status = str(random_with_N_digits(5))
            member.save()

            sendcode(member.email, member.auth_status)

            resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))




@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if password != '':
            members = SatuhatiMember.objects.filter(email=email, password=password)
        else:
            members = SatuhatiMember.objects.filter(email=email)
        resp = {}
        if members.count() > 0:
            member = members[0]
            if member.auth_status != 'verified':
                member.auth_status = str(random_with_N_digits(5))
                member.save()
                sendcode(member.email, member.auth_status)
            serializer = SatuhatiMemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = SatuhatiMember.objects.filter(email=email)
            if members.count() > 0:
                resp = {'result_code': '2'}
            else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        usrs = SatuhatiMember.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        message = 'You are allowed to reset your password from your request.<br>For it, please click this link to reset your password.<br><br>https://schocher.pythonanywhere.com/resetpassword?email=' + email

        html =  """\
                    <html>
                        <head></head>
                        <body>
                            <a href="#"><img src="https://schocher.pythonanywhere.com/static/images/logo.png" style="width:150px;height:120px;border-radius: 8%; margin-left:25px;"/></a>
                            <h2 style="margin-left:10px; color:#02839a;">Satuhati User's Security Update Information</h2>
                            <div style="font-size:14px; word-break: break-all; word-wrap: break-word;">
                                {mes}
                            </div>
                        </body>
                    </html>
                """
        html = html.format(mes=message)

        fromEmail = 'admin@satuhati.my'
        toEmailList = []
        toEmailList.append(email)
        msg = EmailMultiAlternatives('We allowed you to reset your password', '', fromEmail, toEmailList)
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)

        return HttpResponse(json.dumps({'result_code': '0'}))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def addmusic(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        member_id = request.POST.get('member_id', '1')

        users = SatuhatiMember.objects.filter(id=member_id)
        count = users.count()
        if count == 0:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            music = Music()
            music.member_id = member_id
            music.member_name = users[0].name
            music.name = name
            music.time = str(int(round(time.time() * 1000)))
            music.likes = '0'

            fs = FileSystemStorage()

            file = request.FILES['file']

            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)

            music.url = settings.URL + uploaded_file_url
            music.save()

            resp = {'result_code': '0'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def allmusics(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        ms = Music.objects.all().order_by('-id')
        for m in ms:
            mlikes = Like.objects.filter(music_id=m.pk, member_id=member_id)
            if mlikes.count() > 0:
                m.liked = 'yes'
            else: m.liked = 'no'
        serializer = MusicSerializer(ms, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def likemusic(request):
    if request.method == 'POST':
        music_id = request.POST.get('music_id', '1')
        member_id = request.POST.get('member_id', '1')
        mlike = Like()
        mlike.music_id = music_id
        mlike.member_id = member_id
        mlike.liked_time = str(int(round(time.time() * 1000)))
        mlike.save()
        mlikes = Like.objects.filter(music_id=music_id)
        music = Music.objects.get(id=music_id)
        music.likes = str(mlikes.count())
        music.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def unlikemusic(request):
    if request.method == 'POST':
        music_id = request.POST.get('music_id', '1')
        member_id = request.POST.get('member_id', '1')
        mlikes = Like.objects.filter(music_id=music_id, member_id=member_id)
        if mlikes.count() > 0:
            mlike = mlikes[0]
            mlike.delete()
        mlikes = Like.objects.filter(music_id=music_id)
        music = Music.objects.get(id=music_id)
        music.likes = str(mlikes.count())
        music.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def profile_update(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        eml = request.POST.get('email', '')
        latitude = request.POST.get('latitude', '0')
        longitude = request.POST.get('longitude', '0')

        users = SatuhatiMember.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            member.name = name
            member.email = eml
            member.latitude = latitude
            member.longitude = longitude

            member.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    member.picture_url = settings.URL + uploaded_url
                    member.save()

            serializer = SatuhatiMemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def reglocation(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id','1')
        latitude = request.POST.get('latitude','0')
        longitude = request.POST.get('longitude','0')
        members = SatuhatiMember.objects.filter(id=member_id)
        if members.count() > 0:
            member = members[0]
            member.latitude = latitude
            member.longitude = longitude
            member.save()

        resp = {'result_code': '0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delmusic(request):
    if request.method == 'POST':
        m_id = request.POST.get('music_id','1')
        ms = Music.objects.filter(id=m_id)
        resp = {}
        fs = FileSystemStorage()
        if ms.count() > 0:
            m = ms[0]
            fname = m.url.replace(settings.URL + '/media/', '')
            fs.delete(fname)
            m.delete()
            resp = {'result_code': '0'}
        else:
            resp = {'result_code': '1'}
        return HttpResponse(json.dumps(resp))


def resetpassword(request):
    email = request.GET['email']
    return render(request, 'satuhati/resetpwd.html', {'email':email})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if password != repassword:
            return render(request, 'satuhati/result.html',
                          {'response': 'Please enter the same password.'})
        members = SatuhatiMember.objects.filter(email=email)
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'satuhati/result.html',
                          {'response': 'Password has been reset successfully.'})
        else:
            return render(request, 'satuhati/result.html',
                          {'response': 'You haven\'t been registered.'})
    else: pass









































