from app.integrations.carrier.automation import CarrierAutomationClient


class ShippingService:
    def __init__(self) -> None:
        self.client = CarrierAutomationClient()

    def prepare_label_generation(self, payload: dict) -> dict:
        return self.client.create_shipping_label(payload)
