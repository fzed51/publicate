# module manager

class Manager(object):
	"Définition d'un managet"

	_db = none
	_table = ""
	_field = ""
	
	@classmethod
	def setDb(cls, db):
		" Initialisation de l'acces à la base de donnée"
		
		cls._db = db
	
	def backup(cls, champs**)
		" insertion de valeur "
		
		# TODO : detection de id dans les champs
		# TODO : parser les paramètre pour recrééer une requete insert ou update