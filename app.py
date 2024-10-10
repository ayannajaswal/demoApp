import os
import zipfile
from flask import Flask, render_template, request, redirect, send_file, flash, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'supersecretkey'

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file:
        # Save the file to the uploads folder
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Compress the file to a zip
        zip_filename = f"{filename}.zip"
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(file_path, arcname=filename)

        # Render output.html after upload
        return render_template('output.html', zip_file=zip_filename)

@app.route('/download/<zip_file>')
def download_file(zip_file):
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_file)
    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
