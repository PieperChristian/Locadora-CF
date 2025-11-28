-- AlterTable
ALTER TABLE `atendentes` ADD COLUMN `bloqueadoAte` DATETIME(3) NULL,
    ADD COLUMN `perguntaSeguranca` VARCHAR(100) NULL,
    ADD COLUMN `respostaSeguranca` VARCHAR(60) NULL,
    ADD COLUMN `tentativasLogin` INTEGER NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE `veiculos` ADD COLUMN `deleted` BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN `deletedAt` DATETIME(3) NULL;
