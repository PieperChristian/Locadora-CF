# 🗃️ Dados para Teste e População

Utilize estes dados para popular seu sistema e testar as validações de segurança e regras de negócio.

## 👤 1. Atendentes (Usuários do Sistema)

**Atendente Admin (Para criar primeiro):**

* **Nome:** Administrador Sistema
* **E-mail:** <admin@locadoracf.com.br>
* **Senha Forte:** `Admin@2025`
* **Pergunta Secreta:** Qual o nome do seu primeiro pet?
* **Resposta:** Rex

**Atendente Operacional:**

* **Nome:** Ana Maria Santos
* **E-mail:** <ana.santos@locadoracf.com.br>
* **Senha Forte:** `Ana#Locadora23`
* **Pergunta:** Cidade de nascimento?
* **Resposta:** Pelotas

---

## 👥 2. Clientes

**Cliente A (Bom Pagador):**

* **Nome:** Roberto de Barros
* **CPF:** 111.222.333-44
* **E-mail:** <roberto.barros@gmail.com>
* **Telefone:** 53999887766
* **Endereço:** Av. Bento Gonçalves, 1000

**Cliente B (Empresarial):**

* **Nome:** Tech Solutions LTDA
* **CPF:** 999.888.777-66
* **E-mail:** <contato@techsolutions.com>
* **Telefone:** 5133445566
* **Endereço:** Rua das Flores, 500, Sala 2

---

## 🚗 3. Veículos (Frota)

**Veículo 1 (Econômico):**

* **Placa:** ABC1234
* **Modelo:** Fiat Uno Mille
* **Cor:** Prata
* **Ano:** 2013
* **Status Inicial:** DISPONIVEL

**Veículo 2 (Sedan):**

* **Placa:** XYZ9876
* **Modelo:** Toyota Corolla XEi
* **Cor:** Preto
* **Ano:** 2020
* **Status Inicial:** DISPONIVEL

**Veículo 3 (Em Manutenção - Teste de Bloqueio):**

* **Placa:** MAN5555
* **Modelo:** Ford Ka
* **Cor:** Branco
* **Ano:** 2018
* **Status Inicial:** EM_REPARO (Tente alugar este para testar o bloqueio!)

---

## 🧪 Cenários de Teste Sugeridos

1. **Teste de Rate Limit:** Tente logar com o e-mail da Ana e senha errada 3 vezes. Na 4ª, verifique o bloqueio de 15 min.
2. **Teste de Duplicidade:** Tente cadastrar um veículo com a placa `ABC1234` novamente.
3. **Teste de Fluxo de Locação:**
    * Alugue o `Toyota Corolla` para o `Roberto`.
    * Verifique se o status do carro mudou para ALUGADO.
    * Tente alugar o mesmo carro para a `Tech Solutions` (Deve falhar).
    * Realize a devolução.
    * Verifique se o carro voltou para DISPONIVEL.
