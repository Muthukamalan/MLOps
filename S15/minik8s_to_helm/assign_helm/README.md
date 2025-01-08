`
make sure all namespace aligned and build Images
`
```bash
eval $(minikube -p minikube docker-env)

cd src/frontend &&  docker build -t ui-server:latest -f Dockerfile.nextjs .

cd src/middleware && docker build -t fastapi-server:latest -f Dockerfile.fastapi .

cd src/modelserver && docker build -t model-server:latest -f Dockerfile.model .

eval $(minikube docker-env -u) 


# check in minikube 
minikube ssh
docker image ls | grep -Ei 'ui-|fastapi-|model-|redis'
```

- switch different ns
```bash
mkubectl config set-context --current --namespace=default
```

```bash
helm create helmdogs

# move all files to templates and respective changes wrt values

helm lint helmdogs/
mkubectl get all -A
helm install prod-release helmdogs --values helmdogs/values.yaml -f helmdogs/values-prod.yaml 

helm install local-release helmdogs --values helmdogs/values.yaml -f helmdogs/values-dev.yaml 

kubectl port-forward service/frontend-service  8080:80 -n prod
curl localhost:8080/



ssh -R 80:localhost:8080 nokey@localhost.run
```
