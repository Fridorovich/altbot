import json
import re

class NumberValue:
    def __init__(self, st):
        self.value = int(st)
        if self.value < 0 or self.value > 100: raise Exception()
    
class CountryValue:
    def __init__(self, st):
        self.value = re.sub(r"[^а-яА-ЯёЁ\s\-']", "", st)

    def deserialize(self):
        return self.value.split()
    
class CurrencyValue:
    def __init__(self, st):
        self.value = re.sub(r"[^а-яА-ЯёЁ\s\-']", "", st)