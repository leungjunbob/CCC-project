FROM python:3.8.10

WORKDIR /frontend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user

COPY . .

ENV NOTEBOOK_DIR=/frontend
WORKDIR ${NOTEBOOK_DIR}

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
