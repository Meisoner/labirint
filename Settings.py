class Settings:
    def __init__(self, file):
        self.mdict = dict()
        with open(file) as f:
            for i in f.read().split('\n'):
                s, arg = i.split()
                if arg.isnumeric():
                    self.mdict[s] = int(arg)
                elif arg.replace('.', '').isnumeric():
                    self.mdict[s] = float(arg)
                else:
                    self.mdict[s] = arg

    def __getattr__(self, k):
        if k in self.mdict.keys():
            return self.mdict[k]
        return None