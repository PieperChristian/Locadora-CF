import nodemailer from "nodemailer"

// Configuração do Transporter (Mailtrap)
const transporter = nodemailer.createTransport({
  host: "sandbox.smtp.mailtrap.io",
  port: 587,
  secure: false,
  auth: {
    user: process.env.MAILTRAP_USER,
    pass: process.env.MAILTRAP_PASS
  },
});

export async function enviarEmailComprovante(
  destinatario: string, 
  assunto: string, 
  dados: {
    cliente: string,
    veiculo: string,
    placa: string,
    dataRetirada: Date,
    dataDevolucao?: Date | null, // Pode ser nulo se for apenas retirada
    tipo: "ALUGUEL" | "DEVOLUCAO"
  }
) {
  
  const dataFormatada = (data: Date) => data.toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });

  // Template HTML simples
  const html = `
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ccc; max-width: 600px;">
      <h2 style="color: #2c3e50;">Locadora CF - Comprovante de ${dados.tipo === 'ALUGUEL' ? 'Retirada' : 'Devolução'}</h2>
      <p>Olá, <strong>${dados.cliente}</strong>.</p>
      <p>Confira abaixo os detalhes da sua transação:</p>
      
      <table style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #f2f2f2;">
          <td style="padding: 10px; border: 1px solid #ddd;"><strong>Veículo:</strong></td>
          <td style="padding: 10px; border: 1px solid #ddd;">${dados.veiculo} (${dados.placa})</td>
        </tr>
        <tr>
          <td style="padding: 10px; border: 1px solid #ddd;"><strong>Data Retirada:</strong></td>
          <td style="padding: 10px; border: 1px solid #ddd;">${dataFormatada(dados.dataRetirada)}</td>
        </tr>
        ${dados.dataDevolucao ? `
        <tr style="background-color: #e8f5e9;">
          <td style="padding: 10px; border: 1px solid #ddd;"><strong>Data Devolução:</strong></td>
          <td style="padding: 10px; border: 1px solid #ddd;">${dataFormatada(dados.dataDevolucao)}</td>
        </tr>` : ''}
      </table>

      <p style="margin-top: 20px; font-size: 12px; color: #7f8c8d;">Este é um e-mail automático. Não responda.</p>
    </div>
  `;

  try {
    const info = await transporter.sendMail({
      from: '"Locadora CF" <sistema@locadoracf.com.br>',
      to: destinatario,
      subject: `[Locadora CF] ${assunto}`,
      html: html,
    });
    console.log("Message sent: %s", info.messageId);
  } catch (error) {
    console.error("Erro ao enviar e-mail:", error);
  }
}