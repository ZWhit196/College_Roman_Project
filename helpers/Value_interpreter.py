import roman

class Translator:
    
    RESULT = {}
    
    # Conversion
    def From_ten(self, x, b):
        """
        Converts given number x, from base 10 to base b 
        x -- the number in base 10
        b -- base to convert
        """
        assert(x >= 0)
        assert(1< b < 37)
        r = ''
        import string
        while x > 0:
            r = string.printable[x % b] + r
            x //= b
        return r
    
    def To_ten(self, x, b):
        """
        Converts given number x, from base b to base 10
        x -- string representation of number
        b -- base of given number
        """
        assert(1 < b < 37)
        return int(x, b)
    
    def From_a_to_b(self, x, a, b):
        """
        Converts x from base a to base b
        """
        return self.From_ten(self.To_ten(x, a), b)
    
    def To_roman(self, v):
        try:
            if v == 5000:
                return "MMMMM"
            return roman.toRoman(v)
        except:
            return None
        
    def From_roman(self, v):
        try:
            if v == "MMMMM":
                return 5000
            return roman.fromRoman(v)
        except:
            return None
    
    # Translation
    def _Determine_base(self, v):
        '''
        Determine what the base value of a value is
        '''
        if v is None or v == "":
            return None
        if type(v) is str:
            bases = {"0b": 2, "0o": 8, "0x": 16}
            if v[:2] in bases:
                b = bases.get( v[:2] )
            else:
                b = "Roman"
            self.RESULT['Base_value'] = str(b)
            return b
        elif type(v) is int:
            self.RESULT['Base_value'] = str(10)
            return 10
        return None
    
    def Evaluate_value(self, v):
        b = self._Determine_base(v)
        if b is not None:
            if b != 10 and b != "Roman": # X base to base 10, then to Roman
                self.RESULT['Value'] = str(v)
                r = self.To_roman( self.To_ten(v, b) )
                if r is None: 
                    return None
                self.RESULT['Roman'] = r
                
            elif b == "Roman": # Roman to base 10
                self.RESULT['Roman'] = v.upper()
                r = self.From_roman(v.upper())
                if r is None:
                    return None
                self.RESULT['Value'] = str( r )
                 
            else: # Base 10 to Roman
                self.RESULT['Value'] = str(v)
                r = self.To_roman(v)
                if r is None:
                    return None
                self.RESULT['Roman'] = r
            
            return self.RESULT
        else:
            return None
        
        
        