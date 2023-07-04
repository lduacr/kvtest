FROM python:3.10

RUN apt-get update && apt-get install -y vim net-tools
RUN pip install falcon gunicorn
RUN pip install azure-keyvault-secrets azure-identity
RUN pip install logzero

ADD ./ /project
WORKDIR /project

EXPOSE 8000

# CMD gunicorn --certfile=certificate.crt --keyfile=private.key -w 3 -b 0.0.0.0:8000 k8sapp:app
CMD gunicorn -w 3 -b 0.0.0.0:8000 k8sapp:app

