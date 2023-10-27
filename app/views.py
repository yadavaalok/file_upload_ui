from flask import Blueprint, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
import io

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
    return render_template('form_with_download.html')


@view.route('/download')
def download_file():
    # Generate the content to be downloaded
    content = "This is the content of the file that you can download."

    # Convert the content to bytes
    content_bytes = content.encode('utf-8')

    # Create an in-memory file-like object
    file_obj = io.BytesIO(content_bytes)

    # Use the send_file function to send the file for download
    return send_file(file_obj, as_attachment=True, download_name='downloaded_file.txt')
