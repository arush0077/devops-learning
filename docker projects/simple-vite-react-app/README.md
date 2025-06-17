# What to do?

docker build -t test-app .
docker run -p 3000:5173 --name test-app test-app
run this to make it working and go to localhost:3000 in your browser 
and remove by 
docker rm -f test-app


