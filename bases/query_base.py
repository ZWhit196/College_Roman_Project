from bases.query_serialiser import Serialiser 
from models import *


class QueryBase(Serialiser):
    '''
        Base class for query execution. 
        
        Provided with a Table and optional criteria, the search will 
        return one or multiple results.
    '''
    def __repr__(self):
        return "<Basic DB Interface Object>"
    
    
    # SINGLE TABLE QUERYING
    def TableQueryID(self, search, Table, ID):
        '''
            Search a Table by the ID(s).
        '''
        if search is not None:
            if type(search) is list:
                if len(search) > 1:
                    final = []
                    for id in search:
                        final.append( self.Serialise( Table.query.filter( getattr(Table, ID)==id) ).first() )
                    return final
                return self.Serialise( Table.query.filter( getattr(Table, ID)==search[0] ).first() )
            return self.Serialise( Table.query.filter( getattr(Table, ID)==search ).first() )
        return self.Serialise( Table.query.all() )
    
    def TableQueryName(self, search, Table, Name='Name'):
        '''
            Search a Table by the Name(s).
        '''
        if search is not None:
            if type(search) is list:
                if len(search) > 1:
                    final = []
                    for name in search:
                    	final.append( self.Serialise( Table.query.filter( getattr(Table, Name)==name ).first() ) )
                    return final
                return self.Serialise( Table.query.filter( getattr(Table, Name)==search[0] ) )
            else:
                ret = self.Serialise( Table.query.filter( getattr(Table, Name)==search ).first() )
                if ret is not None:
                    return ret[0]
                return ret
        return None
    
    
    # DOUBLE TABLE QUERYING
    def TwoTableQuery(self, search, Table, Link, Linked, ID, TID=None, Tsearch=None):
        '''
            Search tables which are linked.
        '''
        if search is not None:
            item_list = []
            for id in search:
                if TID is not None:
                    obj = Table.query.join( getattr(Table, Link) ).filter( getattr(Linked, ID)==id, getattr(Table, TID)==Tsearch ).all()
                else:
                    obj = Table.query.join( getattr(Table, Link) ).filter( getattr(Linked, ID)==id ).all()
                item_list.append( obj )
            return self.Serialise( item_list )
        return None
    
    def TwoTableQueryDirect(self, search, Table, Linked, ID, TID=None, Tsearch=None):
        '''
            As TwoTableQuery, but has direct Table join instead
            of association table.
        '''
        if search is not None:
            item_list = []
            for id in search:
                if TID is not None:
                    obj = Table.query.join( Linked ).filter( getattr(Linked, ID)==id, getattr(Table, TID)==Tsearch ).all()
                else:
                    obj = Table.query.join( Linked ).filter( getattr(Linked, ID)==id ).all()
                item_list.append( obj )
            return self.Serialise( item_list )
        return None
    
    # TRIPLE TABLE QUERYING
    def RelationalTableQuery(self, search_1, search_2, Table, Link_1, Link_2, Linked_1, Linked_2, ID_1, ID_2):
        '''
            Three linked tables via association table searched with IDs provided.
        '''
        if search_1 is not None and search_2 is not None:
            item_list = []
            for s_1 in search_1:
                for s_2 in search_2:
                    obj = Table.query.join( getattr(Table,Link_1) ).join( getattr(Table,Link_2) ).filter( getattr(Linked_1,ID_1)==s_1, getattr(Linked_2,ID_2)==s_2 ).first()
                    if obj is not None:
                        item_list.append( obj )
            return self.Serialise( item_list )
        return None
        
    def ThreeTableQuery(self, search_1, search_2, Table, Linked_1, Linked_2, ID_1, ID_2):
        '''
            Three linked table searched with IDs provided.
        '''
        if search_1 is not None and search_2 is not None:
            item_list = []
            for id_1 in search_1:
                for id_2 in search_2:
                    obj = Table.query.join( Linked_1 ).join( Linked_2 ).filter( getattr(Linked_1,ID_1)==id_1, getattr(Linked_2,ID_2)==id_2 ).all()
                    if obj is not None:
                        item_list.append( obj )
            return self.Serialise( item_list )
        return None
    
    # RELATIONSHIP QUERYING
    def RelationshipChecker(self, criteria_1, criteria_2, Table, Link, Linked, ID_1, ID_2):
        '''
            Checking for any existing relationship between two 
            given IDs, return True for an existing relationship.
        '''
        if criteria_1 is not None and criteria_2 is not None:
            result = Table.query.join( getattr(Table, Link) ).filter( getattr(Table, ID_1)==criteria_1[ID_1], getattr(Linked, ID_2)==criteria_2[ID_2] ).all()
            if result is not None and len(result) > 0:
                return True
        return False
    
    
    