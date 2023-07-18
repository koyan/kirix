from flask import Flask, jsonify, request, redirect
import base64

application = Flask(__name__)

@application.route("/")
def hello_world():
    return jsonify(hello="world")
    
@application.route("/latex")
def latex():
    form = """
            <form action="/submit" method="post" target="_blank">
            <input type="text" name="title_1" value="My title 1"><br>
            <input type="text" name="text_1" value="My text goes here"><br>
            <input type="submit" value="creatre">
            </form>
            """        
    
    return form
    
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
    
    new_filename = "issues/issue_" + "{:05d}".format(issue_nr) + ".tex"
    # Write the file out again
    with open(new_filename, 'w') as file:
      file.write(filedata)
    
    url = 'https://www.overleaf.com/docs?snip_uri=' + new_filename
    return redirect(url)
    #return 'done'