
# to get a string like this run:
# openssl rand -hex 32
# ESTE ES EL KEY DE DEV
SECRET_KEY = "3827f9616ecc024d04f2d7242faa4ba6b99c249afaddee7e66555db3c8bce29b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

ESTADO_ACTIVO = "A"
ESTADO_INACTIVO = "I"


ASUNTO_RECUPERAR = "Nueva contraseña en Massender!"

CORREO_RECUPERACION = "Estimado/a NOMBRE,\n\nHemos recibido una solicitud para restablecer la contraseña de tu cuenta en Massender. A continuación, te proporcionamos tus nuevos datos de acceso:\n\nUsuario: USUARIO\n\nNueva Contraseña: PASSWORD\n\nTe recomendamos cambiar esta contraseña después de iniciar sesión para mayor seguridad.\n\nPara acceder a tu cuenta, sigue estos pasos:\n\nDirígete a Massender Web.\nInicia sesión con tu nombre de usuario y la nueva contraseña proporcionada.\nCambia tu contraseña desde la configuración de la cuenta.\nSi no solicitaste este cambio, por favor, ignora este mensaje o contacta con nuestro equipo de soporte de inmediato.\n\nGracias por utilizar Massender.\n\nSaludos cordiales,\n\nEquipo de Hangaroa"
