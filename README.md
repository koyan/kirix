# kirix

A python web app that collects article titles and text and produces a pdf based on a latex newspaper template

# Requirements

1) A free account at https://www.overleaf.com/

# Tech stack

1) Python, flask
1) Docker (optional, for development)
1) Latex (for templating). Nothing to install, just knowledge of how latex works for templating.

# Development

1) Have docker installed and running
1) Copy the `services/web/.env.example` to `services/web/.env`
1) `docker-compose build`
1) `docker-compose up`
1) Go to `http://localhost:5001/latex`
1) Fill in the form (click `add` to add more articles, and `create` to create the newspaper)
1) An issue must have been added in the `services/web/issues` directory as `issue_XXXXX.tex`
1) If you added an image, it must have been added to the `services/web/uploads` directory as `image_XXXXX.YYY`
1) In overleaf create a new project, and upload the `issue_XXXXX.tex`, the `image_XXXXX.YYY`, and the `bullpen3d.otf` font
1) In overleaf, click `Generate`

#  Production

(Always depending on your environment:)

1) `git clone https://github.com/koyan/kirix`
1) `cd kirix/services/web/`
1) `mkdir issues`
1) `mkdir uploads`
1) `echo "0" > issue_nr.txt`
1) `cp services/web/.env.example services/web/.env`
1) With the editor of your choise edit the `.env` and put the correct values for `HTTP_HOST` and `UPLOAD_FOLDER`
1) Set up nginx, python, virtualenv and flask and run the application. (Example instructions at: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-centos-7 ) 

# Usage: 

1) Log in overleaf
1) Go to `https://myserver.com/latex` 
1) Fill in the form
1) Click `Generate`
