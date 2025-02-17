class Mechanismus:

    def __init__(self, name, glieder, gelenke):
        self.id = None
        self.name = name
        self.glieder = glieder
        self.gelenke = gelenke
        self.antrieb = None
        self.statik = None

    def add_gelenk(self,):
    
    def add_glied(self,):

    def speichern(self,):
        db = TinyDB('database.json')
        mechanismus_tabelle = db.table('mechanismen')

    
        
