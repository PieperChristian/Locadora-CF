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
```

### 4. Executando o Servidor

Para rodar em modo de desenvolvimento (com hot-reload):

```bash
npm run dev
```

*O servidor iniciará na porta **3000**.*

## 📚 Documentação da API

### 🔐 Autenticação

| Método | Rota | Descrição | Auth | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/login` | Realiza login e retorna Token JWT. | ❌ | `{ "email": "...", "senha": "..." }` |

### 🧑‍💼 Atendentes

| Método | Rota | Descrição | Auth | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/atendentes` | Lista todos os atendentes (ID, Nome, Email). | ❌ | - |
| `POST` | `/atendentes` | Cadastra novo atendente. | ❌ | `{ "nome": "...", "email": "...", "senha": "...", "perguntaSeguranca": "...", "respostaSeguranca": "..." }` |
| `PUT` | `/atendentes/alterar-senha` | Altera senha do usuário logado. | ✅ | `{ "senhaAtual": "...", "novaSenha": "..." }` |
| `POST` | `/atendentes/recuperar-senha` | Redefine senha via pergunta de segurança. | ❌ | `{ "email": "...", "resposta": "...", "novaSenha": "..." }` |

### 🚗 Veículos

| Método | Rota | Descrição | Auth | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/veiculos` | Lista frota ativa (exclui deletados). | ✅ | - |
| `POST` | `/veiculos` | Cadastra novo veículo. | ✅ | `{ "placa": "ABC1234", "modelo": "...", "cor": "...", "ano": 2023, "status": "DISPONIVEL" }` |
| `PUT` | `/veiculos/:id` | Atualiza dados do veículo. | ✅ | `{ "placa": "...", "modelo": "...", ... }` |
| `DELETE` | `/veiculos/:id` | Remove veículo (Soft Delete). | ✅ | - |

### 👥 Clientes

| Método | Rota | Descrição | Auth | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/clientes` | Lista todos os clientes. | ✅ | - |
| `POST` | `/clientes` | Cadastra novo cliente. | ✅ | `{ "nome": "...", "cpf": "000.000.000-00", "email": "...", "telefone": "...", "endereco": "..." }` |
| `PUT` | `/clientes/:id` | Atualiza dados do cliente. | ✅ | `{ "nome": "...", ... }` |
| `DELETE` | `/clientes/:id` | Remove cliente (se não tiver aluguéis). | ✅ | - |

### 🔑 Aluguéis

| Método | Rota | Descrição | Auth | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/alugueis` | Lista histórico de locações. | ✅ | - |
| `POST` | `/alugueis` | Registra nova locação. | ✅ | `{ "clienteId": 1, "veiculoId": 1 }` |
| `PUT` | `/alugueis/devolucao/:id` | Finaliza locação (Devolução). | ✅ | - |
| `DELETE` | `/alugueis/:id` | Remove registro de aluguel. | ✅ | - |

### ⚙️ Sistema

| Método | Rota | Descrição | Auth | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/sistema/backup` | Baixa backup completo (JSON). | ✅ | - |
| `POST` | `/sistema/restore` | Restaura banco de dados via JSON. | ✅ | `{ "atendentes": [...], "clientes": [...], ... }` |
| `GET` | `/sistema/logs` | Lista os últimos 50 logs de auditoria. | ✅ | - |

## 🧪 Testes com Insomnia / Postman

Para facilitar os testes, configure uma variável de ambiente no seu cliente HTTP (Insomnia/Postman) chamada `base_url` com o valor `http://localhost:3000`.

### Lista de Endpoints (Copiar e Colar)

**Autenticação**
- `POST {{base_url}}/login`

**Atendentes**
- `GET {{base_url}}/atendentes`
- `POST {{base_url}}/atendentes`
- `PUT {{base_url}}/atendentes/alterar-senha`
- `POST {{base_url}}/atendentes/recuperar-senha`

**Veículos**
- `GET {{base_url}}/veiculos`
- `POST {{base_url}}/veiculos`
- `PUT {{base_url}}/veiculos/1` (Substitua '1' pelo ID desejado)
- `DELETE {{base_url}}/veiculos/1`

**Clientes**
- `GET {{base_url}}/clientes`
- `POST {{base_url}}/clientes`
- `PUT {{base_url}}/clientes/1`
- `DELETE {{base_url}}/clientes/1`

**Aluguéis**
- `GET {{base_url}}/alugueis`
- `POST {{base_url}}/alugueis`
- `PUT {{base_url}}/alugueis/devolucao/1`
- `DELETE {{base_url}}/alugueis/1`

**Sistema**
- `GET {{base_url}}/sistema/backup`
- `POST {{base_url}}/sistema/restore`
- `GET {{base_url}}/sistema/logs`

---

## 🔒 Segurança

A API implementa **Rate Limiting** e bloqueio de conta após 3 tentativas falhas de login consecutivas, protegendo contra ataques de força bruta.
