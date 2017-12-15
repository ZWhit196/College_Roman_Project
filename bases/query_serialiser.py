class Serialiser():
    
    def Serialise(self, obj):
        if obj is not None:
            serialised_results = []
            if type(obj) is list:
                obj = self.RemoveDuplicates(obj)
                for n in obj:
                    serialised_results.append( self.To_dict(n) )
            else:
                serialised_results.append( self.To_dict(obj) )
            return serialised_results
        return obj
    
    def To_dict(self, obj):
        keys = obj.get_keys()
        final_dict = {}
        for k in keys:
            final_dict[k] = getattr(obj, k)
        return final_dict
    
    def RemoveDuplicates(self, arr):
        l = []
        for result in arr:
            if type(result) is list:
                for item in result:
                    if item not in l:
                        l.append( item )
            else:
                if result not in l:
                    l.append( result )
        return l