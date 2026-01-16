from googleAdsDummy.dataModels.campaign import Campaign


class Campaign:
    def __repr__(self):
        return f"Campaign classe that provides methods to mockup data about campigns"

    def configClass(self, **kwargs) -> None: ...

    def generator(self): ...
