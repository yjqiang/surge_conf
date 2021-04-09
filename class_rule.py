class Base:
    NAMES = []
    
    def __init__(self, line: str):
        pass
        
    def __str__(self):
        pass
        

class Comment(Base):
    NAMES = []
    
    def __init__(self, line: str):
        self.value = line
        
    def __str__(self):
        return self.value


class KeyValue(Base):
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


class Rule(Base):
    NAMES = [
        '[Rule]',
        ]
    
    def __init__(self, line: str):
        # Each rule consists 3 parts
        # rule type, a traffic matcher (except for FINAL rule), and a proxy policy
        rule_type, matcher, policy = [ele.strip() for ele in line.split(',')]
        self.rule_type = rule_type
        self.matcher = matcher
        self.policy = policy
            
    def __str__(self):
        return f'{self.rule_type}, {self.matcher}, {self.policy}'
        
        
class UrlRewrite(Base):
    NAMES = ['[URL Rewrite]']
    
    def __init__(self, line: str):
        # The rewrite rule consists 3 parts
        # regular expression, replacement and type.
        exp, replacement, rule_type = [ele.strip() for ele in line.split()]
        self.rule_type = rule_type
        self.exp = exp
        self.replacement = replacement
        
    def __str__(self):
        return f'{self.exp} {self.replacement} {self.rule_type}'
        

class HeaderRewrite(Base):
    NAMES = ['[Header Rewrite]']
    
    def __init__(self, line: str):
        # The rewrite rule consists 4 parts
        # URL regular expression, action type, header field and value.
        results = [ele.strip() for ele in line.split(maxsplit=3)]
        assert len(results) == 3 or len(results) == 4
        if len(results) == 4:
            exp, rule_type, field, value = results
        else:
            exp, rule_type, field, value = *results, None
        self.rule_type = rule_type
        self.exp = exp
        self.field = field
        self.value = value
        
    def __str__(self):
        if self.value is not None:
            return f'{self.exp} {self.rule_type} {self.field} {self.value}'
        return f'{self.exp} {self.rule_type} {self.field}'
        

class Default(Base):
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
CLASSES = dict()  # key 为 class 名字，value 为对应 class
DEFAULT = Default
# 列出使用特别的 class，把 name 等与之绑定
for special_class in inheritors(Base):
    CLASSES[special_class.__name__] = special_class
    for name in special_class.NAMES:
        assert name not in GUIED
        GUIED[name] = special_class

