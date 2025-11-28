# 🖥️ Locadora CF - Sistema (Frontend CLI)

Interface de Linha de Comando (CLI) moderna e interativa desenvolvida em **Python**, que atua como cliente para a API da Locadora CF.

## 🎨 Destaques Visuais

O sistema utiliza a biblioteca **Rich** para proporcionar uma experiência de usuário (UX) superior no terminal:

- **Tabelas Formatadas:** Exibição clara de dados.
- **Painéis e Cores:** Interface organizada e visualmente agradável.
- **Inputs Mascarados:** Senhas ocultas (`****`) com `pwinput`.
- **Gráficos ASCII:** Visualização de dados gerenciais diretamente no console.

## 📦 Estrutura do Módulo

```bash
sistema/
├── autenticacao.py     # Lógica de Login e Gestão de Sessão
├── controle.py         # Ponto de Entrada (Menu Principal)
├── cadastros/          # Módulos de CRUD (Clientes, Veículos)
├── locacoes/           # Processos de Aluguel e Devolução
├── graficos/           # Geração de Dashboards
├── pesquisas/          # Filtros avançados
└── utilitarios/        # Backup, Restore e Configurações
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior.
- API da Locadora rodando (localmente ou via Docker).

### 1. Configuração do Ambiente Virtual (Recomendado)

Para evitar conflitos de bibliotecas, crie um ambiente virtual:

**Windows:**

```bash
python -m venv venv
python -m venv venv
venv\Scripts\activate
**Linux/Mac:**

```bash
python3 -m venv venv
```bash
python3 -m venv venv
### 2. Instalação das Dependências

```bash
pip install requests rich pwinput
``` 2. Instalação das Dependências
```bash
pip install requests rich pwinput
### 3. Executando o Sistema

```bash
python controle.py
```bash
python controle.py
```

## 📊 Funcionalidades do Cliente

1. **Gestão de Clientes:** Cadastro completo, listagem e edição.
2. **Gestão de Veículos:** Controle de frota, alteração de status e filtros por modelo/ano.
3. **Locações:**
   - **Retirada:** Associa um carro disponível a um cliente.
   - **Devolução:** Calcula o tempo de uso e libera o veículo.
4. **Relatórios:**
   - Gráficos de barras mostrando a frota por status.
   - Histórico de locações por período.
5. **Administração:**
   - Backup dos dados da API (salvo localmente em JSON).
   - Alteração de senha do usuário logado.

## ⚠️ Notas Importantes

- O sistema se comunica com a API via `http://localhost:3000`. Certifique-se de que a API está online.
- O diretório `__pycache__` e arquivos de backup são ignorados pelo Git para manter o repositório limpo.
