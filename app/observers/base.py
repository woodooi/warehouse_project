from abc import ABC, abstractmethod
from app.models.product import Product

class Observer(ABC):
    @abstractmethod
    def update(self, product: Product):
        pass
