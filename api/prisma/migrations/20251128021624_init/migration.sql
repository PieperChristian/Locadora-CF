-- CreateTable
CREATE TABLE `clientes` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(60) NOT NULL,
    `cpf` VARCHAR(14) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `telefone` VARCHAR(20) NOT NULL,
    `endereco` VARCHAR(255) NOT NULL,

    UNIQUE INDEX `clientes_cpf_key`(`cpf`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `veiculos` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `placa` VARCHAR(8) NOT NULL,
    `modelo` VARCHAR(50) NOT NULL,
    `cor` VARCHAR(30) NOT NULL,
    `ano` SMALLINT NOT NULL,
    `status` ENUM('DISPONIVEL', 'ALUGADO', 'EM_REPARO') NOT NULL DEFAULT 'DISPONIVEL',

    UNIQUE INDEX `veiculos_placa_key`(`placa`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `atendentes` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `nome` VARCHAR(60) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `senha` VARCHAR(60) NOT NULL,

    UNIQUE INDEX `atendentes_email_key`(`email`),
    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `alugueis` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `clienteId` INTEGER NOT NULL,
    `veiculoId` INTEGER NOT NULL,
    `atendenteId` INTEGER NOT NULL,
    `dataHoraRetirada` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `dataHoraDevolucao` DATETIME(3) NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `logs` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `atendenteId` INTEGER NOT NULL,
    `atividade` VARCHAR(255) NOT NULL,
    `data` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `alugueis` ADD CONSTRAINT `alugueis_clienteId_fkey` FOREIGN KEY (`clienteId`) REFERENCES `clientes`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `alugueis` ADD CONSTRAINT `alugueis_veiculoId_fkey` FOREIGN KEY (`veiculoId`) REFERENCES `veiculos`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `alugueis` ADD CONSTRAINT `alugueis_atendenteId_fkey` FOREIGN KEY (`atendenteId`) REFERENCES `atendentes`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `logs` ADD CONSTRAINT `logs_atendenteId_fkey` FOREIGN KEY (`atendenteId`) REFERENCES `atendentes`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
