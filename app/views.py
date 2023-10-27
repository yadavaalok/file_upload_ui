from flask import Blueprint, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
from zipfile import ZipFile

view = Blueprint('view', __name__)


ALLOWED_EXTENSIONS = {'pdf'}  # Set allowed file extensions

# Helper function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_files(request):
    file1 = request.files['file_upload']
    file2 = request.files['relevant_cost']
    for file in (file1, file2):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #Create a folder to store files
            file_path = f"/home/alok/Documents/AI_Project_Doc/flask_webapp/uploaded_files/{filename}"
            file.save(file_path)


@view.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.files)
        save_files(request)
        return redirect('/file_processed')

    return render_template('new.html')

@view.route('/file_processed', methods=['GET'])
def processed_file():
    global directory_path,temp_zip_path
    directory_path = "/home/alok/Documents/AI_Project_Doc/flask_webapp/uploaded_files"
    files = os.listdir(directory_path)

    temp_zip_path = '/home/alok/Documents/AI_Project_Doc/flask_webapp/uploaded_files/downloaded_files.zip'
    with ZipFile(temp_zip_path, 'w') as zipf:
        for file in files:
            file_path = os.path.join(directory_path, file)
            zipf.write(file_path, os.path.basename(file_path))

    return render_template('form_with_download.html')

@view.route('/download')
def download_file():
    # Use the send_file function to send the file for download
    return send_file(temp_zip_path, as_attachment=True)

@view.route('/back_home', methods=['GET'])
def back_to_home():
    #While going back to home page we will delete the files from uploaded folder
    files = os.listdir(directory_path)

    for file in files:
        file_path = os.path.join(directory_path, file)
        os.remove(file_path)

    return redirect('/home')