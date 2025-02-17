class Glied:
    id_counter = 1
    
    def __init__(self, gelenk1_id, gelenk2_id):
        self.id_glied = Glied.id_counter
        Glied.id_counter += 1


        self.gelenk1_id = gelenk1_id
        self.gelenk2_id = gelenk2_id
        self.gestell = False
        self.kurbel = False


    def speichern(self):
        return {"id_glied": self.id_glied, "gelenk1_id": self.gelenk1_id, "gelenk2_id": self.gelenk2_id, "gestell": self.gestell, "kurbel": self.kurbel}