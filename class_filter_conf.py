import class_rule


class Delete:
    def __init__(self, group_name: str, value: list):
        # group_name = [[匹配模式, param_name, param_value], [class_rule 类型(单数或者复数)]]
        # 单数表示就删一个，复数表示多个
        class_name = value[-1][0]
        pattern, self.param_name, self.param_value = value[0]
        if class_name[-1] == 's':
            self.type = class_rule.CLASSES.get(class_name[:-1], class_rule.DEFAULT)
            self.operate = self._delete_all
        else:
            self.type = class_rule.CLASSES.get(class_name, class_rule.DEFAULT)
            self.operate = self._delete_one
        
        assert pattern in ['in', 'equal']
        self.match = self._match_in if pattern == 'in' else self._match_equal
        
        self.group_name = group_name
    
    def _match_in(self, orig) -> bool:
        return self.param_value in getattr(orig, self.param_name)

    def _match_equal(self, orig) -> bool:
        return self.param_value == getattr(orig, self.param_name)
        
    # 仅删除一个
    def _delete_one(self, conf: dict):
        cur = conf[self.group_name]
        

        count = 0
        for i, line in enumerate(cur):
            if isinstance(line, self.type) and self.match(line):
                del cur[i]
                count += 1

        assert count == 1
        
    # 管他三七二十一全删了
    def _delete_all(self, conf: dict):
        conf[self.group_name] = [ele for ele in conf[self.group_name] if not (isinstance(ele, self.type) and self.match(ele))]
        

class Replace:
    def __init__(self, group_name: str, value: list):
        # group_name = [[匹配模式, param_name, param_value], [str new_line], [class_rule 类型(单数)]]
        self.type = class_rule.CLASSES.get(value[-1][0], class_rule.DEFAULT)
        pattern, self.param_name, self.param_value = value[0]
        self.new_line = value[1][0]
        
        assert pattern in ['in', 'equal']
        self.match = self._match_in if pattern == 'in' else self._match_equal
        
        self.group_name = group_name
    
    def _match_in(self, orig) -> bool:
        return self.param_value in getattr(orig, self.param_name)

    def _match_equal(self, orig) -> bool:
        return self.param_value == getattr(orig, self.param_name)
        
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
        # group_name = [[str new_line], [class_rule 类型(单数)]]
        self.new_line = class_rule.CLASSES.get(value[-1][0], class_rule.DEFAULT)(value[0][0])
        self.group_name = group_name
        
    def operate(self, conf: dict):
        conf[self.group_name].insert(0, self.new_line)  # 加在最前面
