# 🔌 Locadora CF - API (Backend)

API RESTful desenvolvida em **Node.js** com **TypeScript**, responsável por toda a regra de negócio, persistência de dados e segurança do sistema Locadora CF.

## 🛠 Tecnologias & Ferramentas

- **Runtime:** Node.js
- **Linguagem:** TypeScript
- **Framework:** Express.js
- **ORM:** Prisma (MySQL)
- **Validação:** Zod
- **Segurança:** JWT (Json Web Token) & Bcrypt
- **Logs:** Implementação personalizada de auditoria no banco.

## ✨ Funcionalidades Principais

- **Autenticação Segura:** Login com validação de senha (hash) e emissão de tokens JWT.
- **Controle de Acesso:** Middleware `verificaToken` protege rotas sensíveis.
- **CRUD Completo:** Gerenciamento de Atendentes, Clientes e Veículos.
- **Regras de Negócio:**
  - Validação de CPF e Placas.
  - Controle de status de veículos (Disponível/Alugado).
  - Bloqueio de exclusão para veículos com histórico.
- **Soft Delete:** Veículos não são apagados fisicamente, mantendo integridade histórica.
- **Segurança Avançada:** Proteção contra força bruta (bloqueio temporário de usuário).

## ⚙️ Configuração e Instalação

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz da pasta `api` com o seguinte conteúdo:

```env
# Conexão com o Banco de Dados (MySQL)
DATABASE_URL="mysql://usuario:senha@localhost:3306/locadora_cf"

# Chave Secreta para assinatura do JWT
JWT_KEY="SuaChaveSuperSecretaAqui"

# Configurações de E-mail (Opcional - Mailtrap)
MAILTRAP_EMAIL="seu_usuario"
MAILTRAP_SENHA="sua_senha"
```

### 2. Instalação de Dependências

```bash
npm install
```

### 3. Banco de Dados (Prisma)

Gere as tabelas no banco de dados MySQL:

```bash
npx prisma migrate dev --name init
``` prisma migrate dev --name init
### 4. Executando o Servidor

Para rodar em modo de desenvolvimento (com hot-reload):

```bash
npm run dev
```bash
npm run dev
```

*O servidor iniciará na porta **3000**.*

## 🛣️ Endpoints Principais

| Método | Rota | Descrição | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/login` | Autentica um atendente e retorna Token. | ❌ |
| `GET` | `/veiculos` | Lista toda a frota. | ✅ |
| `POST` | `/veiculos` | Cadastra um novo veículo. | ✅ |
| `POST` | `/alugueis` | Realiza a locação de um veículo. | ✅ |
| `PUT` | `/alugueis/devolucao/:id` | Registra a devolução e libera o carro. | ✅ |
| `GET` | `/clientes` | Lista clientes cadastrados. | ✅ |

---

## 🔒 Segurança

A API implementa **Rate Limiting** e bloqueio de conta após 3 tentativas falhas de login consecutivas, protegendo contra ataques de força bruta.
