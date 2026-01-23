from domain.port.whey_ports import WheyRepository


class DeleteWheyUseCase:
    def __init__(self, whey_repo: WheyRepository):
        self._whey_repo = whey_repo
        
    def Execute(self, whey_id: str) -> None:
        self._whey_repo.delete_whey(whey_id)
