# Image select
FROM python:3.7-alpine3.7
# Change image contains depend on this value 
# "/app/" is deafult value at build time
ARG project_dir=/app/
WORKDIR $project_dir
# execute at "docker build"
RUN pip install flask
# execute at "docker run"
# CMD ["python", "main.py"]
