from pydantic import BaseModel


class WheyProtein(BaseModel):
    name: str
    price: float
    brand: str
    serving_size: int
    total_weight: int
    protein_per_serving: int

    #EAAs
    fenilanina: float =0
    histidina: float =0
    isoleucina: float =0
    leucina: float =0
    lisina: float =0
    metionina: float =0
    treonina: float =0
    triptofano: float =0
    valina: float=0
    def eea_per_serving(self) -> float:
        return self.fenilanina + self.histidina + self.isoleucina + self.leucina + self.lisina + self.metionina + self.treonina + self.triptofano + self.valina
    def servings_per_packet(self) -> float:
        return self.total_weight / self.serving_size
    def total_eea_per_packet(self) -> float:
        return self.eea_per_serving() * self.servings_per_packet()
    def eea_price(self) -> float:
        return self.total_eea_per_packet() / self.price
    def protein_concentration(self) -> float:
        return self.protein_per_serving / self.serving_size * 100


