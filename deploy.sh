CONTAINER_NAME="front-container"
IMAGE_NAME="interfaces-basicas"

echo "Parando o container atual..."
docker stop $CONTAINER_NAME

echo "Removendo o container atual..."
docker rm $CONTAINER_NAME

echo "Fazendo build da nova imagem..."
docker build -t $IMAGE_NAME .

echo "Subindo o container com a nova imagem..."
docker run -d -p 8080:80 --name $CONTAINER_NAME $IMAGE_NAME

echo "Deploy concluído com sucesso! Acesse: http://localhost:8080"
