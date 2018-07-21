#only works with python2

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = "https://www.googleapis.com/auth/youtube.upload"#a string representing user permissions
CLIENT_SECRET = "./client_secret.json"

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow,store)
    
API = "youtube"
VERSION = "v3"


SERVICE = build(API, VERSION, http=credz.authorize(Http()))
#get API names and VERSIONs from the docs

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body = dict(
        snippet = dict(title = options.title,
                       description = options.description,
                       tags = tags,
                       categoryID = options.category
                    ),
        status = dict(
            privacyStatus = options.privacyStatus
            )
        )
    
