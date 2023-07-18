from flask import Flask, jsonify, request, redirect, send_file
import base64
import os
from dotenv import load_dotenv

load_dotenv()

HTTP_HOST = os.getenv('HTTP_HOST')

application = Flask(__name__)

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
            <form action="/submit" method="post" target="_blank">
            <div id="articles">
                <h3>Αρθρο 1</h3>
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

@application.route('/bullpen3d.otf')
def get_font():
    return send_file('bullpen3d.otf')
    
@application.route("/submit", methods=['POST'])
def submit():
    title_1 = 'Uknown'
    text_1 = 'Uknown'
    
    if request.method == 'POST':
        title_1 = request.form.get('title_1')
        text_1 = request.form.get('text_1')    

    with open('issue_nr.txt', 'r') as file :
      issue = file.read()
      
      issue_nr = int(issue)
      issue_nr = issue_nr +1
    # Write the file out again
    with open('issue_nr.txt', 'w') as file:
      file.write(str(issue_nr))


    with open('newspaper_template.tex', 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('TITLE_OF_ARTICLE_1', title_1)
    filedata = filedata.replace('TEXT_OF_ARTICLE_1', text_1)
    
    new_filename = "issue_" + "{:05d}".format(issue_nr) + ".tex"
    # Write the file out again
    with open('issues/' + new_filename, 'w') as file:
      file.write(filedata)
    
    font_file = HTTP_HOST + 'bullpen3d.otf'
    tex_file = HTTP_HOST + 'issue/' + new_filename
    
    url = 'https://www.overleaf.com/docs?snip_uri=' + tex_file + '&snip_uri=' + font_file + '&engine=xelatex'
    return redirect(url)
    #return 'done'