#google API client library
#only works with python2
#works!
#all file info into d: d = SERVICE.files().list().execute()
#title of a file from d: d['items'][0]['title']
#can also run d['items']['id']
import datetime
import apiclient.discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = "https://www.googleapis.com/auth/drive.birdPics"#a string representing user permissions
CLIENT_SECRET = "./client_id.json"
"""needed to delete the old storage
should switch to an app key (one that can access app data)"""
folderID = u"0Bzmn5wWjaNOaRWZSNGpJOHA0bk0"


store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow,store)
    
API = "drive"
VERSION = "v2"


SERVICE = apiclient.discovery.build(API, VERSION, http=credz.authorize(Http()))
#get API names and VERSIONs from the docs
def uploadPicture(filename="./bird20161030-214744.jpg"):
    """filename and title must have .jpg (or whatever extension)
body's 'parents' attribute must be a list of dictionaries"""
    date = str(datetime.date.today())
    MIMETYPE="image/jpeg"
    title = "first_bird.jpg"
    description = "this is my first bird upload"
    media_body = apiclient.http.MediaFileUpload(fileName, mimetype=MIMETYPE,
                                                resumable=False)
    body = {"title":title, "description":description,
            'parents':[{"id":folderID}]}
    new_file = SERVICE.files().insert(body=body,
                                      media_body = media_body,
                                      fields='id').execute()
    print new_file
