#! python
# -*- coding:utf-8 -*-

# code test :
# python.exe .\publicate.py -a "./CC_Script/disk/advTurtle.lua" "[CC] turtle - advTurtle" 2

import sys, os, hashlib, sqlite3
from functools import partial

class db(object):
	""" définit une base de donnée
	"""
	def __init__(self,fichier,rqSqlStart = []):
		""" Initialisation de la basestring
		"""
		self.connexion = sqlite3.connect(fichier)
		self.connexion.isolation_level = None
		if len(rqSqlStart) > 0 :
			self.start(rqSqlStart)
		
	def getCursor(self):
		return self.connexion.cursor()
		
	def start(self, rqSqlStart):
		"""Execution d'une série de requête de départ
		"""
		print('init DB');
		cur = self.getCursor()
		for rqSql in rqSqlStart :
			print('DB ...');
			try:
				cur.execute(rqSql);
			except sqlite3.Error as e:
				raise SystemExit("Problème sqlite3 : ", e.args[0])
		print('DB Ok');
		
class fichierManager(object):
	""" déinition de l interface BD fichiers
	"""
	def __init__(self, _db) :
		""" Initialisation du manager
		"""
		self.db = _db
		
	def getById(self, id):
		""" Délivre un fichier public
		"""
		cur = self.db.getCursor()
		fp = None
		rqSql = """
		select * from fichiers where id = ?;
		"""
		data = (id,)
		try:
			cur.execute(rqSql, data);
			rows = cur.fetchall()
			if len(rows)>0:
				row = rows[0]
				fp = fichierPublic(row[2], row[4], row[3], row[0])
				fp.setNom(row[1])
			
		except sqlite3.Error as e:
			raise SystemExit("Problème sqlite3 : ", e.args[0])
		
		return fp
		
	def getAll(self):
		""" Délivre tous les fichier
		"""
		cur = self.db.getCursor()
		fps = []
		rqSql = "select * from fichiers;"
		try:
			cur.execute(rqSql);
			rows = cur.fetchall()
			if len(rows)>0:
				for row in rows :
					fp = fichierPublic(row[2], row[4], row[3], row[0])
					fp.setNom(row[1])
					fps.append(fp)
			
		except sqlite3.Error as e:
			raise SystemExit("Problème sqlite3 : ", e.args[0])
		
		return fps
		
	def backup(self, fp):
		""" Sauvegarde un fichier publique à la basestring
		"""
		cur = self._db.getCursor()
		if fp.getId() < 0:
			rqSql = """
			INSERT INTO fichiers(nom, path, titre_pastebin, version)
			VALUES (?, ?, ?, ?);
			"""
			data = (fp.getNom(), fp.getPath(), fp.getTitre(), fp.getVersion(),)
		else:
			rqSql = """
			UPDATE fichiers
			SET
			nom = ?,
			path = ?,
			titre_pastebin = ?,
			version = ?
			WHERE
			id = ?
			"""
			data = (fp.getNom(), fp.getPath(), fp.getTitre(), fp.getVersion(),fp.getId())
			
		try:
			cur.execute(rqSql, data);
		except sqlite3.Error as e:
			raise SystemExit("Problème sqlite3 : ", e.args[0])

class versionManager(object):
	""" Définition d'une interface entre les versions d'un fichier et la base
	de donnée
	"""
	def __init__(self, _db) :
		""" Initialisation du manager
		"""
		self.db = _db
		
	def getById(self, id):
		""" Délivre un fichier public
		"""
		cur = self._db.getCursor()
		vers = None
		rqSQL = """
		select * from versions where id = ?;
		"""
		data = (id,)
		try:
			cur.execute(rqSql, data);
			rows = cur.fetchall()
			
			
		except sqlite3.Error as e:
			raise SystemExit("Problème sqlite3 : ", e.args[0])
		
		return vers
		
	def getAll(self):
		""" Délivre tous les fichier
		"""
		cur = self._db.getCursor()
		fps =  []
		
		return fps
		
	def backup(self, vers):
		""" Sauvegarde un fichier publique à la basestring
		"""
		cur = self._db.getCursor()
		if vers.getId() < 0:
			rqSql = """
			INSERT INTO fichiers(nom, path, titre_pastebin, version)
			VALUES (?, ?, ?, ?);
			"""
			data = (vers.getNom(), fp.getPath(), fp.getTitre(), fp.getVersion(),)
		else:
			rqSql = """
			UPDATE fichiers
			SET
			nom = ?,
			path = ?,
			titre_pastebin = ?,
			version = ?
			WHERE
			id = ?
			"""
			data = (fp.getNom(), fp.getPath(), fp.getTitre(), fp.getVersion(),fp.getId())
			
		try:
			cur.execute(rqSql, data);
		except sqlite3.Error as e:
			raise SystemExit("Problème sqlite3 : ", e.args[0])
			
class fichierPublic(object) :
	""" definition d'un fichier
	"""
	def __init__(self, _path = '', _titre = '', _version = '', _id = -1) :
		""" Initialisation d'un objet
		"""
		
		if len(_path) > 0:
			if not os.path.isfile(_path):
				raise SystemExit('Le fichier "{}" n\'est pas valide'.format(_path))
		
		nom, ext = os.path.splitext(os.path.basename(_path));
		
		self.id = _id
		self.name = nom
		self.path = _path
		self.titre = _titre
		self.versionBase = _version
	
	def __repr__(self):
		return "<[{0}] {1}, path : {2}, titre : {3}, version : {4}>".format(self.id, self.name, self.path, self.titre, self.versionBase)
	
	def setNom(self, _nom):
		self.name = _nom
		return self
	def getNom(self):
		return self.name
		
	def setPath(self, _path):
		if not os.path.isfile(_path):
				raise SystemExit('Le fichier "{}" n\'est pas valide'.format(_path))
		self.path = _path
		return self
	def getPath(self):
		return self.path
		
	def setTitre(self, _titre):
		self.titre = _titre
		return self
	def getTitre(self):
		return self.titre
		
	def setVersionBase(self, _version):
		self.versionBase = _version
		return self
	def getVersionBase(self):
		return self.versionBase

	def setId(self, _id):
		if self.id < 0:
			self.id = _id
		else:
			raise Exception('Impossible de modifier l\'ID du fichier.')
		return self
	def getId(self):
		return self.id
		
class versionFichier(object)
	
		
def sha1sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def affiche1fichier(fp):
	pass
	
def ajoutFichier(path, titre, version, _db):
	fpsm = fichierManager(_db)
	fp = fichierPublic(path, titre, version)
	fpdm.backup(fp)

def afficheFichier(fichiers):
	pass

def publiFichier():
	pass

rqSqls = ["""
	CREATE TABLE IF NOT EXISTS [fichiers] (
	[id] INTEGER  PRIMARY KEY AUTOINCREMENT NULL,
	[nom] VARCHAR(256)  UNIQUE NOT NULL,
	[path] TEXT  NOT NULL,
	[version] VARCHAR(10)  NOT NULL,
	[titre_pastebin] VARCHAR(256)  UNIQUE NOT NULL,
	[cree] TIMESTAMP  NULL,
	[modifie] TIMESTAMP  NULL
	);
	""","""
	CREATE TRIGGER IF NOT EXISTS [t_fichiers_c] 
	AFTER INSERT ON [fichiers] 
	FOR EACH ROW 
	BEGIN 
	UPDATE fichiers
	SET cree = DATETIME('NOW')
	WHERE rowid = new.rowid;
	END;
	""","""
	CREATE TRIGGER IF NOT EXISTS [t_fichiers_m] 
	AFTER UPDATE ON [fichiers] 
	FOR EACH ROW 
	BEGIN 
	UPDATE fichiers
	SET modifie = DATETIME('NOW')
	WHERE rowid = new.rowid;
	END;
	""","""
	CREATE TABLE IF NOT EXISTS [versions] (
	[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
	[id_fichier] INTEGER  NOT NULL,
	[hash_fichier] VARCHAR(128)  NOT NULL,
	[sous_version] VARCHAR(10)  NULL,
	[pastebin_id] VARCHAR(16)  NULL,
	[cree] TIMESTAMP  NULL,
	[modifie] TIMESTAMP  NULL
	);
	""","""
	CREATE TRIGGER IF NOT EXISTS [t_version_c]
	AFTER INSERT ON [versions]
	FOR EACH ROW 
	BEGIN 
	UPDATE versions
	SET cree = DATETIME('NOW')
	WHERE rowid = new.rowid;
	END;
	""","""
	CREATE TRIGGER IF NOT EXISTS [t_versions_m]
	AFTER UPDATE ON [versions]
	FOR EACH ROW 
	BEGIN 
	UPDATE versions
	SET modifie = DATETIME('NOW')
	WHERE rowid = new.rowid;
	END;
	""","""
	CREATE INDEX IF NOT EXISTS [i_versions_hash_fichier] 
	ON [versions]([hash_fichier]  ASC);
	"""]
myDb = db("db.sqlite3", rqSqls)

"""
if len(sys.argv) > 1 :
	cmd = sys.argv[1];
	if cmd == '-a' :
		if len(sys.argv[2:]) != 3 :
			raise SystemExit('le nombre d\'argument n\'est pas valide')
		path, titre, vers = sys.argv[2:];
		ajoutFichier(path, titre, vers);
	elif cmd == '-m' :
		if len(sys.argv[2:]) != 3 :
			raise SystemExit('le nombre d\'argument n\'est pas valide')
		fich, key, val = sys.argv[2:]
		print('fich',fich,'titre',key,'version', val);
	elif cmd == '-r' :
		if len(sys.argv[2:]) > 1 :
			raise SystemExit('le nombre d\'argument n\'est pas valide')
		fich = sys.argv[2:]
		afficheFichier(fich);
	else :
		print('option inconnue')
"""

fpsm = fichierManager(myDb)
print(fpsm.getAll())