"""
Merge function for 2048 game.
"""

def slide(line):
    """
    Function that slide tiles to the front
    """
    _original_list = line
    _new_list = []
    _nr_zero = 0
    
    # count number of zero in list
    for item in _original_list:
        if item == 0:
            _nr_zero +=1
    
    # slide all non-zero value to the front    
    for item in _original_list:
        if item!=0:
            _new_list.append(item)
    
    # add all the zeros at the end
    for item in range(_nr_zero):
        _new_list.append(0)
    
    # return new list
    return _new_list

def combine(line):
    """
    Function that combine adjust value if they are the same
    """
    _original_list = line
    _new_list = _original_list
    
    # find paired tiles
    item = 0
    while item <=(len(_original_list)-1):
        if item<=(len(_original_list)-2):
            if _original_list[item]==_original_list[item+1]:
                _new_list[item] = _original_list[item]*2
                _new_list[item+1] = 0
                item += 2
            else:
                _new_list[item] = _original_list[item]
                item +=1               
        else:
            _new_list[item] = _original_list[item]
            item +=1
    
    return _new_list

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    _original_list = line
    _new_list = []
  
    _new_list = slide(_original_list)
    _new_list = combine(_new_list)        
    _new_list = slide(_new_list)
    
    # return new list
    return _new_list

