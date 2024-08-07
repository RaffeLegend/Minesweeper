from define import *

# define Mine
class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._around_mine_count = -1
        self._status = NORMAL
        self.set_value(value)

    def __repr__(self):
        return str(self._value)
    
    def get_x(self):
        return self._x
    
    def set_x(self, x):
        self._x = x
    
    x = property(fget=get_x, fset=set_x)
    
    def get_y(self):
        return self._y
    
    def set_y(self, y):
        self._y = y
    
    y = property(fget=get_y, fset=set_y)
    
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        if value:
            self._value = 1
        else:
            self._value = 0
    
    value = property(fget=get_value, fset=set_value, doc='0:非地雷 1:雷')
    
    def get_around_mine_count(self):
        return self._around_mine_count
    
    def set_around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count
    
    around_mine_count = property(fget=get_around_mine_count, fset=set_around_mine_count, doc='四周地雷数量')
    
    def get_status(self):
        return self._status
    
    def set_status(self, value):
        self._status = value
    
    status = property(fget=get_status, fset=set_status, doc='BlockStatus')
