from os import scandir

import toml

import parse
import setting
import class_filter_conf


if __name__ == "__main__":
    conf = dict()
    
    for path in [setting.DOWNLOAD_PATH, setting.ADD_PATH]:
        for entity in scandir(path):
            conf.update(parse.parse(entity.path))
    
    with open(f'{setting.CONF_PATH}/filter.toml', 'r', encoding='utf8') as f:
        filter = toml.load(f)
    
    for control, values in filter['replace'].items():
        for value in values:
            replace = class_filter_conf.Replace(control, value)
            replace.operate(conf)
    
    for control, values in filter['delete'].items():
        for value in values:
            delete = class_filter_conf.Delete(control, value)
            delete.operate(conf)
    
    for control, values in filter['addition'].items():
        for value in values:
            addition = class_filter_conf.Addition(control, value)
            addition.operate(conf)
            
    parse.write(conf, '0.conf', filter['sort_keys'])
