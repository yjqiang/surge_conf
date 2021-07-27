import re

import class_rule


def parse(path: str) -> dict:
    conf = {}
    with open(path, encoding='utf8') as f:
        for line in f:
            line = line.strip()
                        
            if re.fullmatch(r'\[[a-zA-Z ]+\]', line):
                name = line
                conf[name] = []
            # 注释
            elif not line or (line[:2] == '//' or line[0] == '#'):
                conf[name].append(class_rule.Comment(line))
            elif name in class_rule.GUIED:
                conf[name].append(class_rule.GUIED[name](line))
            else:
                conf[name].append(class_rule.DEFAULT(line))
                print(name, line)
    
    return conf
    

def write(conf: dict, path: str, sort_keys: list) -> None:
    with open(path, 'w', encoding='utf8') as f:
        for key in sort_keys:
            f.write(f'{key}\n')
            if key in conf:
                for line in conf[key]:
                    f.write(f'{line}\n')
            f.write('\n')

