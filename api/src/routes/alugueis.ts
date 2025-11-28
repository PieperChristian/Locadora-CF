import { PrismaClient } from '@prisma/client'
import { Router } from 'express'
import { z } from 'zod'
import { verificaToken } from './verificaToken.js'
import { registrarLog } from '../utils/logger.js'
import { enviarEmailComprovante } from '../utils/emailService.js'

const prisma = new PrismaClient()
const router = Router()

router.use(verificaToken)

const aluguelSchema = z.object({
    clienteId: z.number().int().positive(),
    veiculoId: z.number().int().positive()
})

router.get("/", async (req, res) => {
    try {
        const alugueis = await prisma.aluguel.findMany({
            include: {
                cliente: true,
                veiculo: true,
                atendente: { select: { id: true, nome: true } }
            },
            orderBy: { id: 'desc' }
        })
        res.status(200).json(alugueis)
    } catch (error) {
        res.status(500).json({ erro: error })
    }
})

router.post("/", async (req, res) => {
    const valida = aluguelSchema.safeParse(req.body)
    if (!valida.success) {
        res.status(400).json({ erro: valida.error })
        return
    }

    const { clienteId, veiculoId } = valida.data
    const atendenteId = req.userLogadoId as number

    try {
        const cliente = await prisma.cliente.findUnique({ where: { id: clienteId } })
        const veiculo = await prisma.veiculo.findUnique({ where: { id: veiculoId } })

        if (!cliente) { res.status(400).json({ erro: "Cliente não encontrado." }); return }
        if (!veiculo) { res.status(400).json({ erro: "Veículo não encontrado." }); return }
        if (veiculo.status !== 'DISPONIVEL') { res.status(400).json({ erro: "Veículo indisponível." }); return }

        const [aluguel, veiculoAtualizado] = await prisma.$transaction([
            prisma.aluguel.create({
                data: { clienteId, veiculoId, atendenteId }
            }),
            prisma.veiculo.update({
                where: { id: veiculoId },
                data: { status: 'ALUGADO' }
            })
        ])

        await registrarLog(atendenteId, `Realizou aluguel do veículo ${veiculo.placa} para o cliente ${cliente.nome}`)

        enviarEmailComprovante(cliente.email, "Confirmação de Aluguel", {
            cliente: cliente.nome,
            veiculo: `${veiculo.modelo} - ${veiculo.cor}`,
            placa: veiculo.placa,
            dataRetirada: aluguel.dataHoraRetirada,
            dataDevolucao: null,
            tipo: "ALUGUEL"
        })

        res.status(201).json({ aluguel, veiculo: veiculoAtualizado })
    } catch (error) {
        console.log(error)
        res.status(500).json({ erro: "Erro ao processar aluguel." })
    }
})

router.put("/devolucao/:id", async (req, res) => {
    const { id } = req.params
    const atendenteId = req.userLogadoId as number

    try {
        // Busca aluguel com dados do cliente e veiculo inclusos para o e-mail
        const aluguelExistente = await prisma.aluguel.findUnique({
            where: { id: Number(id) },
            include: { cliente: true, veiculo: true }
        })

        if (!aluguelExistente) { res.status(400).json({ erro: "Aluguel não encontrado." }); return }
        if (aluguelExistente.dataHoraDevolucao) { res.status(400).json({ erro: "Aluguel já encerrado." }); return }

        const [aluguelAtualizado, veiculo] = await prisma.$transaction([
            prisma.aluguel.update({
                where: { id: Number(id) },
                data: { dataHoraDevolucao: new Date() }
            }),
            prisma.veiculo.update({
                where: { id: aluguelExistente.veiculoId },
                data: { status: 'DISPONIVEL' }
            })
        ])

        // === AÇÕES PÓS-TRANSAÇÃO ===
        await registrarLog(atendenteId, `Registrou devolução do veículo ${aluguelExistente.veiculo.placa} (Aluguel #${id})`)

        if (aluguelAtualizado.dataHoraDevolucao) {
            enviarEmailComprovante(aluguelExistente.cliente.email, "Comprovante de Devolução", {
                cliente: aluguelExistente.cliente.nome,
                veiculo: `${aluguelExistente.veiculo.modelo} - ${aluguelExistente.veiculo.cor}`,
                placa: aluguelExistente.veiculo.placa,
                dataRetirada: aluguelExistente.dataHoraRetirada,
                dataDevolucao: aluguelAtualizado.dataHoraDevolucao,
                tipo: "DEVOLUCAO"
            })
        }

        res.status(200).json({ aluguel: aluguelAtualizado, veiculo })
    } catch (error) {
        res.status(500).json({ erro: "Erro ao processar devolução." })
    }
})

router.delete("/:id", async (req, res) => {
    const { id } = req.params
    try {
        const aluguelParaExcluir = await prisma.aluguel.findUnique({ where: { id: Number(id) } })
        if (!aluguelParaExcluir) { res.status(400).json({ erro: "Registro não encontrado." }); return }

        let operacoes: any[] = [prisma.aluguel.delete({ where: { id: Number(id) } })]
        if (!aluguelParaExcluir.dataHoraDevolucao) {
            operacoes.push(prisma.veiculo.update({ where: { id: aluguelParaExcluir.veiculoId }, data: { status: 'DISPONIVEL' } }))
        }
        await prisma.$transaction(operacoes)
        res.status(200).json({ mensagem: "Registro excluído." })
    } catch (error) { res.status(500).json({ erro: "Erro ao excluir." }) }
})

export default router