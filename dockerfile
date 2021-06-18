FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade cython
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# copy all the files to the container
COPY . .

# run test
#RUN sh run_tests.sh

# run setup
RUN sh setup.sh

# tell the port number the container should expose
# EXPOSE 5000

ENV environment=live

# run the command
CMD ["python", "./index.py"]
