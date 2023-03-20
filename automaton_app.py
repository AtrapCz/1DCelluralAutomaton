import automaton
import tkinter as tk
import time
from functools import partial

##TODO
# new screens showing population, way to stop showing it, saving it to a file (from index to index (on the left))
# first screen buttons and entries bigger

##DEFAULTS
size, wolfram, generations, interval = 81, 90, -1, 0.5

##COLOURS
BLACK, WHITE = "#ffffff", "#000000"
colors = {0: BLACK, 1: WHITE}
##white foreground: RED, BLUE, DARK_RED, DARK_BLUE, DARK_ORANGE
##black foreground: GREEN, ORANGE, DARK_GREEN
RED, GREEN, BLUE, ORANGE = "#d50000", "#00c853", "#2962ff", "#ff6d00"
DARK_RED, DARK_GREEN, DARK_BLUE, DARK_ORANGE = "#9b0000", "#009624", "#0039cb", "#c43c00"

##BOUNDRIES (MAXIMUM AND MINIMUM VALUES)
##none of the corresponding values can go OVER these max and min values (they can be equal though)
## [a little more details]
MIN_SIZE, MIN_WOLFRAM, MIN_GENERATIONS, MIN_INTERVAL = 3, 0, -1, 0
MAX_SIZE, MAX_WOLFRAM, MAX_GENERATIONS, MAX_INTERVAL = 999, 255, 5000, 3600

def validate_entry(name, index, mode):
    """
    Method called every time any of entries is edited.

    Every variable (and corresponding entries' values) is adjusted not to go outside the boundries specified below.
    Boundries: 3 < (int)size < 999, 0 <= (int)wolfram < 256, 0 <= (float)generations, 0 <= (float)interval
    """
    try:
        if name == 'size':
            val = iv_size.get()
            if val < 0 and val > 3:
                #iv_size.set(abs(val))
                val = abs(val)
            elif val > 0 and val < 3:
                #iv_size.set(3)
                val = 3
            elif val > 999:
                iv_size.set(999)
                val = 999

            global size
            size = val
        elif name == 'wolfram':
            val = iv_wolfram.get()
            if val < 0:
                #iv_wolfram.set(abs(val))
                val = abs(val)
            elif val > 255:
                #iv_wolfram.set(255)
                val = 255
            
            global wolfram
            wolfram = val
        elif name == 'generations':
            val = iv_generations.get()
            if val < 0:
                #iv_generations.set(0)
                val = 0

            global generations
            generations = val
        elif name == 'interval':
            val = iv_interval.get()
            if val < 0:
                #iv_interval.set(0)
                val = 0

            global interval
            interval = val
        
        #print(name, index, mode, val)
    except tk.TclError as tcle:
        tcle = str(tcle)
        if name == 'size':
            ##if entry is empty (i.e. error message says: 'expected floating-point number but got ""' <=> space between "" is 0) 
            ## sets entry to default value
            ##else if entry has invalid characters in it (e.g. letters, "-")
            ## entry is set to last correct value
            if len(tcle[tcle.find('"')+1:tcle.rfind('"')]) == 0:
                #iv_size.set(3)
                #global size
                size = 3
            else:
                iv_size.set(size)
                
        elif name == 'wolfram':
            ##analogically to size
            if len(tcle[tcle.find('"')+1:tcle.rfind('"')]) == 0:
                #iv_wolfram.set(0)
                #global wolfram
                wolfram = 0
            else:
                iv_wolfram.set(wolfram)

        elif name == 'generations':
            if len(tcle[tcle.find('"')+1:tcle.rfind('"')]) == 0:
                #iv_generations.set(0)
                #global generations
                generations = 0
            else:
                iv_generations.set(generations)
            
        elif name == 'interval':
            if len(tcle[tcle.find('"')+1:tcle.rfind('"')]) == 0:
                #iv_interval.set(0)
                #global interval
                interval = 0
            else:
                iv_interval.set(interval)
            
        #print(tcle[tcle.find('"')+1:tcle.rfind('"')])

    #print(size, wolfram, generations, interval)

def adjust_first_generation(name, index, mode):
    """
    Method called every time size is changed in `size`'s entry.

    Uses global variables (size, firstgenerationframe, first_generation, buttons_first_generation).

    If new size is larger than `size` vaiable: 
     `first_generation` is extended by zeros in a number of the difference between new size and previous size,
     new buttons (in a number of the difference between new size and previous size) are created and added to `buttons_first_generation` list.
    Else, if new size is smaller than `size` variable:
     a number (difference between previous size and new size) of elements is subtracted from `first_generation`,
     a number (difference between previous size and new size) of buttons is destroyed, thus deleted from `buttons_first_generation`.
    """
    try:
        new_size = iv_size.get()
        global size
    except tk.TclError:
        global size
        new_size = size

    if new_size < 3:
        new_size = 3
    
    global firstgenerationframe, first_generation, buttons_first_generation
    
    if len(first_generation) == 0:
        first_generation = [0]*new_size
        first_generation[new_size//2] = 1
        buttons_first_generation = [tk.Button(firstgenerationframe, text=first_generation[i], command=partial(first_generation_button_change, i), background=colors[first_generation[i]], foreground=colors[not first_generation[i]], name=str(i)) for i in range(new_size)]
        [button.grid(column=i, row=0) for button, i in zip(buttons_first_generation, range(len(buttons_first_generation)))]
    elif size < len(first_generation):
        first_generation = first_generation[:new_size]
        [button.destroy() for button in buttons_first_generation[new_size:]]
        buttons_first_generation = buttons_first_generation[:new_size]
    elif size > len(first_generation):
        first_generation.extend([0]*(new_size-len(first_generation)))
         
        for i in range(len(buttons_first_generation), new_size):
            firstgenerationframe.columnconfigure(i, weight=1)
            buttons_first_generation.append(tk.Button(firstgenerationframe, text=first_generation[i], command=partial(first_generation_button_change, i), background=colors[first_generation[i]], foreground=colors[not first_generation[i]], name=str(len(buttons_first_generation))))
            buttons_first_generation[-1].grid(column=len(buttons_first_generation), row=0)

    size = new_size

def first_generation_button_change(name):
    """
    Method is called when any of the buttons from `buttons_first_generation` is pressed.

    Changes a value from 0 to 1 or from 1 to 0 in the `first_generation` list, than changes value and colour of the button under index `name` in `buttons_first_generation` list.
    """
    first_generation[name] = not first_generation[name]
    buttons_first_generation[name].configure(text=first_generation[name], background=colors[first_generation[name]], foreground=colors[not first_generation[name]])

def first_generation_buttons_pattern_change(name):
    pass

def start_population():
    """
    Method called after START button is clicked.

    Creates new window in which scrallable frame is created and filled with new population's generations.
    """
    def window_destroy(pop, nw):
        all_populations.remove(pop)
        nw.destroy()

    global size, wolfram, generations, interval, first_generation, all_populations

    population = automaton.Population(first_generation, wolfram)
    all_populations.append(population)

    new_window = tk.Toplevel(root)
    new_window.protocol("WM_DELETE_WINDOW", partial(window_destroy, population, new_window))

    new_window.title(f'Population-{size}-{wolfram}')
    new_window.geometry("600x700")

    new_window_mainframe = tk.Frame(new_window)
    new_window_mainframe.grid_columnconfigure(0, weight=1)
    new_window_mainframe.rowconfigure(0, weight=1)
    new_window_mainframe.rowconfigure(1, weight=2)

    new_window_buttonframe = tk.Frame(new_window_mainframe)
    new_window_buttonframe.grid(columns=0, row=0, columnspan=1)

    button_stop, button_prev, button_next = tk.Button(new_window_buttonframe, text="STOP", command=population.stop_iteration, background=RED, activebackground=DARK_RED, ), tk.Button(new_window_buttonframe, text="PREV", background=ORANGE, activebackground=DARK_ORANGE, foreground=BLACK), tk.Button(new_window_buttonframe, text="NEXT", background=ORANGE, activebackground=DARK_ORANGE, foreground=BLACK)
    button_stop.grid(column=0, row=0, sticky=tk.LEFT)
    button_next.grid(column=1, row=0, sticky=tk.RIGHT)
    button_prev.grid(column=2, row=0, sticky=tk.RIGHT)

    populationframe = tk.Scrollbar(new_window_mainframe, orient=tk.VERTICAL)
    populationframe.grid(column=0, row=1)
    populationframe.columnconfigure(0, weight=1, pad=5)
    populationframe.columnconfigure(1, weight=2)

    fill_width = generations
    if generations <= 0:
        fill_width = MAX_GENERATIONS
    tk.Label(populationframe, text=str(1).rjust(fill_width)).grid(column=0, row=0)

    new_window_mainframe.pack(fill='both')

    for gen in population:
        if len(population) > generations or len(population) > MAX_GENERATIONS:
            population.stop_iteration()
        tk.Label(populationframe, text=str(len(population)).rjust(fill_width)).grid(column=0, row=len(population))

        [tk.Label(populationframe, text=str(i), background=colors[i], foreground=colors[not i]).grid(column=1, row=len(population)) for i in gen]
        time.sleep(interval)

##The main window `root` is partitioned into three frame objects: `entry_frame`, `buttonframe`, `firstgenerationframe`
##All of them are placed in a `mainframe` which fills the whole main window (`root`)
##Contents of every frame couting from top:
## `entryframe` - (first part) holds 4 labels and 4 corresponding entries,
## `buttonframe` - (second, middle, part) holds a button to start the population (and two other GET RID OF THEM), 
## `firstgenerationframe` - (third part) holds a bunch (their number is `size`) of buttons representing first generation.
##
##
root = tk.Tk()

root.geometry("900x300")
root.title("Game of life")

iv_size, iv_wolfram, iv_generations, iv_interval = tk.IntVar(root, size, "size"), tk.IntVar(root, wolfram, "wolfram"), tk.IntVar(root, generations, "generations"), tk.DoubleVar(root, interval, "interval")
iv_size.trace_add("write", adjust_first_generation)
iv_size.trace_add("write", validate_entry)
iv_wolfram.trace_add("write", validate_entry)
iv_generations.trace_add("write", validate_entry)
iv_interval.trace_add("write", validate_entry)

## most top frame
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=2)
mainframe.columnconfigure(0, weight=1)

entryframe = tk.Frame(mainframe, padx=5)
entryframe.grid(column=0, row=0)
entryframe.rowconfigure(0, weight=1)
entryframe.rowconfigure(1, weight=1)
[entryframe.columnconfigure(i, weight=1) for i in range(4)]

label_size, label_wolfram, label_generations, label_interval = tk.Label(entryframe, text="Size"), tk.Label(entryframe, text="Wolfram code"), tk.Label(entryframe, text="Generations"), tk.Label(entryframe, text="Time interval")
entry_size, entry_wolfram, entry_generations, entry_interval = tk.Entry(entryframe, textvariable=iv_size), tk.Entry(entryframe, textvariable=iv_wolfram), tk.Entry(entryframe, textvariable=iv_generations), tk.Entry(entryframe, textvariable=iv_interval)

[label.grid(column=i, row=0, padx=2) for label, i in zip([label_size, label_wolfram, label_generations, label_interval], range(4))]
[entry.grid(column=i, row=1, padx=2) for entry, i in zip([entry_size, entry_wolfram, entry_generations, entry_interval], range(4))]

## middle frame
buttonframe = tk.Frame(mainframe)
buttonframe.grid(column=0, row=1, pady=5)

button_start = tk.Button(buttonframe, text="START", command=start_population, background=GREEN, activebackground=DARK_GREEN, )
button_start.grid(column=0, row=0, columnspan=3)

## third frame
firstgenerationframe = tk.Frame(mainframe)
firstgenerationframe.grid(column=0, row=2, padx=5)
[firstgenerationframe.columnconfigure(i, weight=1) for i in range(size)]

first_generation = []
buttons_first_generation = []

adjust_first_generation('size', '', 'write')

all_populations = []

mainframe.pack(fill="both")
root.mainloop()