# Imagem base leve do Node.js
FROM node:18-alpine

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência
COPY package*.json ./
COPY prisma ./prisma/

# Instala dependências
RUN npm install

# Gera o cliente do Prisma (Tipagem)
RUN npx prisma generate

# Copia o restante do código
COPY . .

# Expõe a porta da API
EXPOSE 3000

# Comando padrão (será sobrescrito pelo compose para rodar migrations antes)
CMD ["npm", "run", "dev"]