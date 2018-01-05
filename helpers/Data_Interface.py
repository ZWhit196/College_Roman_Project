import datetime

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
    
    
    def Get_stats_data(self):
        # Set 1: top 5 numerals by volume - group by numeral - limit(5)
        tops = self.TableTopX( "Roman", "Result", 5 )
        vals = []
        counts = []
        for x in tops:
            vals.append(x[0])
            counts.append(x[1])
        tops = {"values": vals, "counts": counts}
        # Set 2: past week usage chart - today ... today minus week - all()
        now = datetime.datetime.now()
        vols = []
        dates = []
        for x in range(7,-1,-1):
            d = (now - datetime.timedelta( days=x )).strftime("%d/%m/%Y")
            q = self.TableQueryName( d, Result, "Date" )
            vols.append( len(q) )
            dates.append( d )
        weeks = { "volumes": vols, "dates": dates } 
        # Return
        return {"top5":tops,"weekUse":weeks}
    
    
    def Get_all_data(self, lim, page=0):
        # All database data paged - 20 per page
        d = self.TablePagedResult( Result, lim, page*lim )
        for r in d:
            r['User'] = self.Serialise( r['User'], nolist=True )
            r['User'].pop("Password")
        return d
        