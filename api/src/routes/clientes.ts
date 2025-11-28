import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import { verificaToken } from './verificaToken.js'

const prisma = new PrismaClient()
const router = Router()

// Aplica o middleware de segurança em TODAS as rotas de clientes
router.use(verificaToken)

// Schema de Validação
const clienteSchema = z.object({
    nome: z.string().min(3, { message: "Nome deve ter no mínimo 3 caracteres" }),
    cpf: z.string().length(14, { message: "CPF deve ter 14 caracteres (000.000.000-00)" }),
    email: z.string().email({ message: "E-mail inválido" }),
    telefone: z.string().min(10, { message: "Telefone deve ter no mínimo 10 caracteres" }),
    endereco: z.string().min(5, { message: "Endereço deve ter no mínimo 5 caracteres" })
})

// === LISTAGEM (R) ===
router.get("/", async (req, res) => {
    try {
        const clientes = await prisma.cliente.findMany({
            orderBy: { nome: 'asc' }
        })
        res.status(200).json(clientes)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})

// === INCLUSÃO (C) ===
router.post("/", async (req, res) => {
    const valida = clienteSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    const { nome, cpf, email, telefone, endereco } = valida.data

    try {
        // Verifica duplicidade de CPF ou E-mail
        const existe = await prisma.cliente.findFirst({
            where: {
                OR: [
                    { cpf: cpf },
                    { email: email }
                ]
            }
        })

        if (existe) {
            res.status(400).json({ erro: "CPF ou E-mail já cadastrado no sistema" })
            return
        }

        const cliente = await prisma.cliente.create({
            data: { nome, cpf, email, telefone, endereco }
        })

        res.status(201).json(cliente)
    } catch (error) {
        res.status(400).json({ error })
    }
})

// === ALTERAÇÃO (U) ===
router.put("/:id", async (req, res) => {
    const { id } = req.params

    const valida = clienteSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    try {
        const cliente = await prisma.cliente.update({
            where: { id: Number(id) },
            data: valida.data
        })
        res.status(200).json(cliente)
    } catch (error) {
        res.status(400).json({ erro: "Erro ao alterar cliente (verifique se CPF/Email já existem)" })
    }
})

// === EXCLUSÃO (D) ===
router.delete("/:id", async (req, res) => {
    const { id } = req.params

    try {
        // Verifica se cliente possui aluguéis antes de excluir (Integridade Referencial)
        const possuiAluguel = await prisma.aluguel.findFirst({
            where: { clienteId: Number(id) }
        })

        if (possuiAluguel) {
            res.status(400).json({ erro: "Não é possível excluir: Cliente possui histórico de aluguéis." })
            return
        }

        const cliente = await prisma.cliente.delete({
            where: { id: Number(id) }
        })
        res.status(200).json(cliente)
    } catch (error) {
        res.status(400).json({ erro: "Cliente não encontrado ou erro no servidor" })
    }
})

export default router