FROM python:3.9-slim
LABEL maintainer="Muthu kamalan(muthukamalan98@gmail.com)"


# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=True

# Don't write byte code __pycache__/
ENV PYTHONDONTWRITEBYTECODE=True

# Keep src files
WORKDIR /workspace

# Add requirements
COPY requirements.txt /workspace/

# torch cpu version 
RUN python3 -m pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision  

COPY train.py /workspace/

##FIXME:: TODO
# pip install --no-cache-dir -r requirements.txt  (need build-essential)

##install core dependencies <apt-get>
# RUN apt-get update && apt-get install -y libpq-dev build-essential git && apt autoclean && apt autoremove

##upgrade pip
# RUN pip install --upgrade pip

##install production dependencies.
# RUN python -m  pip install --no-cache-dir -r requirements.txt

CMD ["python", "train.py"]