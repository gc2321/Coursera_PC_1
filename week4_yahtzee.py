"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)
import random

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.    
    hand: full yahtzee hand
    Returns an integer score 
    """
    _score ={1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    for item in hand:
        _score[item] += item
    _max = max(_score.values())
    return _max

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    _dice =[]
    _outcome=()
    for _ in range(num_die_sides):
        _dice.append(_+1)
    _outcome = tuple(_dice)    
    
    #generate list of combination of free dice
    _combo = set()
    _combo = gen_all_sequences(_outcome, num_free_dice)
    
    # obtain score for each dice combination    
    _total=0
    
    for _ in _combo:
        held_and_free =[]
        held_and_free_tuple =()
        
        for each in held_dice:
            held_and_free.append(each)
                
        for each in _:
            held_and_free.append(each)
            
        held_and_free_tuple = tuple(held_and_free)
        _total += score(held_and_free_tuple)*1.0
    _total2 =  _total/(len(_combo) *1.0)
    
    return _total2

#print expected_value((1,), 6, 1)
#print expected_value((2, 2), 6, 1)
#print expected_value((2, 4), 6, 3)
#print expected_value((5, 5), 6, 4)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    ans = set([()])
    total =set([()])
    length =len(hand)
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in hand:
                new_seq = list(seq)
                new_seq.append(item)
                new_seq.sort()
                #print new_seq
                total.add(tuple(new_seq))
                temp.add(tuple(new_seq))
        ans = temp
    
    total2=set(total)
    for each_set in total:
        for item in each_set:
            if each_set.count(item)>hand.count(item):
                total2.remove(each_set)
                break
                
    return total2
   
def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hand_dict ={}
    total_hand = gen_all_holds(hand)
    for each in total_hand:
        hand_dict[each]= expected_value(each, num_die_sides, len(hand)-len(each))
    
    _max = max(hand_dict.values())
    max_key=[]
    for key, value in hand_dict.items():
        if value==_max:
            max_key.append(key)
            
    return (_max, random.choice(max_key))

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 6, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



