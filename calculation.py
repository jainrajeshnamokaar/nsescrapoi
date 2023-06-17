from datetime import datetime


class DataSaver:
    def __init__(self, strike_price, put_io, call_io, put_change_io, call_change_io):
        self.strike_price = strike_price
        self.put_io = put_io
        self.call_io = call_io
        self.put_change_io = put_change_io
        self.call_change_io = call_change_io

    def __repr__(self):
        return f"{self.strike_price}, {(datetime.now().time())}"

    @staticmethod
    def calculate_percent_change(old_value, new_value):
        if old_value:
            return round(((new_value - old_value) / old_value) * 100, 3)
        else:
            return round(((new_value - old_value) / 1) * 100, 3)

    def __mod__(self, other):
        if isinstance(other, DataSaver) and self.strike_price == other.strike_price:
            new_value_put_io = other.put_io
            new_value_call_io = other.call_io
            new_value_put_change_io = other.put_change_io
            new_value_call_change_io = other.call_change_io

            put_percent_of_io = self.calculate_percent_change(self.put_io, new_value_put_io)
            put_percent_of_change_io = self.calculate_percent_change(self.put_change_io, new_value_put_change_io)
            call_percent_of_io = self.calculate_percent_change(self.call_io, new_value_call_io)
            call_percent_of_change_io = self.calculate_percent_change(self.call_change_io, new_value_call_change_io)
            
            return_value =     {
                "call_change_io":  "%s(%s)"%(self.call_change_io,call_percent_of_change_io), 
                "call_io":  "%s(%s)"%(self.call_io,call_percent_of_io), 
                "put_change_io": "%s(%s)"%(self.put_change_io,put_percent_of_change_io), 
                "put_io":  "%s(%s)"%(self.put_io,put_percent_of_io), 
                "strike_price": self.strike_price
                }, 
            return return_value
        else:
            raise TypeError("Operand must be of type 'DataSaver'")
