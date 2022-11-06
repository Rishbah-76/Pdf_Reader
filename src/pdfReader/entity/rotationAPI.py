import os
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from pdfReader.utils.common import read_yaml
from pdfReader import logger
from pdfReader.entity.pdfRotation import Rotatepdf
#reading the config file
config=read_yaml(Path("config.yaml"))

from flask import send_from_directory



UPLOAD_FOLDER = config.upload_folder.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = config.allowed_extensions.ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logger.info("File saved successfully")
            return redirect(url_for('rotatepdffile', filename=filename))
            #return redirect(url_for('download_file', name=filename))
        
            
    return render_template('index.html')


@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/process', methods=['GET' , 'POST' ])
def rotatepdffile():
    pdf=Rotatepdf()
    logger.info("Pdf object created")
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    logger.info(files)
    if request.method == 'POST':
        logger.info("POST REQUEST VERIFIED")
       # getting input with name = fname in HTML form
        all_pages = request.form.get("all")
        specific_page_value = request.form.get("specific")
        list_of_page_value= request.form.get("lst")
        degree_of_rotation= int(request.form.get("deg"))
        if all_pages =='True' and (specific_page_value=='None' and list_of_page_value=='None'):
            func1=pdf.all(deg_of_rotation=degree_of_rotation,filepath=os.path.join(app.config['UPLOAD_FOLDER'], files[0]))
            # logger.info(str(func1[0]))
            # logger.info(type(func1[1]))
            # logger.info(type(func1[2]))
            output={'file_path':str(func1[0]),'angle_of_rotation':str((func1[1])),'page_number':func1[2]}
            return jsonify(output)

        
        if specific_page_value !="None" and (list_of_page_value =="None" and all_pages !='True'):
            logger.info("no empty")
            func2=pdf.specific_page(page_No=int(specific_page_value),deg_of_rotation=degree_of_rotation,filepath=os.path.join(app.config['UPLOAD_FOLDER'], files[0]))
            # logger.info(str(func1[0]))
            # logger.info(type(func1[1]))
            # logger.info(type(func1[2]))
            output={'file_path':str(func2[0]),'angle_of_rotation':str((func2[1])),'page_number':func2[2]}
            return jsonify(output)

        if list_of_page_value !="None" and (specific_page_value =="None" and all_pages !='True'):
            logger.info("no empty")
            logger.info(list_of_page_value)
            func3=pdf.list_of_pages(page_No=list_of_page_value,deg_of_rotation=degree_of_rotation,filepath=os.path.join(app.config['UPLOAD_FOLDER'], files[0]))
            # logger.info(str(func1[0]))
            # logger.info(type(func1[1]))
            # logger.info(type(func1[2]))
            output={'file_path':str(func3[0]),'angle_of_rotation':str((func3[1])),'page_number':func3[2]}
            return jsonify(output)

        if list_of_page_value =="None" and specific_page_value =="None" and all_pages !='True':
            return render_template("pdf.html")

    return render_template("pdf.html")

if __name__ == '__main__':
   app.run(debug = True)
