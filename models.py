from Database import db

from flask import request
from passlib.hash import pbkdf2_sha256


class User():
	id = db.Column('UID', db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.Text)
	
	# functions to handle the password
    def set_password(self, password):
        '''
        hashes and salts a new password
        '''
        self.password = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        db.session.add(self)
        db.session.commit()

    def verify_password(self, password):
        '''
        verifies a password
        '''
        return pbkdf2_sha256.verify(password, self.password)

    def update_password(self, password):
        '''
        sets and saves a password
        '''
        self.set_password(password)
        db.session.add(self)
        db.session.commit()


		
# MODIFY AS NEEDED



Client_games = db.Table('Client_games',
    db.Column('CID', db.Integer, db.ForeignKey('clients.CID'), primary_key=True ),
    db.Column('GID', db.Integer, db.ForeignKey('games.GID'), primary_key=True )
)
  
  
Games_sources = db.Table('Games_sources',
    db.Column('SID', db.Integer, db.ForeignKey('sources.SID'), primary_key=True ),
    db.Column('GID', db.Integer, db.ForeignKey('games.GID'), primary_key=True )
)


class Clients(db.Model):
    '''
        Clients table model.
    '''
    CID = db.Column('CID', db.Integer, primary_key=True)
    Name = db.Column(db.String(256), nullable=False)
    _games = db.relationship('Games', secondary=Client_games, backref=db.backref('Client_games', lazy='dynamic'), lazy='dynamic', primaryjoin='Client_games.c.CID==Clients.CID', secondaryjoin='Client_games.c.GID==Games.GID' )
    
    def __init__(self, name):
        self.Name = name
        
    def __repr__(self):
        return '<Client:{}>'.format(self.Name)
    
    def get_keys(self):
        return ['CID', 'Name']


class Sources(db.Model):
    '''
        Sources table model.
    '''
    SID = db.Column('SID', db.Integer, primary_key=True)
    Name = db.Column(db.String(256), nullable=False)
    _Sentiments = db.relationship('Sentiment_over_time', backref='Sources', primaryjoin='Sources.SID==Sentiment_over_time.Source' )
    _games = db.relationship('Games', secondary=Games_sources, backref=db.backref('Games_sources', lazy='dynamic'), lazy='dynamic', primaryjoin='Games_sources.c.SID==Sources.SID', secondaryjoin='Games_sources.c.GID==Games.GID' )
    
    def __init__(self, name):
        self.Name = name
        
    def __repr__(self):
        return '<Source:{}>'.format(self.Name)
    
    def get_keys(self):
        return ['SID', 'Name']
        
        
class Games(db.Model):
    '''
        Games table model.
    '''
    GID = db.Column('GID', db.Integer, primary_key=True)
    Name = db.Column(db.String(256), nullable=False)
    Franchise = db.Column(db.String(256), nullable=False)
    Release_date = db.Column(db.String(256), nullable=False)
    _Semantics = db.relationship('Semantic_results', backref='Games', primaryjoin='Games.GID==Semantic_results.GID' )
    _Sentiments = db.relationship('Sentiment_over_time', backref='Games', primaryjoin='Games.GID==Sentiment_over_time.GID' )
    _clients = db.relationship('Clients', secondary=Client_games, backref=db.backref('Client_games', lazy='dynamic'), lazy='dynamic', primaryjoin='Client_games.c.GID==Games.GID', secondaryjoin='Client_games.c.CID==Clients.CID' )
    _sources = db.relationship('Sources', secondary=Games_sources, backref=db.backref('Games_sources', lazy='dynamic'), lazy='dynamic', primaryjoin='Games_sources.c.GID==Games.GID', secondaryjoin='Games_sources.c.SID==Sources.SID' )
    
    def __init__(self, name, fran, date):
        self.Name = name
        self.Franchise = fran
        self.Release_date = date
        
    def __repr__(self):
        return '<Game:{}>'.format(self.Name)
        
    def get_keys(self):
        return ['GID', 'Name', 'Franchise', 'Release_date']
        

class Semantic_results(db.Model):
    '''
        Semantic_results table model.
    '''
    SemanticID = db.Column('SemanticID', db.Integer, primary_key=True)
    GID = db.Column(db.Integer, db.ForeignKey('games.GID') )
    Start_date = db.Column(db.String(64), nullable=False)
    End_date = db.Column(db.String(64), nullable=False)
    Type = db.Column(db.String(128), nullable=False)
    Contents = db.Column(db.String(128), nullable=False)
    Alternatives = db.Column(db.String(256), nullable=False)
    Semantic = db.Column(db.String(64), nullable=False)
    Category = db.Column(db.String(128), nullable=False)
    Occurences = db.Column(db.Integer, nullable=False)
    Sentiment = db.Column(db.Float, nullable=False)
    Source = db.Column(db.Integer, db.ForeignKey('sources.SID'), nullable=True)
    
    def __init__(self, gid, sdate, edate, stype, cont, alts, sem, cat, occ, sent, src=None ):
        self.GID = gid
        self.Start_date = sdate
        self.End_date = edate
        self.Type = stype
        self.Contents = str(cont)
        self.Alternatives = str(alts)
        self.Semantic = sem
        self.Category = cat
        self.Occurences = occ
        self.Sentiment = sent
        self.Source = src
        
    def __repr__(self):
        return '<Semantic:{}>'.format(self.SemanticID)
    
    def get_keys(self):
        return ['SemanticID', 'GID', 'Start_date', 'End_date', 'Type', 'Contents', 'Alternatives', 'Category', 'Occurences', 'Sentiment', 'Source' ]
    
    
class Sentiment_over_time(db.Model):
    '''
        Sentiment_over_time table model.
    '''
    SentimentID = db.Column('SentimentID', db.Integer, primary_key=True, nullable=False )
    GID = db.Column(db.Integer, db.ForeignKey('games.GID'), nullable=False )
    Sentiment_score = db.Column( db.Float, nullable=False)
    Source = db.Column(db.Integer, db.ForeignKey('sources.SID'), nullable=False )
    Start_date = db.Column(db.String(64), nullable=False )
    End_date = db.Column(db.String(64), nullable=False )
    Period_type = db.Column(db.String(64), nullable=False)
    
    def __init__(self, gid, score, source, start, end, period):
        self.GID = gid
        self.Sentiment_score = score
        self.Source = source
        self.Start_date = start
        self.End_date = end
        self.Period_type = period
        
    def __repr__(self):
        return '<Sentiment:{}>'.format(self.SentimentID)
    
    def get_keys(self):
        return ['SentimentID', 'GID', 'Sentiment_score', 'Source', 'Start_date', 'End_date', 'Period_type']
    