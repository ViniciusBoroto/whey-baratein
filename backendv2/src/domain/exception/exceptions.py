from domain.entity.product import ProductRead, ProductType


class EntityNotFoundException(Exception):
    pass

class ProductNotFoundException(EntityNotFoundException):
    def __init__(self, product_id: int, type: ProductType):
        super().__init__(f"{type} with id '{product_id}' not found")

class WheyNotFoundException(ProductNotFoundException):
    def __init__(self, whey_id: int):
        super().__init__(whey_id, ProductType.WHEY)


class BrandNotFoundException(EntityNotFoundException):
    def __init__(self, brand_id: int):
        super().__init__(f"Brand with id '{brand_id}' not found")

class UserNotFoundException(EntityNotFoundException):
    def __init__(self, user_id: int):
        super().__init__(f"User with id '{user_id}' not found")

class InvalidCredentialsException(Exception):
    pass