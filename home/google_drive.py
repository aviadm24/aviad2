import io
import tempfile

import flask

from apiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import googleapiclient.discovery
from google_auth import build_credentials, get_user_info

from werkzeug.utils import secure_filename

app = flask.Blueprint('google_drive', __name__)


# from another file

# def get_authenticated_service():
#   flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#   credentials = flow.run_console()
#   return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
#
# def list_drive_files(service, **kwargs):
#   # Call the People API
#   print('List 10 connection names')
#   results = service.people().connections().list(
#     resourceName='people/me',
#     pageSize=10,
#     personFields='names,emailAddresses').execute()
#   connections = results.get('connections', [])
#
#   for person in connections:
#     names = person.get('names', [])
#     if names:
#       name = names[0].get('displayName')
#       print(name)
#
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# service = get_authenticated_service()
# list_drive_files(service,
#                orderBy='modifiedByMeTime desc',
#                pageSize=5)

#from another file



def build_drive_api_v3():
    credentials = build_credentials()
    return googleapiclient.discovery.build('drive', 'v3', credentials=credentials).files()


def build_people_api_v1():
    credentials = build_credentials()
    return googleapiclient.discovery.build('people', 'v1', credentials=credentials)


def create_new_contact():
    people_api = build_people_api_v1()
    # https: // stackoverflow.com / questions / 46948326 / creating - new - contact - google - people - api
    contact1 = people_api.people().createContact(
        body={"names": [{"givenName": "John", "familyName": "Doe"}],
              })
    print('==============')
    print(contact1)
    # "phoneNumbers": [{"phoneNumber": "0547573120"}]
    contact1.execute()
    return {"names": [{"givenName": "John", "familyName": "Doe"}]}
    # people_api.people().createContact(contactToCreate).execute()

def save_image(file_name, mime_type, file_data):
    drive_api = build_drive_api_v3()

    generate_ids_result = drive_api.generateIds(count=1).execute()
    file_id = generate_ids_result['ids'][0]

    body = {
        'id': file_id,
        'name': file_name,
        'mimeType': mime_type,
    }

    media_body = MediaIoBaseUpload(file_data,
                                   mimetype=mime_type,
                                   resumable=True)

    drive_api.create(body=body,
                     media_body=media_body,
                     fields='id,name,mimeType,createdTime,modifiedTime').execute()

    return file_id


@app.route('/google/add_contact', methods=['GET'])
def add_contact():

    contact = create_new_contact()
    print(contact)

    return flask.redirect('/')



@app.route('/gdrive/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in flask.request.files:
        return flask.redirect('/')

    file = flask.request.files['file']
    if (not file):
        return flask.redirect('/')

    filename = secure_filename(file.filename)

    fp = tempfile.TemporaryFile()
    ch = file.read()
    fp.write(ch)
    fp.seek(0)

    mime_type = flask.request.headers['Content-Type']
    save_image(filename, mime_type, fp)

    return flask.redirect('/')


@app.route('/gdrive/view/<file_id>', methods=['GET'])
def view_file(file_id):
    drive_api = build_drive_api_v3()

    metadata = drive_api.get(fields="name,mimeType", fileId=file_id).execute()

    request = drive_api.get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    fh.seek(0)

    return flask.send_file(
        fh,
        attachment_filename=metadata['name'],
        mimetype=metadata['mimeType']
    )