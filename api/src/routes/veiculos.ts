import { PrismaClient, StatusVeiculo } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import { verificaToken } from './verificaToken.js'

const prisma = new PrismaClient()
const router = Router()

// Proteção total das rotas
router.use(verificaToken)

// Schema de Validação
const veiculoSchema = z.object({
    placa: z.string().length(7, { message: "Placa deve ter exatamente 7 caracteres (sem traço)" }).toUpperCase(),
    modelo: z.string().min(2, { message: "Modelo deve ter no mínimo 2 caracteres" }),
    cor: z.string().min(2, { message: "Cor inválida" }),
    ano: z.number().int().min(1900).max(new Date().getFullYear() + 1),
    status: z.nativeEnum(StatusVeiculo).optional()
})

// === LISTAGEM (R) ===
// router.get("/", async (req, res) => {
//     try {
//         const veiculos = await prisma.veiculo.findMany({
//             orderBy: { modelo: 'asc' }
//         })
//         res.status(200).json(veiculos)
//     } catch (error) {
//         res.status(500).json({ erro: error })
//     }
// })
// ...
router.get("/", async (req, res) => {
    try {
        const veiculos = await prisma.veiculo.findMany({
            where: { deleted: false }, // <--- FILTRO SOFT DELETE
            orderBy: { modelo: 'asc' }
        })
        res.status(200).json(veiculos)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})
// ...

// === INCLUSÃO (C) ===
router.post("/", async (req, res) => {
    const valida = veiculoSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    const { placa, modelo, cor, ano, status } = valida.data

    try {
        const existe = await prisma.veiculo.findUnique({
            where: { placa }
        })

        if (existe) {
            res.status(400).json({ erro: "Já existe um veículo com esta placa." })
            return
        }

        const veiculo = await prisma.veiculo.create({
            data: {
                placa,
                modelo,
                cor,
                ano,
                ...(status && { status })
            }
        })

        res.status(201).json(veiculo)
    } catch (error) {
        res.status(400).json({ error })
    }
})

// === ALTERAÇÃO (U) ===
router.put("/:id", async (req, res) => {
    const { id } = req.params

    const valida = veiculoSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    try {
        // Verifica se a placa nova já existe em OUTRO veículo
        const veiculoExistente = await prisma.veiculo.findUnique({
            where: { placa: valida.data.placa }
        })

        if (veiculoExistente && veiculoExistente.id !== Number(id)) {
            res.status(400).json({ erro: "Esta placa já pertence a outro veículo." })
            return
        }

        const { status: statusUpdate, ...resto } = valida.data
        const veiculo = await prisma.veiculo.update({
            where: { id: Number(id) },
            data: {
                ...resto,
                ...(statusUpdate && { status: statusUpdate })
            }
        })
        res.status(200).json(veiculo)
    } catch (error) {
        res.status(400).json({ erro: "Veículo não encontrado ou erro no servidor." })
    }
})

// === EXCLUSÃO (D) ===
// router.delete("/:id", async (req, res) => {
//     const { id } = req.params

//     try {
//         // Verifica dependência de aluguéis
//         const possuiAluguel = await prisma.aluguel.findFirst({
//             where: { veiculoId: Number(id) }
//         })

//         if (possuiAluguel) {
//             res.status(400).json({ erro: "Não é possível excluir: Veículo possui histórico de aluguéis." })
//             return
//         }

//         const veiculo = await prisma.veiculo.delete({
//             where: { id: Number(id) }
//         })
//         res.status(200).json(veiculo)
//     } catch (error) {
//         res.status(400).json({ erro: "Veículo não encontrado ou erro no servidor" })
//     }
// })
// ...
router.delete("/:id", async (req, res) => {
    const { id } = req.params

    try {
        // Verifica se já está excluído
        const veiculo = await prisma.veiculo.findUnique({ where: { id: Number(id) } })
        if (!veiculo || veiculo.deleted) {
            res.status(400).json({ erro: "Veículo não encontrado" })
            return
        }

        // Soft Delete: Atualiza flag e data
        await prisma.veiculo.update({
            where: { id: Number(id) },
            data: {
                deleted: true,
                deletedAt: new Date(),
                status: 'EM_REPARO' // Opcional: evita que seja listado como disponível em outras buscas
            }
        })

        res.status(200).json({ mensagem: "Veículo excluído com sucesso (Soft Delete)" })
    } catch (error) {
        res.status(400).json({ erro: "Erro ao excluir veículo" })
    }
})
// ...

export default router