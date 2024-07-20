import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_correo(destinatarios, asunto, mensaje):
    remitente = "telemercadeo@hangaroa.ec"
    password = "Telemercadeo2024@"

    # Configuración del servidor SMTP
    servidor = "mail.hangaroa.ec"
    puerto = 465

    destinatarios.append("marrcarr@espol.edu.ec")

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['Subject'] = asunto

    # Adjuntar el mensaje en formato de texto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Conectar al servidor SMTP usando SSL y enviar el correo
        server = smtplib.SMTP_SSL(servidor, puerto)
        server.login(remitente, password)
        # Enviar correo a cada destinatario
        for destinatario in destinatarios:
            msg['To'] = destinatario
            server.sendmail(remitente, destinatario, msg.as_string())

        server.quit()
        print("Correo enviado exitosamente a todos los destinatarios")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
