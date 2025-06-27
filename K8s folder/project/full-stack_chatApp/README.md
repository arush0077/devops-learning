### Enable Ingress in Minikube
- minikube addons enable ingress

###  What TO DO ?
- cd ./k8s 
- kubectl apply -f .\namespace.yml -f .\mongodb-pv.yml -f .\mongodb-pvc.yml -f secret.yml -f config-map.yml -f .

### Access the application using Ingress
- kubectl port-forward svc/ingress-nginx-controller -n ingress-nginx 8080:80 --address=0.0.0.0

### check localhost:8080 for your chat app hurray
- App UI is available at http://localhost:8080



### to remove all run 
- kubectl delete ns chat-app
- kubectl delete pv mongodb-pv