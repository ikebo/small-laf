import uuid
import datetime
import os
from app import app

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def get_fileRoute(filename):
    file = str(uuid.uuid4()) + '.' + filename.rsplit('.',1)[1].lower()
    folder = os.path.join(app.config['UPLOAD_FOLDER'],get_current_date())
    if not os.path.exists(folder):
        os.mkdir(folder)
    return os.path.join(folder,file)