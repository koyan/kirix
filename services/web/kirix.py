from flask import Flask, jsonify, request, redirect, send_file
import base64
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PIL import Image

load_dotenv()

HTTP_HOST = os.getenv('HTTP_HOST')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

application = Flask(__name__)

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route("/")
def hello_world():
    return jsonify(hello="world")
    
@application.route("/latex")
def latex():
    form = """
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
            <script>
                nr_fields = 1;
                function add() {
                 
                    nr_fields = nr_fields + 1
                    var new_input = '<h3>Αρθρο ' + nr_fields + '</h3><input type="text" name="title_' + nr_fields + '" value="Τίτλος"><br>';
                    $('#articles').append(new_input);
                    var new_textarea = '<textarea id="text_' + nr_fields + '" name="text_' + nr_fields + '" rows="4" cols="50">Κείμενο</textarea><br>';
                    $('#articles').append(new_textarea);
                    
                    $('#nr_articles').val(nr_fields);

                }
            </script>
            <form action="/submit" method="post" target="_blank" enctype="multipart/form-data">
            <div id="articles">
                <h3>Αρθρο 1</h3>
                Φωτο κύριου άρθρου: <input type="file" id="main_image" name="main_image" accept="image/*"><br><br>
                <input type="hidden" id="nr_articles" name="nr_articles" value="1">
                <input type="text" name="title_1" value="Τίτλος"><br>
                <textarea id="text_1" name="text_1" rows="4" cols="50">Κείμενο</textarea><br>
            </div>
            <button type="button" onclick="add()">Add</button>                       
            <input type="submit" value="Create"><br>
            </form>
            """        
    
    return form

@application.route('/issue/<issue>')
def get_issue(issue):
    return send_file('issues/' + issue)

@application.route('/uploads/<imagename>')
def get_image(imagename):
    return send_file('uploads/' + imagename)

@application.route('/bullpen3d.otf')
def get_font():
    return send_file('bullpen3d.otf')
    
@application.route("/submit", methods=['POST'])
def submit():
    content_str = ""

    if request.method == 'POST':
        with open('issue_nr.txt', 'r') as file :
          issue = file.read()
          
          issue_nr = int(issue)
          issue_nr = issue_nr +1
        # Write the file out again
        with open('issue_nr.txt', 'w') as file:
          file.write(str(issue_nr))


        main_image_found = False
        if 'main_image' in request.files:
            main_image = request.files['main_image']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if main_image.filename != '':
                if main_image and allowed_file(main_image.filename):
                    filename = secure_filename(main_image.filename)
                    full_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
                    main_image.save(full_path)
                    main_image_found = True
                    
                    extension = filename.rsplit('.', 1)[1].lower()
                    
                    article_image = Image.open(full_path)
                    new_image_name = "image_" + "{:05d}".format(issue_nr) + "." + extension
                    thumbnail_path = os.path.join(application.config['UPLOAD_FOLDER'], new_image_name)
                    article_image.thumbnail([350, 350])
                    article_image.save(thumbnail_path)
                    

        first_article = True
        nr_articles = int(request.form.get("nr_articles"))
        for n in range(nr_articles):
            if first_article and main_image_found:
                content_str += f"\\begin{{window}}[2,l,\includegraphics[width=2.0in]{{{new_image_name}}},\centerline{{}}]"
            content_str += f"\n\\headline{{{request.form.get(f'title_{n+1}')}}}\n{request.form.get(f'text_{n+1}')}"
            if first_article:
                first_article = False
                if main_image_found:
                    content_str += "\\end{{window}}\n"
                content_str += "\n\\begin{multicols}{2}\n"


    with open('newspaper_template.tex', 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('CONTENT', content_str)
    filedata = filedata.replace('REPLACE_ISSUE_NUMBER', str(issue_nr))
    
    new_filename = "issue_" + "{:05d}".format(issue_nr) + ".tex"
    # Write the file out again
    with open('issues/' + new_filename, 'w') as file:
      file.write(filedata)
    
    font_file = HTTP_HOST + 'bullpen3d.otf'
    tex_file = HTTP_HOST + 'issue/' + new_filename
    
    url = 'https://www.overleaf.com/docs?snip_uri=' + tex_file + '&snip_uri=' + font_file + '&engine=xelatex'
    if (main_image_found):
        image_file = HTTP_HOST + 'uploads/' + new_image_name
        url = url+'&snip_uri='+image_file
    return redirect(url)
    