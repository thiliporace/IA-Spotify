# 1. Especificar uma imagem base do Python
FROM python:3.10-slim

# 2. Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copiar todos os arquivos do projeto para o contêiner
COPY . .

# 4. Instalar dependências, caso estejam listadas (opcional)
RUN pip install -r requirements.txt

# 5. Configurar variáveis de ambiente (caso precise do arquivo variables.env)
ENV $(cat variables.env | xargs)

# 6. Expor a porta, se o seu script precisar se comunicar externamente
# EXPOSE 5000  # Descomente e ajuste a porta se necessário

# 7. Executar o script principal
CMD ["python", "teste.py"]