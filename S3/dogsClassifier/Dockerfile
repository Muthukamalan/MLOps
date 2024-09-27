FROM  python:3.9-slim 
LABEL maintainer="Muthu kamalan(muthukamalan98@gmail.com)"


# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=True

# Don't write byte code __pycache__/
ENV PYTHONDONTWRITEBYTECODE=True

WORKDIR /app 

COPY requirement.txt /app/
RUN pip install -r requirement.txt

COPY . .

CMD [ "python","train.py" ]
