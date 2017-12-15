from models import User, Result

class DBInterface:
    '''
        Basic class to interact with the db and clean out some 
        of the router file.
    '''
    
    def Create_new_user(self, e, n, p):
        new_user = User(e, n, p)
        if new_user is not None:
            new_user.commit_this()
            
    def Update_password(self, u, p):
        u.update_password(p)
        
    