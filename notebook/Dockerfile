FROM python:3.6-jessie

#install python
COPY requirements.txt /
RUN pip install -r /requirements.txt

CMD ["jupyter", "notebook", "--NotebookApp.token='user'", "--ip=0.0.0.0", "--allow-root"]