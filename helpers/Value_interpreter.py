import roman

class Value_interpreter:
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
    
    def To_ten(self, s, b):
        """
        Converts given number s, from base b to base 10
        s -- string representation of number
        b -- base of given number
        """
        assert(1 < b < 37)
        return int(s, b)
    
    def Convert_a_to_b(self, s, a, b):
        """
        Converts s from base a to base b
        """
        return self.From_ten(self.To_ten(s, a), b)
    
    def Determine_base(self, v):
        if type(v) is str:
            bases = {"0b": "2", "0o": "8", "0x": "16", "123456789": "10", "IVXLCDM": "Roman"}
            
            return b
        return None