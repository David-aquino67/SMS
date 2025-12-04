class RepResponseDTO:

    def __init__(self, rep_model):
        fec_eve_str = str(rep_model.FECEVE) if rep_model.FECEVE else None
        fec_rep_str = str(rep_model.FECREP) if rep_model.FECREP else None
        self.IDEREP = rep_model.IDEREP
        self.CONREP = bool(rep_model.CONREP)
        self.FECEVE = fec_eve_str
        self.FECREP = fec_rep_str
        self.FREREP = rep_model.FREREP
        self.OBSREP = rep_model.OBSREP

        self.LUGREP = rep_model.LUGREP
        self.PERREP = rep_model.PERREP



    def to_dict(self) -> dict:
        return self.__dict__