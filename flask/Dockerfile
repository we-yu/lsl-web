# Image select
FROM python:3.7-alpine3.7
# FROM nikolaik/python-nodejs
# Change image contains depend on this value
# "/app/" is deafult value at build time
ARG project_dir=/app/
WORKDIR $project_dir
# execute at "docker build"
#RUN npm i -S sqlite3
# RUN npm install -g express \
#                     express-generator
#RUN npm install sqlite3 --save
RUN apk --no-cache add --virtual=addpacks curl vim
RUN apk del addpacks
RUN apk info

RUN pip install --upgrade pip
RUN pip install flask \
                mysql-connector-python \
                pymongo \
                requests \
                bs4
# execute at "docker run"
CMD ["python", "frame_app.py"]
# ABCDEF