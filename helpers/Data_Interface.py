from bases import query_base
from models import User, Result


class Interface(query_base.QueryBase):
    '''
        Basic class to interact with the db.
    '''
    
    def Create_new_user(self, e, n, p):
        new_user = User(e, n, p)
        if new_user is not None:
            new_user.commit_this()
            
    def Update_password(self, u, p):
        u.update_password(p)
        
    def Create_result(self, nm, d, vals):
        res = Result(nm, vals.get("Value"), vals.get("Roman"), vals.get("Base_value"), d)
        res.commit_this()

    def Get_all_data(self):
        
        
        
        return None
    