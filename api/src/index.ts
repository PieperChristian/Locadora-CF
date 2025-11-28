import express from 'express'
import cors from 'cors'
import routesAtendentes from './routes/atendentes.js'
import routesLogin from './routes/login.js'
import routesClientes from './routes/clientes.js'
import routesVeiculos from './routes/veiculos.js'
import routesAlugueis from './routes/alugueis.js'
import routesSistema from './routes/sistema.js'

const app = express()
const port = 3000

app.use(express.json())
app.use(cors())

app.use("/atendentes", routesAtendentes)
app.use("/login", routesLogin)
app.use("/clientes", routesClientes)
app.use("/veiculos", routesVeiculos)
app.use("/alugueis", routesAlugueis)
app.use("/sistema", routesSistema)

app.get('/', (req, res) => {
    res.send('API: Locadora de Veículos - Sistema de Gestão')
})

app.listen(port, () => {
    console.log(`Servidor rodando na porta: ${port}`)
})
