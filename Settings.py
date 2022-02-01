# Класс, отвечающий за загрузку переменных из файла.
class Settings:
    def __init__(self, file):
        self.mdict = dict()
        with open(file) as f:
            for i in f.read().split('\n'):
                try:
                    s, arg = i.split()
                    if s == '.':
                        continue
                    if arg.isnumeric():
                        self.mdict[s] = int(arg)
                    elif arg.replace('.', '').isnumeric():
                        self.mdict[s] = float(arg)
                    else:
                        self.mdict[s] = arg
                except Exception:
                    continue

    def __getattr__(self, k):
        if k in self.mdict.keys():
            return self.mdict[k]
        return None


st = Settings('settings.txt')