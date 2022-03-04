import class_rule


class Delete:
    def __init__(self, group_name: str, value: list):
        # group_name = [[匹配模式, param_name, param_value], [删除几个]]
        num = value[-1][0]
        pattern, self.param_name, self.param_value = value[0]
        self.num = num
        self.type = class_rule.GUIED.get(group_name, class_rule.DEFAULT)
        
        assert pattern in ['in', 'equal']
        self.match = self._match_in if pattern == 'in' else self._match_equal
        
        self.group_name = group_name
    
    def _match_in(self, rule) -> bool:
        return self.param_value in getattr(rule, self.param_name)

    def _match_equal(self, rule) -> bool:
        return self.param_value == getattr(rule, self.param_name)
        
    # 仅删除一个
    def operate(self, conf: dict):
        cur = conf[self.group_name]
        

        count = 0
        for i, line in enumerate(cur):
            if isinstance(line, self.type) and self.match(line):
                del cur[i]
                count += 1
        if self.num == -1:
            return 
        assert count == self.num
        

class Replace:
    def __init__(self, group_name: str, value: list):
        # group_name = [[匹配模式, param_name, param_value], [str new_line], ]
        self.type = class_rule.GUIED.get(group_name, class_rule.DEFAULT)
        pattern, self.param_name, self.param_value = value[0]
        self.new_line = value[1][0]
        
        assert pattern in ['in', 'equal']
        self.match = self._match_in if pattern == 'in' else self._match_equal
        
        self.group_name = group_name
    
    def _match_in(self, rule) -> bool:
        return self.param_value in getattr(rule, self.param_name)

    def _match_equal(self, rule) -> bool:
        return self.param_value == getattr(rule, self.param_name)
        
    def operate(self, conf: dict):
        count = 0
        the_list = conf[self.group_name]
        for index, line in enumerate(the_list):
            if isinstance(line, self.type) and self.match(line):
                the_list[index] = self.type(self.new_line)
                count += 1
        assert count == 1
        

class Addition:
    def __init__(self, group_name: str, value: list):
        # group_name = [[str new_line], ]
        self.new_line = class_rule.GUIED.get(group_name, class_rule.DEFAULT)(value[0][0])
        self.group_name = group_name
        
    def operate(self, conf: dict):
        conf[self.group_name].insert(0, self.new_line)  # 加在最前面
