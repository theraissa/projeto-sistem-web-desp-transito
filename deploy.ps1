Write-Host "Parando e removendo containers, redes e volumes antigos..."
docker-compose down -v

Write-Host "Buildando imagens..."
docker-compose build

Write-Host "Subindo containers..."
docker-compose up -d

Write-Host "Deploy concluído com sucesso!"
docker-compose ps
