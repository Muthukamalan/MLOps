minikube start --driver=docker --cpus=max --memory=max
minikube tunnel
minikube dashboard
minikube addons enable ingress

eval $(minikube -p minikube docker-env)

`build docker images`
cd src/middleware
=>  docker build -t fastapi-server -f Dockerfile.fastapi .
cd src/modelserver
=> docker build -t model-server -f Dockerfile.model .
cd src/frontend
=> docker build -t frontend-server -f Dockerfile.nextjs .

kubectl get all
