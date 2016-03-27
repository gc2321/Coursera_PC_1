"""
Clone of 2048 game.
"""

import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0), DOWN: (-1, 0), LEFT: (0, 1), RIGHT: (0, -1)}

def slide(line, val):
    """
    Function that slide tiles to the front
    """
    _original_list = line
    _new_list = []
    
    # slide all non-zero value to the front  
    if val == 1:
        for item in _original_list:       
            if item!=0:
                _new_list.append(item)
        for item in _original_list:       
            if item==0:
                _new_list.append(item)
    else:        
        for item in _original_list:
            if item==0:
                _new_list.append(item)
        for item in _original_list:
            if item!=0:
                _new_list.append(item)
                
    # return new list
    return _new_list

def combine(line, val):
    """
    Function that combine adjust value if they are the same
    """
    _original_list = line
    _new_list = _original_list
    
    # reverse list val !=1
    if val!=1:
        _original_list= _original_list[::-1]
        
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
    if val!=1:
        _new_list= _new_list[::-1]
    
    return _new_list

def merge(line, val):
    """
    Helper function that merges a single row or column in 2048
    """
    _original_list = line
    _new_list = []
  
    _new_list = slide(_original_list, val)
    _new_list = combine(_new_list, val) 
    _new_list = slide(_new_list, val)
    
    # return new list
    return _new_list
    
class TwentyFortyEight:
    """
    Class to run the game logic.
    """    
    
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = [[row + col for col in range(self._grid_width)]
                           for row in range(self._grid_height)]
        
        # make every cell = 0
        for row in range(self._grid_height):
            for column in range(self._grid_width):
                self._grid[row][column] = 0
                
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        for row in range(self._grid_height):
            for column in range(self._grid_width):
                self._grid[row][column] = 0
        
        fill_cell = 0
        while (fill_cell <2):
            self.new_tile()
            fill_cell +=1
                
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        #return str(self._grid)
        return str([x for x in self._grid]).replace("],", "]\n")
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # copy grid before move
        _grid_before = [[row + col for col in range(self._grid_width)]
                           for row in range(self._grid_height)]
        
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                _grid_before[row][col] = 0
                _grid_before[row][col] = self._grid[row][col]
     
        _direction = direction
        self._direction = OFFSETS[_direction]
        if (self._direction[1]==1 or self._direction[1]==-1):
            for row in range(self._grid_height):
                _old_list = []
                for col in range(self._grid_width):
                    
                    _old_list.append(self._grid[row][col])               
                
                if (self._direction[1]==-1): 
                    _new_list = merge(_old_list, 2)
                else:
                    _new_list = merge(_old_list, 1)
                    
                for col in range(self._grid_width):
                    self._grid[row][col] = _new_list[col]
        else: 
            for col in range(self._grid_width):
                _old_list = []
                for row in range(self._grid_height):
                    
                    _old_list.append(self._grid[row][col])               
                
                if (self._direction[0]==-1): 
                    _new_list = merge(_old_list, 2)
                else:
                    _new_list = merge(_old_list, 1)
                    
                for row in range(self._grid_height):
                    self._grid[row][col] = _new_list[row]   
              
        # compare grid before and after
        _move_happen = 0
        
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if (_grid_before[row][col] != self._grid[row][col]):
                    _move_happen +=1
        
        print "Move happen"+str(_move_happen)        
        
        # add new tile if there is a empty cell and move happened
        _empty = 0
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if (self._grid[row][col]==0):
                    _empty += 1
                    break
                
        if(_empty!=0 and _move_happen!=0):
            self.new_tile()
                                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        fill_cell = 0
        while (fill_cell <1): 
            row = random.randrange(self._grid_height)
            col = random.randrange(self._grid_width)
                     
            if (self._grid[row][col]==0):
                val = random.choice([2,2,2,2,2,2,2,2,2,4])
                self._grid[row][col] = val
                fill_cell +=1
       
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col]=value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
