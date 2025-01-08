Prerequisite:
- run successful locally 
- run successful docker

*local*
```shell
pip install -r requirements.txt
python main.py
```
*docker*
```shell
docker build -t USERNAME/kclassify_dogbreeds:latest -f Dockerfile .
docker login
docker push USERNAME/kclassify_dogbreeds:latest

docker run --rm -it -p8080:8080 USERNAME/kclassify_dogbreeds:latest

for i in {1..15}; do curl http://localhost:8080/health; done | awk '{gsub(/}{/, "}\n{")}1'
docker image rm USERNAME/kclassify_dogbreeds:latest
```

*minikube*
```shell
minikube start --driver=docker
alias mkubectl='minikube kubectl --'


mkubectl config set-context --current --namespace=default # stick with default namespace

minikube tunnel &
minikube dashboard &

mkubectl create -f classifier.yaml

for i in {1..35}; do curl http://earth.localhost/health; done | awk '{gsub(/}{/, "}\n{")}1'

# get all logs
mkubectl delete -f classifier.yaml
```


# Expose to Earth
```bash
ssh -R 80:earth.localhost:80 nokey@localhost.run
```
