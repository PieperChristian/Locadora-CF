import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { verificaToken } from './verificaToken.js'

const prisma = new PrismaClient()
const router = Router()

router.use(verificaToken)

router.get("/backup", async (req, res) => {
    try {
        const backup = {
            atendentes: await prisma.atendente.findMany(),
            clientes: await prisma.cliente.findMany(),
            veiculos: await prisma.veiculo.findMany(),
            alugueis: await prisma.aluguel.findMany(),
            logs: await prisma.log.findMany()
        }
        res.status(200).json(backup)
    } catch (error) {
        res.status(500).json({ erro: "Falha ao gerar backup: " + error })
    }
})

router.post("/restore", async (req, res) => {
    const dados = req.body

    try {
        // Transação massiva para limpar e restaurar
        await prisma.$transaction(async (tx) => {
            // 1. Limpeza (Ordem importa devido às chaves estrangeiras)
            await tx.log.deleteMany()
            await tx.aluguel.deleteMany()
            await tx.veiculo.deleteMany()
            await tx.cliente.deleteMany()
            await tx.atendente.deleteMany()

            // 2. Restauração
            // Usamos createMany para performance, mas removemos IDs para evitar conflitos 
            // ou mantemos IDs se o banco permitir (MySQL permite insert em auto-increment se especificado)

            if (dados.atendentes?.length) await tx.atendente.createMany({ data: dados.atendentes })
            if (dados.clientes?.length) await tx.cliente.createMany({ data: dados.clientes })
            if (dados.veiculos?.length) await tx.veiculo.createMany({ data: dados.veiculos })
            if (dados.alugueis?.length) {
                // Alugueis precisam de tratamento de data (string -> Date) se vierem do JSON puro
                const alugueisFormatados = dados.alugueis.map((a: any) => ({
                    ...a,
                    dataHoraRetirada: new Date(a.dataHoraRetirada),
                    dataHoraDevolucao: a.dataHoraDevolucao ? new Date(a.dataHoraDevolucao) : null
                }))
                await tx.aluguel.createMany({ data: alugueisFormatados })
            }
            if (dados.logs?.length) {
                const logsFormatados = dados.logs.map((l: any) => ({
                    ...l,
                    data: new Date(l.data)
                }))
                await tx.log.createMany({ data: logsFormatados })
            }
        })

        res.status(200).json({ mensagem: "Dados restaurados com sucesso!" })
    } catch (error) {
        console.error(error)
        res.status(500).json({ erro: "Falha crítica ao restaurar backup. Verifique o formato dos dados." })
    }
})

router.get("/logs", async (req, res) => {
    try {
        const logs = await prisma.log.findMany({
            take: 50,
            orderBy: { data: 'desc' },
            include: {
                atendente: {
                    select: { nome: true }
                }
            }
        })
        res.status(200).json(logs)
    } catch (error) {
        res.status(500).json({ erro: "Erro ao buscar logs: " + error })
    }
})

export default router