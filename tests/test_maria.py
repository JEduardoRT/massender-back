import pytest
from pydantic import ValidationError
from models.destinatario_request import DestinatarioRequest


def test_valid_destinatario():
    # Prueba con datos válidos
    destinatario = DestinatarioRequest(
        cedula="0123456789",
        nombre="Juan",
        apellido="Pérez",
        genero="M",
        correo="juan.perez@example.com",
        telefono="593987654321"
    )
    assert destinatario.cedula == "0123456789"
    assert destinatario.nombre == "Juan"
    assert destinatario.apellido == "Pérez"
    assert destinatario.genero == "M"
    assert destinatario.correo == "juan.perez@example.com"
    assert destinatario.telefono == "593987654321"

def test_invalid_correo():
    # Prueba con correo inválido
    with pytest.raises(ValidationError):
        DestinatarioRequest(
            cedula="0123456789",
            nombre="Juan",
            apellido="Pérez",
            genero="M",
            correo="correo_invalido",
            telefono="593987654321"
        )

def test_invalid_telefono():
    # Prueba con número de teléfono inválido
    with pytest.raises(ValidationError):
        DestinatarioRequest(
            cedula="0123456789",
            nombre="Juan",
            apellido="Pérez",
            genero="M",
            correo="juan.perez@example.com",
            telefono="1234abc567"
        )

def test_optional_telefono():
    # Prueba con el teléfono como None
    destinatario = DestinatarioRequest(
        cedula="0123456789",
        nombre="Juan",
        apellido="Pérez",
        genero="M",
        correo="juan.perez@example.com",
        telefono=None
    )
    assert destinatario.telefono is None

def test_invalid_genero():
    # Prueba con género inválido
    with pytest.raises(ValidationError):
        DestinatarioRequest(
            cedula="0123456789",
            nombre="Juan",
            apellido="Pérez",
            genero="X",
            correo="juan.perez@example.com",
            telefono="593987654321"
        )

def test_long_cedula():
    # Prueba con cédula demasiado larga
    with pytest.raises(ValidationError):
        DestinatarioRequest(
            cedula="012345678901234567890",
            nombre="Juan",
            apellido="Pérez",
            genero="M",
            correo="juan.perez@example.com",
            telefono="593987654321"
        )

def test_valid_short_cedula():
    # Prueba con cédula válida y corta
    destinatario = DestinatarioRequest(
        cedula="1234567890",
        nombre="Juan",
        apellido="Pérez",
        genero="M",
        correo="juan.perez@example.com",
        telefono="593987654321"
    )
    assert destinatario.cedula == "1234567890"
