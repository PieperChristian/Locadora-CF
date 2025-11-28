import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import bcrypt from 'bcrypt'
import { verificaToken } from './verificaToken.js'

const prisma = new PrismaClient()
const router = Router()

// === SCHEMAS DE VALIDAÇÃO (ZOD) ===

// 1. Schema para Criação de Atendente (Inclui Pergunta Secreta)
const atendenteSchema = z.object({
    nome: z.string().min(3, { message: "Nome deve ter no mínimo 3 caracteres" }),
    email: z.string().email({ message: "E-mail inválido" }),
    senha: z.string(),
    perguntaSeguranca: z.string().min(5, { message: "A pergunta de segurança é muito curta" }),
    respostaSeguranca: z.string().min(2, { message: "A resposta de segurança é muito curta" })
})

// 2. Schema para Troca de Senha (Usuário Logado)
const trocaSenhaSchema = z.object({
    senhaAtual: z.string(),
    novaSenha: z.string()
})

// 3. Schema para Recuperação de Senha (Esqueci minha senha)
const recuperaSchema = z.object({
    email: z.string().email(),
    resposta: z.string(),
    novaSenha: z.string()
})

// === FUNÇÕES AUXILIARES ===

function validaSenha(senha: string) {
    const mensa: string[] = []

    if (senha.length < 8) {
        mensa.push("Erro... senha deve possuir, no mínimo, 8 caracteres")
    }

    let pequenas = 0
    let grandes = 0
    let numeros = 0
    let simbolos = 0

    for (const letra of senha) {
        if ((/[a-z]/).test(letra)) pequenas++
        else if ((/[A-Z]/).test(letra)) grandes++
        else if ((/[0-9]/).test(letra)) numeros++
        else simbolos++
    }

    if (pequenas == 0) mensa.push("Erro... senha deve possuir letra(s) minúscula(s)")
    if (grandes == 0) mensa.push("Erro... senha deve possuir letra(s) maiúscula(s)")
    if (numeros == 0) mensa.push("Erro... senha deve possuir número(s)")
    if (simbolos == 0) mensa.push("Erro... senha deve possuir símbolo(s)")

    return mensa
}

router.get("/", async (req, res) => {
    try {
        const atendentes = await prisma.atendente.findMany({
            select: { id: true, nome: true, email: true }
        })
        res.status(200).json(atendentes)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})

router.post("/", async (req, res) => {
    const valida = atendenteSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    const { nome, email, senha, perguntaSeguranca, respostaSeguranca } = valida.data

    // Valida força da senha
    const mensaErros = validaSenha(senha)
    if (mensaErros.length > 0) {
        res.status(400).json({ erro: mensaErros })
        return
    }

    try {
        const existe = await prisma.atendente.findUnique({ where: { email } })
        if (existe) {
            res.status(400).json({ erro: "E-mail já cadastrado" })
            return
        }

        const salt = bcrypt.genSaltSync(12)

        const hashSenha = bcrypt.hashSync(senha, salt)

        const hashResposta = bcrypt.hashSync(respostaSeguranca.toLowerCase(), salt)

        const atendente = await prisma.atendente.create({
            data: {
                nome,
                email,
                senha: hashSenha,
                perguntaSeguranca,
                respostaSeguranca: hashResposta
            }
        })

        res.status(201).json({ id: atendente.id, nome: atendente.nome, email: atendente.email })
    } catch (error) {
        res.status(400).json({ error })
    }
})

router.put("/alterar-senha", verificaToken, async (req, res) => {
    const valida = trocaSenhaSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    const { senhaAtual, novaSenha } = valida.data
    const id = req.userLogadoId as number

    try {
        const atendente = await prisma.atendente.findUnique({ where: { id } })
        if (!atendente) {
            res.status(400).json({ erro: "Atendente não encontrado" })
            return
        }

        if (!bcrypt.compareSync(senhaAtual, atendente.senha)) {
            res.status(400).json({ erro: "A senha atual está incorreta" })
            return
        }

        const errosNovaSenha = validaSenha(novaSenha)
        if (errosNovaSenha.length > 0) {
            res.status(400).json({ erro: errosNovaSenha })
            return
        }

        const salt = bcrypt.genSaltSync(12)
        const hash = bcrypt.hashSync(novaSenha, salt)

        await prisma.atendente.update({
            where: { id },
            data: { senha: hash }
        })

        res.status(200).json({ mensagem: "Senha alterada com sucesso!" })

    } catch (error) {
        console.log(error)
        res.status(500).json({ erro: "Erro ao alterar senha" })
    }
})

router.post("/recuperar-senha", async (req, res) => {
    const valida = recuperaSchema.safeParse(req.body)
    if (!valida.success) { res.status(400).json({ erro: valida.error }); return }

    const { email, resposta, novaSenha } = valida.data

    try {
        const atendente = await prisma.atendente.findUnique({ where: { email } })

        if (!atendente || !atendente.respostaSeguranca) {
            res.status(400).json({ erro: "Dados inválidos ou pergunta de segurança não configurada" })
            return
        }

        if (!bcrypt.compareSync(resposta.toLowerCase(), atendente.respostaSeguranca)) {
            res.status(400).json({ erro: "Resposta de segurança incorreta" })
            return
        }

        const erros = validaSenha(novaSenha)
        if (erros.length > 0) { res.status(400).json({ erro: erros }); return }

        const salt = bcrypt.genSaltSync(12)
        const hash = bcrypt.hashSync(novaSenha, salt)

        await prisma.atendente.update({
            where: { id: atendente.id },
            data: {
                senha: hash,
                tentativasLogin: 0,
                bloqueadoAte: null
            }
        })

        res.status(200).json({ mensagem: "Senha redefinida com sucesso!" })
    } catch (error) {
        res.status(500).json({ erro: "Erro no servidor" })
    }
})

export default router