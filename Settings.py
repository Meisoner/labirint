class Settings:
    def __init__(self, file):
        with open(file) as f:
            for i in f.read().split('\n'):
                s, arg = i.split()
                if arg.isnumeric():
                    setattr(self, s, int(arg))
                elif arg.replace('.', '').isnumeric():
                    setattr(self, s, float(arg))
                else:
                    setattr(self, s, arg)