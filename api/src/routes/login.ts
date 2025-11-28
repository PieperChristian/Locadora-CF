import { PrismaClient } from "@prisma/client"
import { Router } from "express"
import bcrypt from 'bcrypt'
import jwt from 'jsonwebtoken'
import { registrarLog } from "../utils/logger.js"

const prisma = new PrismaClient()
const router = Router()

router.post("/", async (req, res) => {
    const { email, senha } = req.body
    const mensaPadrao = "Login ou senha incorretos" // Mensagem genérica por segurança

    if (!email || !senha) {
        res.status(400).json({ erro: mensaPadrao })
        return
    }

    try {
        const atendente = await prisma.atendente.findUnique({ where: { email } })

        if (!atendente) {
            res.status(400).json({ erro: mensaPadrao })
            return
        }

        // 1. Verifica Bloqueio
        if (atendente.bloqueadoAte && new Date() < atendente.bloqueadoAte) {
            const tempoRestante = Math.ceil((atendente.bloqueadoAte.getTime() - new Date().getTime()) / 60000)
            res.status(403).json({ erro: `Usuário bloqueado. Tente novamente em ${tempoRestante} minutos.` })
            return
        }

        // 2. Valida Senha
        if (bcrypt.compareSync(senha, atendente.senha)) {
            // SUCESSO: Zera contador e libera token
            await prisma.atendente.update({
                where: { id: atendente.id },
                data: { tentativasLogin: 0, bloqueadoAte: null }
            })

            const token = jwt.sign({
                userLogadoId: atendente.id,
                userLogadoNome: atendente.nome
            },
                process.env.JWT_KEY as string,
                { expiresIn: "1h" }
            )

            await registrarLog(atendente.id, "Realizou login no sistema")

            res.status(200).json({
                id: atendente.id,
                nome: atendente.nome,
                email: atendente.email,
                token
            })
        } else {
            // FALHA: Incrementa contador e verifica limite
            const novasTentativas = atendente.tentativasLogin + 1
            let dadosAtualizacao: any = { tentativasLogin: novasTentativas }
            let msgExtra = ""

            if (novasTentativas >= 3) {
                // Bloqueia por 15 minutos
                const dataDesbloqueio = new Date()
                dataDesbloqueio.setMinutes(dataDesbloqueio.getMinutes() + 15)
                dadosAtualizacao.bloqueadoAte = dataDesbloqueio
                msgExtra = " Usuário BLOQUEADO por excesso de tentativas."
            }

            await prisma.atendente.update({
                where: { id: atendente.id },
                data: dadosAtualizacao
            })

            await registrarLog(atendente.id, `Tentativa de login falha (${novasTentativas}/3).${msgExtra}`)
            res.status(400).json({ erro: mensaPadrao })
        }
    } catch (error) {
        res.status(500).json(error)
    }
})

export default router