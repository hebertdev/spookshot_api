import cloudinary
import cloudinary.api


def verify_cloudinary_credentials():
    try:
        cloudinary.config(
            cloud_name='hebertdev1',
            api_key='514693421829746',
            api_secret='ymvkZZeupgZS4xsTf-EGrGaBrBc',
        )
        cloudinary.api.ping()
        print("Las credenciales son válidas")
        return True
    except Exception as e:
        print("Error al verificar las credenciales:", e)
        return False
