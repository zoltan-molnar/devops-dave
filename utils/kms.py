import base64
import boto3
from utils.config import CONFIG

kms = boto3.client('kms', region_name=CONFIG['aws_region'])


def encrypt(text):
    encrypted = kms.encrypt(KeyId=CONFIG['user_data_kms_arn'], Plaintext=str(text))
    return base64.standard_b64encode(encrypted['CiphertextBlob'])


def decrypt(encrypted_text):
    decrypted = kms.decrypt(CiphertextBlob=base64.standard_b64decode(encrypted_text))
    return decrypted['Plaintext']
