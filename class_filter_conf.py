import class_rule


class Delete:
    def __init__(self, group_name: str, value: list):
        # group_name = [[匹配模式, param_name, value], [类型(单数或者复数)]]
        # 单数表示就删一个，复数表示多个
        class_name = value[-1][0]
        pattern, self.param_name, self.param_value = value[0]
        if class_name[-1] == 's':
            self.type = class_rule.CLASSES[class_name[:-1]]
            self.operate = self._delete_all
        else:
            self.type = class_rule.CLASSES[class_name]
            self.operate = self._delete_one
        
        assert pattern in ['in', 'equal']
        self.match = self._match_in if pattern == 'in' else self._match_equal
        
        self.group_name = group_name
    
    def _match_in(self, orig) -> bool:
        return self.param_value in getattr(orig, self.param_name)

    def _match_equal(self, orig) -> bool:
        return self.param_value == getattr(orig, self.param_name)
        
    def _delete_one(self, conf: dict):
        cur = conf[self.group_name]

        count = 0
        for i, line in enumerate(cur):
            if isinstance(line, self.type) and self.match(line):
                del cur[i]
                count += 1
        assert count == 1
        
    def _delete_all(self, conf: dict):
        conf[self.group_name] = [ele for ele in conf[self.group_name] if not (isinstance(ele, self.type) and self.match(ele))]
        

class Replace:
    def __init__(self, group_name: str, value: list):
        # group_name = [[param_name, value], [new_param_name, new_value], [类型(单数)]]
        self.type = class_rule.CLASSES[value[-1][0]]
        self.param_name, self.value = value[0]
        self.new_param_name, self.new_value = value[1]
        
        self.group_name = group_name
        
    def operate(self, conf: dict):
        count = 0
        for line in conf[self.group_name]:
            if isinstance(line, self.type) and getattr(line, self.param_name) == self.value:
                setattr(line, self.new_param_name, self.new_value)
                count += 1
        assert count == 1


class Addition:
    def __init__(self, group_name: str, value: list):
        # group_name = [[str value], [类型(单数)]]
        self.value = class_rule.CLASSES[value[-1][0]](value[0][0])
        self.group_name = group_name
        
    def operate(self, conf: dict):
        conf[self.group_name].insert(0, self.value)  # 加在最前面
