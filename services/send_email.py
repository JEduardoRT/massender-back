import yagmail

def send_email(destinatarios, subject, content):
    yag = yagmail.SMTP('maria.mariaog.rivera@gmail.com', 'oadv mjhi ykkg mbja')
    yag.send(to=destinatarios, subject=subject, contents=content)
    print("Correo enviado exitosamente")

