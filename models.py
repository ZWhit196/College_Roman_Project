from Database import db

from passlib.hash import pbkdf2_sha256


class User(db.Model):
	Email = db.Column(db.String(256), primary_key=True, unique=True)
	Name = db.Column(db.String(256))
	Password = db.Column(db.String(256))
	_Results = db.relationship('Result', backref='User', primaryjoin='User.Email==Result.User_email' )
	
	def __init__(self, email, name, password):
		self.Email = email.lower()
		self.Name = name.lower()
		self.set_password(password)
	
	def __repr__(self):
		return "<User {}>".format(self.Email)
	
	# Login manager
	def is_active(self):
		return True
	
	def is_anonymous(self):
		return False
	
	def is_authenticated(self):
		return True
	
	def get_id(self):
		return str(self.Email)
	# Login manager end

	def set_password(self, password):
		self.Password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
	
	def verify_password(self, password):
		return pbkdf2_sha256.verify(password, self.Password)
	
	def update_password(self, password):
		self.set_password(password)
		db.session.add(self)
		db.session.commit()
		
	def commit_this(self):
		db.session.add(self)
		db.session.commit()
		
	def get_keys(self):
		return ['Email', 'Name', 'Password']

		
class Result(db.Model):
	'''
		Results table model.
	'''
	Result_ID = db.Column('Result_ID', db.Integer, primary_key=True, nullable=False )
	User_email = db.Column(db.String(256), db.ForeignKey('user.Email'), nullable=False )
	Original_value = db.Column(db.String(32), nullable=False )
	Roman = db.Column( db.Float, nullable=False)
	Base_value = db.Column(db.String(64), nullable=False )
	Date = db.Column(db.String(64), nullable=False )
	
	def __init__(self, em, val, rom, base, date):
		self.User = em
		self.Original_value = val
		self.Roman = rom
		self.Base_value = base
		self.Date = date
		
	def __repr__(self):
		return "<Result {}>".format(self.Result_ID)
	
	def commit_this(self):
		db.session.add(self)
		db.session.commit()
	
	def get_keys(self):
		return ['Result_ID', 'User', 'Original_value', 'Roman', 'Base_value', 'Date']
	