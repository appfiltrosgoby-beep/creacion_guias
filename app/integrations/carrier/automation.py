from app.core.config import get_settings


class CarrierAutomationClient:
    """Punto de integración para generar, descargar o enviar la guía.

    Recomendación para la siguiente fase: usar Playwright para automatizar
    la página de la transportadora cuando no exista API oficial.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

    def create_shipping_label(self, payload: dict) -> dict:
        return {
            "status": "pending",
            "message": "Automatización pendiente de implementar.",
            "carrier_base_url": self.settings.carrier_base_url,
            "payload_preview": payload,
        }
