# Imagem base leve do Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para limpeza de tela
# (ncurses é útil para bibliotecas de terminal rico)
RUN apt-get update && apt-get install -y ncurses-bin && rm -rf /var/lib/apt/lists/*

# Instala as bibliotecas do projeto diretamente
RUN pip install requests rich pwinput

# Copia o código fonte
COPY . .

# Define a variável de ambiente para limpar o buffer do Python (logs imediatos)
ENV PYTHONUNBUFFERED=1

# Comando padrão
CMD ["python", "controle.py"]