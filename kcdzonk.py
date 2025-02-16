import tkinter as tk 
import random
from itertools import combinations

#helper funcs for scoring

def score_selection(dice_tuple, memo={}):
    
    """

    A sorted tuple of dice (the user-selected ones),
    return the max score  if the dice can be completely partitioned
    into valid scoring combinations. Return None if no full partition
    exists
 
    """
    
    if dice_tuple in memo:
        return memo[dice_tuple]
    if not dice_tuple:
        return 0
    
    best = None
    dice_list = list(dice_tuple)
    n = len(dice_list)
    
    #check if matches exactly
    if n == 6 and sorted(dice_list) == [1, 2, 3, 4, 5, 6]:
        best = 1500
    if n == 5:
        if sorted(dice_list) == [1, 2, 3, 4, 5]:
            best = 500 if best is None else max(best, 500)
        if sorted(dice_list) == [2, 3, 4, 5, 6]:
            best == 750 if best is None else max(best, 750)
            
# three-of-a-kind

    for num in range(1, 7):
        if dice_list.count(num) >=3:
            new_list = list(dice_list)
            for _ in range(3):
                new_list.remove(num)
            triple_score = 1 if num == 1 else num * 100
            sub_score = score_selection(tuple(sorted(new_list)), memo)
            if sub_score is not None:
                candidate = triple_score + sub_score
                best = candidate if best is None else max(best, candidate)
                
#indscoring dice (1 or 5 ind)

    if 1 in dice_list:
        new_list = list(dice_list)
        new_list.remove(1)
        sub_score = score_selection(tuple(sorted(new_list)), memo)
        if sub_score is not None:
            candidate= 100 + sub_score
            best = candidate if best is None else max(best, candidate)
    if 5 in dice_list:
        new_list = list(dice_list)
        new_list.remove(5)
        sub_score = score_selection(tuple(sorted(new_list)), memo)
        if sub_score is not None:
            candidate = 50 + sub_score
            best = candidate if best is None else max (best, candidate)
            
    memo[dice_tuple] = best
    return best

def any_valid_subset(roll):
    
    """returns True if any non-empty subset of the rolled dice (list or ints) forms a valid scoring combination
    """
    
    n = len(roll)
    for r in range(1, n+1):
        for subset in combinations(roll, r):
            if score_selection(tuple(sorted(subset))) is not None:
                return True
    return False

#Game state vars

current_dice =[]    # current dice values (only for inplay)
active_dice_count = 6 # how many dice rolled (starts with 6)
turn_score = 0 # score gathered for turn
overall_score = 0 # overall game score

# UI block

root = tk.Tk()
root.title("Sir Ivan's amazing kostky")

#dicebox frame

dice_frame = tk.Frame(root)
dice_frame.pack(pady=10)

#make 6 dices with numbers and check buttons

dice_labels = []
dice_check_vars = []
dice_checkbuttons = []
for i in range(6):
    frame = tk.Frame(dice_frame, relief="groove", bd=2, padx=10, pady=10)
    frame.grid(row=0, column=i, padx=5)
    lbl = tk.Label(frame, text="", font=("Helvetica", 20), width=2, fg="black", bg="lightgray")
    lbl.pack()
    var = tk.BooleanVar()
    #command to check update_selection_buttons to enable scoring buttons
    chk = tk.Checkbutton(frame, variable=var, command=lambda: update_selection_buttons())
    chk.pack()
    dice_labels.append(lbl)
    dice_check_vars.append(var)
    dice_checkbuttons.append(chk)

#message label for game info
message_label = tk.Label(root, text="Click 'Roll!' to start!", font=("Helvetica", 14))
message_label.pack(pady=5)

#turn and overall score labels

turn_score_label = tk.Label(root, text="Turn Score: 0", font=("Helvetica", 12))
turn_score_label.pack()
overall_score_label = tk.Label(root, text="Overall Score: 0", font=("Helvetica", 12))
overall_score_label.pack(pady=5)

#clear overall score button

def clear_overall_score():
    """Clears overall score and updates display"""
    global overall_score
    overall_score = 0
    overall_score_label.config(text="Overall Score: 0")
    message_label.config(text="Overall score cleared. You may start a new turn")
    # disable clear overall score button until the turn is ended with Save and pass
    clear_score_button.config(state="disabled")
    
clear_score_button = tk.Button(root, text="Clear Overall score", font=("Helvetica", 12), state="disabled", command=clear_overall_score)
clear_score_button.pack(pady=5)

#buttons frame

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)
roll_button = tk.Button(buttons_frame, text="Roll!", font=("Helvetica", 14), width=12, command=lambda: roll_dice())
roll_button.grid(row=0, column=0, padx=5)
hold_button = tk.Button(buttons_frame, text="Hold and continue", font=("Helvetica", 12), width=16, state="disabled", command=lambda: hold_and_continue())
hold_button.grid(row=0, column=1, padx=5)
save_button = tk.Button(buttons_frame, text="Save and pass", font=("Helvetica", 12), width=15, state="disabled", command=lambda: save_and_pass())
save_button.grid(row=0, column=2, padx=5)

#game logic

def roll_dice():
    #roll all active dice and update the UI. Check for a bust (no score combo)
    global current_dice, active_dice_count, turn_score
    # roll active_dice_count
    current_dice = [random.randint(1,6) for _ in range(active_dice_count)]
    
    #update dice UI boxes (only first active_dice_count boxes are used)
    for i in range(6):
        if i < active_dice_count:
            dice_labels[i].config(text=str(current_dice[i]), bg="lightgray", fg="black")
            dice_check_vars[i].set(False)
            dice_checkbuttons[i].config(state="normal")
        else:
            dice_labels[i].config(text="")
            dice_checkbuttons[i].config(state="disabled")
            
    #disable scoring until selection is made
    hold_button.config(state="disabled")
    save_button.config(state="disabled")
    
    #check if the roll contains any valid scoring subset
    
    if not any_valid_subset(current_dice):
        message_label.config(text="Kurwa!")
        #reset turn, clear score and restore available dice
        root.after(1500, reset_turn)
    else:
        message_label.config(text="Select dice to score and choose decision!")
        
def update_selection_buttons():
    """Enables the Hold/Save buttons of at least one active dice is selected"""
    selected = any(dice_check_vars[i].get() for i in range(active_dice_count))
    if selected:
        hold_button.config(state="normal")
        save_button.config(state="normal")
    else:
        hold_button.config(state="disabled")
        save_button.config(state="disabled")
def hold_and_continue():
    """Validates the user's selection. If valid adds the selected dice's points to the turn score and remove dice. Remaining dice (if any) will be re-rolled."""
    global current_dice, active_dice_count, turn_score
    selected_values = []
    remaining_values = []
    for i in range(active_dice_count):
        if dice_check_vars[i].get():
            selected_values.append(current_dice[i])
        else:
            remaining_values.append(current_dice[i])
    
    valid_score = score_selection(tuple(sorted(selected_values)))
    if valid_score is None:
        message_label.config(text="No valid combination selected!")
        return
    turn_score += valid_score
    turn_score_label.config(text=f"Turn score: {turn_score}")
    
    #prepare for next roll: remaining dice become active
    
    active_dice_count = len(remaining_values)
    current_dice = remaining_values[:]
    
    #clear checkbuttons
    for i in range(6):
        dice_check_vars[i].set(False)
    
    hold_button.config(state="disabled")
    save_button.config(state="disabled")
    
    #if all dice were scored, player get all 6 dice back
    if active_dice_count == 0:
        active_dice_count = 6
        
    message_label.config(text="Dice held. Click 'Roll!' to roll remaining dice.")
    #optionally clear the dice display until next roll
    for i in range(6):
        if i < active_dice_count:
            dice_labels[i].config(text="")
        else:
            dice_labels[i].config(text="")
            
def save_and_pass():
    """Validates user's selection and if valid add it's score add the turn total to the overrall score then end the turn"""
    global current_dice, active_dice_count, turn_score, overall_score
    selected_values = []
    for i in range(active_dice_count):
        if dice_check_vars[i].get():
            selected_values.append(current_dice[i])
    valid_score = score_selection(tuple(sorted(selected_values)))
    if valid_score is None:
        message_label.config(text="No valid combination selected!")
        return
    
    turn_score += valid_score
    turn_score_label.config(text=f"Turn score: {turn_score}")
    
    overall_score += turn_score
    overall_score_label.config(text=f"Overall score: {overall_score}")
    
    message_label.config(text="Turn ended. Click 'Roll!' to start a new turn!")
    #enables  clear pverall button
    clear_score_button.config(state="normal")
    # print("Save and pass executed: Clear Overall Score button enabled.") #debug

    reset_turn()
    
def reset_turn():
    """Resets the turn, clear turn score, restore active dice pool to 6 and clear dice display"""
    global current_dice, active_dice_count, turn_score
    turn_score = 0
    turn_score_label.config(text="Turn score: 0")
    active_dice_count = 6
    current_dice = []
    for i in range(6):
        dice_labels[i].config(text="", bg="white")
        dice_check_vars[i].set(False)
        dice_checkbuttons[i].config(state="disabled")
    hold_button.config(state="disabled")
    save_button.config(state="disabled")
    
    #Tkinter event loop
    
root.mainloop()