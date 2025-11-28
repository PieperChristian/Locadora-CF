import type { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

interface TokenInterface {
    userLogadoId: number
    userLogadoNome: string
}

declare global {
    namespace Express {
        interface Request {
            userLogadoId?: number
            userLogadoNome?: string
        }
    }
}

export function verificaToken(req: Request, res: Response, next: NextFunction) {
    const { authorization } = req.headers

    if (!authorization) {
        res.status(401).json({ erro: "Token não informado" })
        return
    }

    const token = authorization.split(" ")[1]

    try {
        const secret = process.env.JWT_KEY
        if (!secret) {
            res.status(500).json({ erro: "Chave JWT não configurada" })
            return
        }

        // @ts-ignore
        const decode = jwt.verify(token, secret)
        const { userLogadoId, userLogadoNome } = decode as unknown as TokenInterface

        req.userLogadoId = userLogadoId
        req.userLogadoNome = userLogadoNome

        next()
    } catch (erro) {
        res.status(401).json({ erro: "Token inválido ou expirado" })
    }
}