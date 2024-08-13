import requests
import json
import logging

# Configurar el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def enviar_sms_masivo(numeros_telefonos, nombre_campania):

    for numero_telefono in numeros_telefonos:
        url = "https://api.massend.com/api/sms"

        # Construcción del payload
        payload = json.dumps({
            "user": "Hangaroa@massend.com",
            "pass": "Hangaroa123@#",
            "mensajeid": "43773",
            "campana": nombre_campania,
            "tipo": 0,
            "ruta": 0,
            "telefono": numero_telefono
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info(response)

        return response.text


