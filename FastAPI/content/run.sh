docker build -t johnsnowlabs/sparknlp:sparknlp_api .
docker run -p 8515:8515 -it johnsnowlabs/sparknlp:sparknlp_api
