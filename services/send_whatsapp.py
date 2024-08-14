import requests
import json
import logging

# Configurar el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_mensaje_whatsapp(destinatarios, asunto, mensaje):
    access_token = 'EAB0PZCKUthjIBOz43ffxl8N4SNZBKBroIeUq7mpZBqwDF5NkIzZCL2ErQWsBRlxw0FzqXObkZBH3UyZAQYyqEf0QQ6AkttYiCfwtq4fyYGBZBDLeCdidaebelFoHXPMqdBDZBPShE7ptEE6uJnAaE3fnzoGpmZAoDDFnZCvA7HbZCShCPBp6CZCxdkI1vs7CHIktWZCAdsHcER8ZCWpFvfLZCJEz28ZD'
    phone_number_id = '377344268801407'

    url = f'https://graph.facebook.com/v20.0/{phone_number_id}/messages'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    def formatear_numero(numero_local):
        # Asume que todos los números son de Ecuador y están en el formato 0987615981
        if numero_local.startswith('0'):
            return '+593' + numero_local[1:]
        else:
            return '+593' + numero_local

    for destinatario in destinatarios:
        numero_formateado = formatear_numero(destinatario)
        payload = {
            'messaging_product': 'whatsapp',
            'to': numero_formateado,
            'type': 'template',
            'template': {
                'name': 'hello_world',  # Nombre de la plantilla
                'language': {
                    'code': 'en_US'
                }
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        if response.status_code == 200:
            logger.info(f"Mensaje enviado exitosamente a {numero_formateado}")
            logger.info("Respuesta de la API:", response_data)
        else:
            logger.info(f"Error al enviar el mensaje a {numero_formateado}: {response_data}")
            logger.info("Código de estado:", response.status_code)