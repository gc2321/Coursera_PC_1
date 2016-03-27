"""
Cookie Clicker Simulator
"""
import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(10000000)
import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
           
    def __init__(self):
        self._cookies = 0.0
        self._total_cookies = 0.0       
        self._cps = 1.0
        self._time = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: %s Current Cookies: %s CPS: %s Total Cookies: %s History (length: %s): %s" % (self.get_time(), self.get_cookies(), self.get_cps(), self.get_total_cookies(), len(self._history), self.get_history())
          
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        """
        return self._cookies
    
    def get_total_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        """
        return self._total_cookies
    
    def get_cps(self):
        """
        Get current CPS
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        _history_copy = list(self._history)
        return _history_copy

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """  
        if cookies > 0 or cookies >= self._cookies:
            time = math.ceil((cookies-self._cookies)/self._cps)
            if time <=0:
                time = 0.0
            return time
            
        else:
            return 0.0
                
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time >0:
            self._time += time
            self._cookies += self._cps*time
            self._total_cookies += self._cps*time
                
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies >= cost:
            self._cookies -= cost
            self._cps += additional_cps
            self._history.append((self.get_time(), item_name, cost, self.get_total_cookies()))
            #self._history.append((self.get_time(), item_name, cost, self.get_cookies(), self.get_total_cookies()))
            print "Time:%s Item:%s Cost:%s CPS:%s Cookies:%s Total:%s " %(self.get_time(), item_name, cost, self.get_cps(), self.get_cookies(), self.get_total_cookies())
      
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    item = build_info.clone()
    state = ClickerState()

    while state.get_time() <= duration:
        time_remain = duration - state.get_time()
        buy = strategy(state.get_cookies(), state.get_cps(), state.get_history(), time_remain, item)
        if buy == None:
            break
        if state.time_until(item.get_cost(buy)) > time_remain:
            break 
        else:          
            state.wait(state.time_until(item.get_cost(buy)))
            state.buy_item(buy, item.get_cost(buy), item.get_cps(buy))
            item.update_item(buy)
    
    # wait for the time_remain
    state.wait(time_remain)
    print "Total Cookies :"+ str(state.get_total_cookies())
    return state
    
def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_list =[]
    buy = None
    
    for each in build_info.build_items():
        item_list.append([each, build_info.get_cost(each)])
    
    item_list.sort(key = lambda x: x[1])
    
    affort = cookies + (cps*time_left)
    
    for each in item_list:
        if affort >= each[1]:
            buy = each[0]
            break
    
    return buy
   
def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    item_list =[]
    buy = None
    
    for each in build_info.build_items():
        item_list.append([each, build_info.get_cost(each)])
    
    item_list.sort(key = lambda x: x[1], reverse=True)
    
    affort = cookies + (cps*time_left)
    
    for each in item_list:
        if affort >= each[1]:
            buy = each[0]
            break

    return buy
    
def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    
    item_list =[]
    
    for each in build_info.build_items():
        item_list.append([each, build_info.get_cps(each)/build_info.get_cost(each)])
    
    item_list.sort(key = lambda x: x[1], reverse=True)
    buy = item_list[0][0]
    
    return buy
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    
    print "get_time, item_name, cost, cps, cookies, total_cookies"
    print strategy_name, ":"
    print state
    
    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history1 = [(item[0], item[3]) for item in history]
    #history2 = [(item[0], item[4]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history1], True, ["CPS"])
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history1, history2], True, ["Cookies", "Total"])

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("None", SIM_TIME, strategy_none)
    
    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()

