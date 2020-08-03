import boto3
import logging

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

backup = boto3.client('backup')

def lambda_handler(event, context):

    # List Backup Vaults
    backupvaults = backup.list_backup_vaults()

    logger.info(backupvaults)
    backupVaultNames = [backupvault['BackupVaultName'] for backupvault in backupvaults['BackupVaultList']]

    # For each Vault
    for backupvault in backupVaultNames:
        recoverypoints = backup.list_recovery_points_by_backup_vault(BackupVaultName=backupvault)
        logger.info("Checking Recover points in vault: " + backupvault)
        for recoverypoint in recoverypoints['RecoveryPoints']:
            if recoverypoint['Status'] == 'EXPIRED':
                logger.info("Deleting expired recovery point: " + recoverypoint['RecoveryPointArn'])
                result = backup.delete_recovery_point(BackupVaultName=backupvault,RecoveryPointArn=recoverypoint['RecoveryPointArn'])