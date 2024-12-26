docker build excel_agent/ -t latest
docker run -p 8080:8080 --env-file ./env.local.list latest