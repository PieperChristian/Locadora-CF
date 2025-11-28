# 🚗 Locadora de Veículos CF - Sistema de Gestão Integrado

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

Bem-vindo ao **Locadora CF**, uma solução Fullstack robusta para gestão de locadoras de veículos. Este projeto adota uma arquitetura de **Monorepo**, separando claramente as responsabilidades entre uma API RESTful performática e um Cliente CLI interativo.

---

## 🏗 Arquitetura do Projeto

O sistema é dividido em dois módulos principais:

| Módulo | Diretório | Tecnologia | Descrição |
| :--- | :--- | :--- | :--- |
| **Backend** | `/api` | Node.js + TypeScript | API REST, Regras de Negócio, Prisma ORM, MySQL. |
| **Frontend** | `/sistema` | Python 3.12+ | Interface de Linha de Comando (TUI) rica e interativa. |

### 📂 Estrutura de Diretórios

```bash
LocadoraCF/
├── api/                # Backend (Servidor)
│   ├── prisma/         # Schema do Banco de Dados e Migrations
│   └── src/            # Código fonte (Controllers, Routes, Services)
├── sistema/            # Frontend (Cliente)
│   ├── cadastros/      # Módulos de CRUD
│   ├── graficos/       # Geração de Dashboards ASCII
│   └── locacoes/       # Lógica de Aluguéis
└── docker-compose.yml  # Orquestração dos containers
```

---

## 🚀 Como Executar (Quick Start)

A maneira mais fácil de rodar o projeto é utilizando **Docker**. Isso configura o Banco de Dados, a API e prepara o ambiente do Cliente automaticamente.

### Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados.

### Passo a Passo

1. **Suba a infraestrutura (Banco de Dados + API):**

   ```bash
   docker-compose up -d
   ```

2. **Execute o Sistema (Cliente Python):**

   *Aguarde alguns instantes para o MySQL inicializar e a API conectar.*
2. **Execute o Sistema (Cliente Python):**
   Para interagir com o sistema, execute o container do cliente em modo interativo:

   ```bash
   docker-compose run --rm sistema
   ```ker-compose run --rm sistema
   ```

3. **Parar a execução:**

   ```bash
   docker-compose down
   ```ker-compose down
   ```

---

## 🛠 Execução Manual (Desenvolvimento)

Caso queira rodar localmente sem Docker, siga os passos abaixo.
**Pré-requisitos:**

- Node.js (v18 ou superior)
- Node.js (v18 ou superior)
- Python (v3.10 ou superior)
- MySQL rodando localmente

### 1. Banco de Dados

Certifique-se de ter um servidor MySQL rodando e crie um banco de dados vazio:

```sql
CREATE DATABASE locadora_cf;
### 2. API (Backend)

```bash
cd api API (Backend)
```bash
cd api
# Configure o arquivo .env (copie do exemplo ou veja api/README.md)
npm install
npx prisma migrate dev
npm run dev
```

### 3. Sistema (Frontend)

Em um novo terminal:

```bash
cd sistema
cd sistema
python -m venv venv

# Ativar venv (Windows)
venv\Scripts\activate
# Ativar venv (Mac/Linux)
source venv/bin/activate

pip install -r requirements.txt
# Caso não tenha o arquivo requirements.txt:
# pip install requests rich pwinput

python controle.py
```

---

## 👤 Autor

Desenvolvido por **Christian Pieper** como trabalho avaliativo em Desenvolvimento de APi's e Algorítimos e Estruturas de Dados.
