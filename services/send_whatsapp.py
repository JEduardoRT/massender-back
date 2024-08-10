import requests
import json
import logging

# Configurar el registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_mensaje_whatsapp(destinatarios, mensaje):
    access_token = 'EAA4BSeIrXxYBO4U4XWkE9LQzzvynfdoRAoyOmPDLBCQa6Ed32AoLadZCuGCZBx8Phcf1xjDmZBzi0aIlsZBjyeDAZBoyyFGsPZCtYWQTRhe8FsNf5vrciQY59bCLZByVpOGD2XMtFARXElvM15dnu2vvZBEf7DMNBQEp93DMjwZB7lkl2Sepqpp7SVIT3OqHfOsaEyObOGYqB8DuhzDzppo4ZD'
    phone_number_id = '330293983510087'

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
            "messaging_product": "whatsapp",
            "to": numero_formateado,
            "type": 'text',
            "text": {
                "body": mensaje
            }
        }

        logger.info(f"Enviando mensaje a {numero_formateado} con payload: {payload}")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        if response.status_code == 200:
            logger.info(f"Mensaje enviado exitosamente a {numero_formateado}")
            logger.info(f"Respuesta de la API: {response_data}")
        else:
            logger.error(f"Error al enviar el mensaje a {numero_formateado}: {response_data}")
            logger.error(f"Código de estado: {response.status_code}")

# Ejemplo de uso
destinatarios = ['0987615981', '0998645309']
mensaje = "Este es un mensaje de prueba personalizado."

enviar_mensaje_whatsapp(destinatarios, mensaje)
