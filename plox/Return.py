

class Return(RuntimeError):
    def __init__(self,value):
        self.value = value
        super().__init__()
