from flask import Flask, render_template,send_from_directory,url_for
from flask_restful import Resource, Api, reqparse
from flask_uploads import UploadSet,IMAGES,configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from roboflow import Roboflow
from werkzeug.utils import secure_filename
from waitress import serve
app = Flask(__name__)
app.config['UPLOAD_PHOTOS_DEST']='uploads'

photos = UploadSet('photos',IMAGES)
api = Api(app)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
        FileAllowed(photos,"only images are allowed"),
        FileRequired("File should not be empty")
        ])
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)


@app.route('/', methods =['GET','POST'])
def upload_form():
    form = UploadForm
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file',filename=filename)
        # load the model
        rf = Roboflow(api_key="nDHiyB2cy2bkE6DoVYm9")
        project = rf.workspace("school-oxayw").project("shoe-classifier")
        model = project.version(3).model
        # infer on a local image
        print(model.predict('/uploads/'+filename).json())
        
    else:
        file_url = None
    
    return render_template('index.html',form = form,file_url=file_url)

def create_app():
   return app

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
    serve(app, host="0.0.0.0", port=8080)