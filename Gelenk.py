class Gelenk:

    def __init__(self, x, y, ist_statisch):
        self.id_gelenk
        self.x = x
        self.y = y
        self.ist_statisch = ist_statisch

    def speichern(self):
        return {"id": self.id, "x": self.x, "y": self.y, "ist_statisch": self.ist_statisch}