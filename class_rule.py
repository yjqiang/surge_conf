class BaseRule:
    NAMES = []
    
    def __init__(self, line: str):
        pass
        
    def __str__(self):
        pass
        

class CommentRule(BaseRule):
    NAMES = []
    
    def __init__(self, line: str):
        self.value = line
        
    def __str__(self):
        return self.value


class KeyValueRule(BaseRule):
    NAMES = [
        '[General]',
        '[MITM]',
        '[Host]',
        '[Proxy Group]',
        '[Proxy]',
        '[Replica]'
        ]
        
    def __init__(self, line: str):
        key, value = [ele.strip() for ele in line.split('=', maxsplit=1)]
        self.key = key
        self.value = value
        
    def __str__(self):
        return f'{self.key} = {self.value}'


class DefaultRule(BaseRule):
    NAMES = []
    
    def __init__(self, line: str):
        self.value = line
        
    def __str__(self):
        return self.value
        

# https://stackoverflow.com/questions/5881873/python-find-all-classes-which-inherit-from-this-one
def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return list(subclasses)


GUIED = dict()  # key 为 surge 中 group 名字(写在了 class 的类变量 NAME 里面)，value 为对应 class
DEFAULT = DefaultRule
# 列出使用特别的 class，把 name 等与之绑定
for special_class in inheritors(BaseRule):
    for name in special_class.NAMES:
        assert name not in GUIED
        GUIED[name] = special_class

