# A simple cloned notes app

## Run 
- cd ./k8s
- kubectl apply -f ./ns.yml -f .
- kubectl get pods -n notes-app [wait till all shows running]

## Keep Terminal On
- kubectl port-forward svc/ingress-nginx-controller 8080:80 -n ingress-nginx --address=0.0.0.0 # [keep terminal running]

# on localhost:8080 -> notes-app
# on localhost:8080/nginx -> nginx-app

- kubectl delete ns notes-app

