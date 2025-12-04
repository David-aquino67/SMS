class RepRequestDTO:
    def __init__(self, data: dict):
        self.CONREP = data.get("CONREP")
        self.FECEVE = data.get("FECEVE")
        self.FECREP = data.get("FECREP")
        self.FREREP = data.get("FREREP")
        self.OBSREP = data.get("OBSREP")

        self.LUGREP = data.get("LUGREP")
        self.CANREP = data.get("CANREP")
        self.PERREP = data.get("PERREP")

        if not self.FECEVE or not self.PERREP or not self.LUGREP:
            raise ValueError("Faltan campos obligatorios para el reporte.")

    def to_dict(self) -> dict:
        return self.__dict__