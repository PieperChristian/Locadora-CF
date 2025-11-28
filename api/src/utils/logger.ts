import { PrismaClient } from "@prisma/client"

const prisma = new PrismaClient()

export async function registrarLog(atendenteId: number, atividade: string) {
  try {
    await prisma.log.create({
      data: {
        atendenteId,
        atividade,
        data: new Date()
      }
    })
    console.log(`[LOG] Atendente ${atendenteId}: ${atividade}`)
  } catch (error) {
    console.error("Falha ao registrar log:", error)
  }
}