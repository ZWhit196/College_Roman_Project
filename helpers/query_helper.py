import datetime

from models import *

from bases.query_base import QueryBase


class QueryHelper(QueryBase):
    '''
        Extends a base class for executing queries.
    
        Queries for single Tables.
    '''
    def Get_source(self, src=None):
        return self.TableQueryID( src, Sources, "SID" )
    
    def Get_client(self, cli=None):
        return self.TableQueryID( cli, Clients, "CID" )
    
    def Get_game(self, game=None):
        return self.TableQueryID( game, Games, "GID" )
    
    def Get_sentiment(self):
        return self.TableQueryID( None, Sentiment_over_time, None )
    
    def Get_semantic(self):
        return self.TableQueryID( None, Semantic_results, None )
    
    
    '''
        Filters based on string names instead of IDs.
    '''
    def Get_game_by_name(self, game=None):
        return self.TableQueryName( game, Games )
    
    def Get_client_by_name(self, cli=None):
        return self.TableQueryName( cli, Clients )
    
    def Get_source_by_name(self, src=None):
        return self.TableQueryName( src, Sources )
    
    
    '''
        Two tables joined and queried for result.
    '''
    def Get_game_by_clients(self, c=None):
        return self.TwoTableQuery( c, Games, "_clients", Clients, "CID" )

    def Get_game_by_sources(self, s=None):
        return self.TwoTableQuery( s, Games, "_sources", Sources, "SID" )
    
    def Get_sentiments_by_games(self, g=None):
        return self.TwoTableQueryDirect( g, Sentiment_over_time, Games, "GID" ) # search, Table, Linked, ID
    
    def Get_sentiments_by_sources(self, s=None):
        return self.TwoTableQueryDirect( s, Sentiment_over_time, Sources, "SID" )
    
    def Get_semantics_by_games(self, g=None):
        return self.TwoTableQueryDirect( g, Semantic_results, Games, "GID" )
    
    def Get_semantics_by_sources(self, s=None):
        return self.TwoTableQueryDirect( s, Semantic_results, Sources, "SID" )
    
    
    '''
        Three tables joined and queried for result.
    '''
    def Get_game_by_source_and_client(self, s=None, c=None):
        return self.RelationalTableQuery(c, s, Games, "_clients", "_sources", Clients, Sources, "CID", "SID")
        
    def Get_sentiments_by_game_and_source(self, g=None, s=None):
        return self.ThreeTableQuery(g, s, Sentiment_over_time, Games, Sources, "GID", "SID")
    
    def Get_semantics_by_game_and_source(self, g=None, s=None):
        return self.ThreeTableQuery(g, s, Semantic_results, Games, Sources, "GID", "SID")
    
    
    '''
        Relationship checker returns True for existing relationship.
    '''
    def Check_CG_relationship(self, c=None, g=None):
        return self.RelationshipChecker(g, c, Games, "_clients", Clients, "GID", "CID")
        
    def Check_SG_relationship(self, g=None, s=None):
        return self.RelationshipChecker(g, s, Games, "_sources", Sources, "GID", "SID")
