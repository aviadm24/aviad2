from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
from django.conf import settings
from .models import User_tokens
from django.contrib.sessions.backends.db import SessionStore
import pytesseract
from PIL import Image
from django.core.files.storage import FileSystemStorage

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

# AUTHORIZATION_SCOPE = 'openid email profile'
AUTHORIZATION_SCOPE ='openid email profile https://www.googleapis.com/auth/contacts https://www.googleapis.com/auth/drive.file'

AUTH_REDIRECT_URI = settings.FN_AUTH_REDIRECT_URI
BASE_URI = settings.FN_BASE_URI
CLIENT_ID = settings.FN_CLIENT_ID
CLIENT_SECRET = settings.FN_CLIENT_SECRET

AUTH_TOKEN_KEY = 'auth_token'
AUTH_STATE_KEY = 'auth_state'


def home(request):
    return render(request, 'home/home.html')


def is_logged_in(request):
    return True if AUTH_TOKEN_KEY in request.session else False


def build_credentials(s_key):
    # if not is_logged_in(request):
    #     raise Exception('User must be logged in')
    s = SessionStore(session_key=s_key)
    oauth2_tokens = s['auth_tokens']
    # oauth2_tokens = request.session[AUTH_TOKEN_KEY]
    print('refresh token: ', oauth2_tokens['refresh_token'])
    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)


def build_credentials_from_refresh(refresh_token):
    return google.oauth2.credentials.Credentials(
        None,
        refresh_token=refresh_token,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)


def get_user_info(s_key):
    credentials = build_credentials(s_key)

    oauth2_client = googleapiclient.discovery.build(
        'oauth2', 'v2',
        credentials=credentials)

    return oauth2_client.userinfo().get().execute()



def login(request):
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            redirect_uri=AUTH_REDIRECT_URI)

    uri, state = session.create_authorization_url(AUTHORIZATION_URL)
    request.session[AUTH_STATE_KEY] = state
    s = SessionStore()
    s['auth_state'] = state
    s.create()
    s_key = s.session_key
    request.session['s_key'] = s_key
    # print('----------------------')
    # print(request.session[AUTH_STATE_KEY])
    # print('----------------------')
    # request.session.permanent = True

    return redirect(uri, code=302)


def google_auth_redirect(request):
    req_state = request.GET.get('state')
    # print('----------------------')
    # print('req s_key: ', request.session['s_key'])
    # print('----------------------')
    # s_key = request.session['s_key']
    # s = SessionStore(session_key=s_key)
    #
    # if req_state != s['auth_state']:
    #     response = HttpResponse('no state key', code=401)
    #     return response
    session = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            # state=s['auth_state'],
                            state=req_state,
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
        ACCESS_TOKEN_URI,
        authorization_response=request.get_full_path())
    # request.session[AUTH_TOKEN_KEY] = oauth2_tokens
    s = SessionStore()
    s['auth_tokens'] = oauth2_tokens
    s.create()
    s_key = s.session_key

    user_info = get_user_info(s_key)
    print('user info: ', user_info['given_name'])
    user = User_tokens()
    user.name = user_info['given_name']
    user.refresh_token = oauth2_tokens['refresh_token']
    user.save()

    return redirect(BASE_URI, code=302)


def build_people_api_v1(request):

    credentials = build_credentials(request)
    return googleapiclient.discovery.build('people', 'v1', credentials=credentials)


def build_people_from_refresh(name):
    user = User_tokens.objects.get(name=name)
    refresh_token = user.refresh_token
    credentials = build_credentials_from_refresh(refresh_token)
    return googleapiclient.discovery.build('people', 'v1', credentials=credentials)


def create_new_contact(request):
    people_api = build_people_api_v1(request)
    # https: // stackoverflow.com / questions / 46948326 / creating - new - contact - google - people - api
    # http: // www.fujiax.com / stackoverflow_ / questions / 57538504 / google - people - api - in -python - gives - error - invalid - json - payload - received - unknown
    contact1 = people_api.people().createContact(
        body={"names": [{"givenName": "John", "familyName": "Doe"}],
              "emailAddresses": [{"value": "jenny.doe@example.com"}],
              "phoneNumbers": [{"value": "0547573120"}]
              })
    print('==============')
    print(contact1)
    # "phoneNumbers": [{"phoneNumber": "0547573120"}]
    contact1.execute()
    return {"names": [{"givenName": "John", "familyName": "Doe"}]}
    # people_api.people().createContact(contactToCreate).execute()



def google_contacts_app(request):
    print('----------------------')
    print(request.session.items())
    print('----------------------')
    return render(request, 'home/list.html')


@csrf_exempt
def add_contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        contact_name = request.POST.get('contact_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        # message = request.POST.get('message')
        print('create contact function name: ', contact_name)
        people_api = build_people_from_refresh(user_name)
        # https: // stackoverflow.com / questions / 46948326 / creating - new - contact - google - people - api
        # http: // www.fujiax.com / stackoverflow_ / questions / 57538504 / google - people - api - in -python - gives - error - invalid - json - payload - received - unknown
        contact = people_api.people().createContact(
            body={"names": [{"givenName": user_name, "familyName": user_name}],
                  "emailAddresses": [{"value": email}],
                  "phoneNumbers": [{"value": phone}]
                  })
        print('==============')
        print(contact)
        # "phoneNumbers": [{"phoneNumber": "0547573120"}]
        contact.execute()
        return render(request, 'home/list.html', {'success': contact_name})


@csrf_exempt
def update_sheets(request):
    if request.method == 'POST':
        print('post: ', request.POST)
        return render(request, 'home/list.html')



@csrf_exempt
def action_check(request):
    import json
    print(request)
    if request.method == 'POST':
        # print(json.loads(request.body))

        action = json.loads(request.body.decode("utf-8"))
        # action_success = request.POST.get('action_success')
        err = request.POST.get('err')
        print('action: {} - success: {}'.format(action['action_id'], action['action_success']))
        email = EmailMessage('action check ', 'action: {} - success: {}'.format(action['action_id'], action['action_success']), to=['aviadm24@gamil.com'])
        email.send()
    return render(request, 'home/privacy_policy.html')



def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')


@csrf_exempt
def send_mail(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        email = EmailMessage('sent from '+name, message + ' ' + str(phone), to=['aviadm24@gamil.com'])
        email.send()
    return HttpResponse("")


def pdf_booklet_demo(request):
    return render(request, 'home/pdf_booklet_demo.html')


def lesson1(request):
    return render(request, 'home/lesson1.html')


def lesson2(request):
    return render(request, 'home/lesson2.html')


def lesson3(request):
    return render(request, 'home/lesson3.html')


def lesson4(request):
    return render(request, 'home/lesson4.html')


def lesson5(request):
    return render(request, 'home/lesson5.html')


def plain_ocr(filename):
    text = pytesseract.image_to_string(Image.open(filename), lang='heb')
    with open('after_clean7.txt', 'w', encoding='utf8') as f:
        f.write(text)
    return text


# https://stackoverflow.com/questions/53363547/how-to-deploy-pytesseract-to-heroku
@csrf_exempt
def image_upload(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save('home/static/images/'+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        text = plain_ocr(uploaded_file_url)
        uploaded_file_url = '/'.join(fs.url(filename).split('/')[2:])
        print('uploaded_file_url: ', uploaded_file_url)
        return render(request, 'home/ocr.html', {
            'text': text,
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'home/ocr.html')

