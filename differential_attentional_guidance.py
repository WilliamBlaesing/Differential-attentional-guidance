# The experiment is based on experiment 1A in Eastwood, Smilek, & Merikle (2001)

from psychopy import event, gui, core, visual, monitors
import os
import pandas as pd
import time
import random
import numpy as np
import logging
from typing import Union, Optional, Tuple, List, Dict, Any
   

# !!!Enter your monitor setting here before running the code!!!
my_monitor = monitors.Monitor("")
my_monitor.setWidth(53.5)                               # Enter the physical width of your monitor in centimeters. 
my_monitor.setSizePix([1920, 1080])                     # Enter the screen resolution in pixels (width, height).

pix_per_cm = my_monitor.getSizePix()[0] / my_monitor.getWidth()
height_cm = my_monitor.getSizePix()[1] / pix_per_cm


# Modify these values in case the sizes of different elements need to be adjusted. (Note: The unit is centimeters.)
spacing = 2.12                                # Distance between the calculated positions
text_height = 0.5                             # Height of the text
stim_size = 1.3                               # Diameter of the targets, distractors and size of the rectangles

# The numbers added as comments below reflect the amount of training trials, that have to be answered correctly and the trails per condition that will be used when testing subjects.
# For the sake of testing, lower trial numbers are advised. Feel free to play around with the amount of rows, columns, trials and the set sizes (under the noted constraints).
# Depending on the screen size the spacing and stim_size might need adjustments to fit everything on the screen for more rows or columns.
rows = 6                                     # Rows and cols numbers will be used to generate a rows times cols matrix for the possible stimulus locations.
cols = 6                                     # Valid values for cols and rows range from 1 to 9. Higher values would require modifications to the input collection.
set_sizes = [7, 11, 15, 19]                  # Set sizes (amount of items); neither value should exceed the amount of possible positions (cols * rows)
training_set_size = 3                        # Set size for training phase
training_trials = 4                          # 2
target_states = ["positive", "negative"]     # Possible target types (emotional expressions)
trials_per_condition = 30                    # 2

continue_key = "b"                           # Key to advance the instruction page, display next stimulus display and signaling target has been found.
return_key = "v"                             # Key to go back to the previous instruction page.

# Dictionary for the GUI
info = {
        "age": "",
        "sex": ["Male", "Female"], 
        "sub_id": "", 
        "vision": ["normal", "corrected-to-normal"], 
        "handedness": ["left", "right"]
        }

color = (0.8, 0.8, 0.8)
color2 = (0.8, -0.8, -0.8)

# Timings
feedback_delay = 0.5
feedback_duration = 1
skip_prot = 0.5                             # Delay to avoid accidental skipping of instruction or block messages. If annoying, set it to 0.


instruction = [
                "Willkommen zum Experiment!"
                "\n\nLesen Sie sich diese Instruktion bitte sorgfältig durch:"
                f"\n\nJeder Durchgang dieses Experiments beginnt damit, dass Sie ein '{continue_key.upper()}' sehen, das Sie aufordert die Taste '{continue_key.upper()}' zu drücken."
                "\n\nDaraufhin wird Ihnen eine Auswahl von schematischen Gesichtern (Smileys) an zufälligen Positionen auf dem Bildschirm angezeigt."
                "\n\nDabei gibt es immer genau einen Smiley, der von allen anderen Smileys abweicht."
                f"\n\nIhre erste Aufgabe ist es diesen einen abweichenden Smiley so schnell wie möglich zu finden und die Taste '{continue_key.upper()}' zu drücken, wenn Sie den Smiley gefunden haben."
                f"\n\nDrücken Sie die Taste '{continue_key.upper()}' um fortzufahren ...",

                "Danach wird ein Raster über alle möglichen Positionen gelegt, dessen Zeilen und Reihen nummeriert sind."
                "\n\nIhre zweite Aufgabe ist es dann zuerst die Zeile und danach die Spalte des Rasters anzugeben, an der sich dieser eine abweichende Smiley auf dem Bildschirm befunden hat."
                f"\n\nNutzen Sie dazu die Tasten '1' bis '{max(rows,cols)}' auf der Tastatur. Hierbei kommt es nicht darauf an so schnell wie möglich zu antworten!"
                "\n\nArbeiten Sie dabei aber bitte so genau wie möglich."
                "\n\nAls Hilfestellung, ob gerade die Zeile oder Spalte angegeben werden soll, wird die jeweilige Nummerierung farblich hervorgehoben."
                f"\n\nDrücken Sie die Taste '{continue_key.upper()}' um fortzufahren ..."
                f"\n\nDrücken Sie '{return_key.upper()}' um zurückzugehen ...",

                "Nachdem Sie die Zeile und Spalte eingegeben haben, erhalten Sie eine Rückmeldung ob Sie richtig geantwortet haben oder nicht."
                f"\n\nDazu erscheint die Aufforderung die Taste '{continue_key.upper()}' zu drücken um das nächste Display, auf das Sie reagieren sollen, anzuzeigen."
                f"\n\nDamit Sie so schnell wie möglich antworten können legen Sie bitte einen Finger auf die Taste '{continue_key.upper()}' und lassen diesen auf der Taste liegen."
                f"\n\nDrücken Sie die Taste '{continue_key.upper()}' um fortzufahren ..."
                f"\n\nDrücken Sie '{return_key.upper()}' um zurückzugehen ...",

                "Zwischen einzelnen Versuchsdurchgängen oder Blöcken können Sie nach Bedarf Pausen einlegen."
                "\n\nBevor das eigentliche Experiment beginnt, gibt es einige Probedurchgänge."
                "\n\nIn den Probedurchgängen wird Ihnen in der oberen Bildschirmmitte eine zusätzliche Hilfestellung angezeigt."
                "\n\nDiese wird es im eigentlichen Experiment nicht mehr geben."
                "\n\nViel Erfolg!"
                f"\n\nWenn Sie die Instruktionen verstanden haben, drücken Sie die Taste '{continue_key.upper()}' um mit den Probedurchgängen zu beginnen ..."
                f"\n\nDrücken Sie '{return_key.upper()}' um zurückzugehen ..."
]



# Functions  
def present_text(win: visual.Window, 
                 text: str, 
                 pos: Tuple[float, float] = (0, 0), 
                 height: float = text_height,
                 textColor: Union[str, Tuple[float, float, float]] = color, 
                 flip: bool = False) -> None:
    """
    Draws a text stimulus in a window and optionally flips the window to make the text visible.

    Parameters
    ----------
    win : visual.Window
        The window where the text stimulus will be presented.
    text : str
        The text content to be displayed.
    pos : tuple, optional
        The (x, y) position where the text will be drawn. Defaults to (0, 0), the center of the screen.
    height: float, optional
        The text height in centimeters. Defaults to the global text_height variable.
    textColor : str or list, optional
        The color of the text. Defaults to the global "color" variable.
    flip : bool, optional
        If True, the window will be flipped after drawing the text, making it visible on the screen. Defaults to False.
    """

    text = visual.TextStim(
        win,
        units = "cm",
        height = height,
        color = textColor,
        pos = pos,  
        text = text
    )
    text.draw()

    if flip:
        win.flip()



def present_instructions(win: visual.Window, 
                         instructions: List[str], 
                         continue_key: str, 
                         return_key: str) -> None:
    """
    Displays a sequence of instructions on the screen and allowing the user to navigate through them using specified keys.

    Parameters
    ----------
    win : visual.Window
        The window where the instructions will be presented.
    instructions : list of str
        A list of instruction strings to be displayed, one at a time.
    continue_key : str
        The key that advances to the next instruction in the sequence.
    return_key : str
        The key that returns to the previous instruction, allowing the user to review.
    """

    current_instr = 0

    while current_instr < len(instructions):

        present_text(win, 
                     text = instructions[current_instr],
                     flip = True)
        
        logging.info(f"Presenting instruction {current_instr + 1}")
        core.wait(skip_prot)

        key = event.waitKeys(keyList = [continue_key, return_key])

        if continue_key in key:
            current_instr += 1

        elif return_key in key:
            if current_instr > 0:
                current_instr -= 1



def arc_vertices(radius: float, 
                 start_angle: float, 
                 end_angle: float) -> List[Tuple[float, float]]:
    """
    Helper function to create vertices for a circular arc given a radius and angular range, 
    that are used for the mouth of the smiley stimuli, which will be the targets.

    Parameters
    ----------
    radius : float
        The radius of the arc (distance from the center).
    start_angle : float
        The starting angle of the arc, in degrees.
    end_angle : float
        The ending angle of the arc, in degrees.

    Returns
    -------
    arc : list of tuple
        A list of (x, y) vertices representing the arc in Cartesian coordinates.
    """
    
    # Converting degrees to radians, because the linspace function won't take degrees as a unit
    start_rad = np.deg2rad(start_angle)
    end_rad = np.deg2rad(end_angle)
    
    # Calculates angles between start and end_rad
    angles = np.linspace(start_rad, 
                         end_rad, 
                         25) 
    
    # Calculates the Cartesian coordinates for every angle
    arc = [(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles]

    return arc



def preload_stimuli(win: visual.Window, 
                    set_size: int) -> List[Dict[str, Any]]:
    """
    Preloads a list of smiley stimuli built out of circles and shapes, which can be both targets or 
    distractors. These will be reused across trials with just their position and expression beeing updated
    by another function.

    Parameters
    ----------
    win : visual.Window
        The window where the stimuli will be displayed.
    set_size : int
        The number of smiley stimuli to preload. This defines the number of visual elements that will be created and stored.

    Returns
    -------
    stimuli : list of dict
        A list of dictionaries where each dictionary contains the visual components (head, eyes, mouth) of a smiley face.
    """

    try:
        radius_head = stim_size / 2
        radius_eye = stim_size * 0.0577
        mouth_radius = stim_size * 0.2885
        line_width_cm = stim_size * 0.0577
        line_width_pix = line_width_cm * pix_per_cm                # Necessary because lineWidth only takes pix as a unit
        
        positive_mouth_vertices = arc_vertices(mouth_radius, 
                                               195, 
                                               345)
        
        negative_mouth_vertices = arc_vertices(mouth_radius, 
                                               15, 
                                               165)
    
        stimuli = []
        for _ in range(set_size):

            stimulus = {
                "head": visual.Circle(win = win, 
                                    lineColor = color, 
                                    fillColor = None, 
                                    radius = radius_head,
                                    lineWidth = line_width_pix),

                "left_eye": visual.Circle(win = win, 
                                        lineColor = color, 
                                        fillColor = color, 
                                        radius = radius_eye),

                "right_eye": visual.Circle(win = win, 
                                        lineColor = color, 
                                        fillColor = color, 
                                        radius = radius_eye),

                "mouth_positive": visual.ShapeStim(win = win, 
                                                vertices = positive_mouth_vertices, 
                                                lineWidth = line_width_pix, 
                                                lineColor = color, 
                                                closeShape = False),

                "mouth_negative": visual.ShapeStim(win = win, 
                                                vertices = negative_mouth_vertices, 
                                                lineWidth = line_width_pix, 
                                                lineColor = color, 
                                                closeShape = False),

                "mouth_neutral": visual.Line(win = win, 
                                            start = (0, 0), 
                                            end = (0, 0), 
                                            lineWidth = line_width_pix, 
                                            lineColor = color)
            }
            stimuli.append(stimulus)

        logging.info(f"Preloaded {set_size} stimuli")
        return stimuli

    except Exception as e:
        logging.error(f"Error preloading stimuli: {e}")
    


def calculate_positions(win: visual.Window, 
                        rows: int, 
                        cols: int) -> List[Tuple[float, float]]:
    """
    Calculates and returns a list of rows times cols (x, y) positions in a rectangular grid, spacing value, 
    both on the x- and y-axis, apart from each other and centered on the screen, 
    that will be used as positions for the stimulus presentation and localization task.

    Parameters
    ----------
    win : visual.Window
        The Window!
    rows : int
        The number of rows in the grid.
    cols : int
        The number of columns in the grid.

    Returns
    -------
    positions : list of tuple
        A list of (x, y) coordinates for each position in the grid.
    """

    try:
        screen_width_cm = win.size[0] / pix_per_cm
        screen_height_cm = win.size[1] / pix_per_cm

        grid_width = (cols - 1) * spacing
        grid_height = (rows - 1) * spacing

        offset_x = (screen_width_cm - grid_width) / 2
        offset_y = (screen_height_cm - grid_height) / 2

        positions = []

        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * spacing - (screen_width_cm / 2)
                y = offset_y + row * spacing - (screen_height_cm / 2)
                positions.append((x, y))

        logging.info(f"{len(positions)} positions calculated")

        return positions
    
    except Exception as e:
        logging.error(f"Error calculating positions for {rows} rows and {cols} columns: {e}")



def draw_stimulus(stimulus: Dict[str, Any], 
                  expression: str, 
                  pos: Tuple[float, float]) -> None:
    """
    Updates the position and expression of a preloaded smiley stimulus and draws it.

    Parameters
    ----------
    stimulus : dict
        A dictionary representing the smiley stimulus containing all the parts.
    expression : str
        The emotional expression of the stimulus. Should be either "positive", "negative", or "neutral".
    pos : tuple
        The (x, y) position on the screen where the stimulus will be displayed.
    """

    eye_x_offset = stim_size * 0.1538
    eye_y_offset = stim_size * 0.1923
    mouth_length = stim_size * 0.2885
    mouth_neu_offset = stim_size * 0.1154
    mouth_neg_offset = stim_size * 0.3077
    mouth_pos_offset = stim_size * 0.0192

    stimulus["head"].pos = pos
    stimulus["head"].draw()

    stimulus["left_eye"].pos = (pos[0] - eye_x_offset, pos[1] + eye_y_offset)
    stimulus["left_eye"].draw()

    stimulus["right_eye"].pos = (pos[0] + eye_x_offset, pos[1] + eye_y_offset)
    stimulus["right_eye"].draw()

    if expression == "positive":
        stimulus["mouth_positive"].pos = (pos[0], pos[1] + mouth_pos_offset)
        stimulus["mouth_positive"].draw()

    elif expression == "negative":
        stimulus["mouth_negative"].pos = (pos[0], pos[1] - mouth_neg_offset)
        stimulus["mouth_negative"].draw()

    else:
        stimulus["mouth_neutral"].start = (pos[0] - mouth_length, pos[1] - mouth_neu_offset)
        stimulus["mouth_neutral"].end = (pos[0] + mouth_length, pos[1] - mouth_neu_offset)
        stimulus["mouth_neutral"].draw()



def load_rectangles(win: visual.Window,
                    positions: List[Tuple[float, float]]) -> None:
    """
    Creates a rectangle for every positions.

    Parameters
    ----------
    win: visual.Window
        THe window the rectangles will be displayed in.
    positions : list of tuple
        A list of (x, y) coordinates representing the grid positions.
    """
    try:
        rectangles = []

        rect_size = stim_size

        for pos in positions:
            rectangle = visual.Rect(
                win = win,
                units = "cm",
                size = (rect_size, rect_size),
                fillColor = color,
                pos = pos
                )
            rectangles.append(rectangle)

        logging.info(f"{len(rectangles)} rectangles loaded")
        return rectangles
    
    except Exception as e:
        logging.info(f"Error loading {len(positions)} rectangles: {e}")



def display_grid(win: visual.Window, 
                 positions: List[Tuple[float, float]], 
                 rectangles: List[visual.Rect],
                 row_color: Union[str, Tuple[float, float, float]], 
                 col_color: Union[str, Tuple[float, float, float]]) -> None:
    """
    Displays the rectangle grid at all possible positions as well as the (colored) row 
    and column numbers for the localization task.

    Parameters
    ----------
    win : visual.Window
        The window where the grid and numbers will be displayed.
    positions : list of tuple
        A list of (x, y) coordinates representing the grid positions.
    rectangles : list of visual.Rect
        A list of visual.Rect objects that will be displayed at the positions.
    row_color : str or list
        The color used for the row labels.
    col_color : str or list
        The color used for the column labels.
    """

    # Extracts the x-coordinates of the "first" row of the grid/matrix positions and 
    # displays the column numbers spacing value below the "first" row
    col_positions = [pos[0] for pos in positions[:cols]]

    for i, pos in enumerate(col_positions):
        present_text(win, 
                     text = str(i + 1), 
                     pos = (pos, positions[0][1] - spacing), 
                     textColor = col_color)

    # Extracts the y-coordinates of the "first" column of the grid/matrix positions and 
    # displays the row numbers the spacing value to the left of the "first" column
    row_positions = [pos[1] for pos in positions[::cols]]

    for i, pos in enumerate(row_positions):
        present_text(win, 
                     text = str(i + 1), 
                     pos = (positions[0][0] - spacing, pos), 
                     textColor = row_color)


    for rect in rectangles:
        rect.draw()

    win.flip()



def get_grid_response(win: visual.Window, 
                      positions: List[Tuple[float, float]],
                      rectangles: List[visual.Rect],
                      row_color: Union[str, Tuple[float, float, float]] = "White", 
                      col_color: Union[str, Tuple[float, float, float]] = "White",
                      is_training: bool = False,
                      row_response: bool = False) -> str:
    """
    Collects the participant's response for either row or column selection and displays the grid.

    Parameters
    ----------
    win : visual.Window
        The window where the grid will be displayed.
    positions : list of tuple
        The list of (x, y) positions for the grid.
    rectangles : list of visual.Rect
        A list of visual.Rect objects that will be displayed at the positions.
    row_color : str, optional
        Color of the row numbers displayed on the grid. Defaults to "White".
    col_color : str, optional
        Color of the column numbers displayed on the grid. Defaults to "White".
    is_training : bool, optional
        Whether the trial is part of a training phase. Defaults to False.
    row_response : bool, optional
        Indicates whether the response is for a row (True) or a column (False). Defaults to False.

    Returns
    -------
    str
        The row or column number as selected by the participant.
    """


    if is_training:
        if row_response:
            text = f"In welcher Reihe war der abweichende Smiley? Nutzen Sie zur Eingabe die Tasten '1' bis '{rows}'."
        else:
            text = f"In welcher Spalte war der abweichende Smiley? Nutzen Sie zur Eingabe die Tasten '1' bis '{cols}'."

        present_text(win,
                     text,
                     pos = (0, (height_cm / 2) - (spacing / 2)))
        
    display_grid(win, 
                 positions,
                 rectangles, 
                 row_color,
                 col_color)

    if row_response:
        response = event.waitKeys(keyList = [str(i) for i in range(1, rows + 1)])[0]
    
    if not row_response:
        response = event.waitKeys(keyList = [str(i) for i in range(1, cols + 1)])[0]

    return response



def run_trial(win: visual.Window, 
              set_size: int, 
              positions: List[Tuple[float, float]], 
              rectangles: List[visual.Rect],
              target_state: str,
              stimuli: List[Dict[str, Any]],
              continue_key: str,
              is_training: bool = False) -> Dict[str, Any]:
    """
    Executes a single trial in the main experiment or training phase, displaying stimuli at randomly selected positions and recording 
    the participant's responses. It presents a target with a specified emotional expression, that has to be found 
    among a specified amount of neutral distractors, then asks the participant to identify the target's position.
    Returns a dictionary with trial data, including the tested condition (target state and display size), reaction time, accuracy, 
    target location and the participant's response.

    Parameters
    ----------
    win : visual.Window
        The window where stimuli will be displayed.
    set_size : int
        The number of stimuli (target and distractors) to display during the trial.
    positions : list of tuple
        A list of (x, y) coordinates that specify the positions where stimuli will be drawn on the screen.
    rectangles : list of visual.Rect
        A list of visual.Rect objects that will be displayed at the positions.
    target_state : str
        The emotional expression of the target stimulus. Possible values are "positive" or "negative".
    stimuli : list of dict
        A preloaded list of smiley stimuli, where each dict contains the visual elements for drawing a target or distractor.
    continue_key : str
        The key that participants must press to continue to the next display.
    is_training : bool, optional
        Whether the trial is part of a training phase. Defaults to False.

    Returns
    -------
    dict
        A dictionary containing trial data:
            - "block" (int): 0.
            - "trial_num" (int): 0.
            - "set_size" (int): Number of stimuli displayed during the trial.
            - "target_state" (str): Emotional expresion of the target ("positive" or "negative").
            - "target_position" (tuple): Grid position of the target, as (row, column).
            - "reaction_time" (float): Participant's reaction time in seconds.
            - "response" (tuple): The participant's response, in terms of (row, column) position.
            - "accuracy" (bool): Whether the participant's response was correct (True/False).
    """

    try:
        help_pos = (0, (height_cm / 2) - (spacing / 2))

        target_loc = random.choice(positions)
        distractor_loc = random.sample([pos for pos in positions if pos != target_loc], set_size - 1)


        present_text(win, 
                    text = f"'{continue_key.upper()}'")

       
        if is_training:
            present_text(win, 
                        text = f"'{continue_key.upper()}' drücken um das nächste Display anzuzeigen.",
                        pos = help_pos)

        win.flip()
        event.waitKeys(keyList = continue_key)


        draw_stimulus(stimuli[0],
                      expression = target_state,
                      pos = target_loc)

        for i, loc in enumerate(distractor_loc):
            draw_stimulus(stimuli[1 + i],
                          expression = "neutral", 
                          pos = loc)
        if is_training:
            present_text(win,
                         text = f"Abweichenden Smiley so schnell wie möglich finden und wenn gefunden die Taste '{continue_key.upper()}' drücken.",
                         pos = help_pos)

        win.flip()

        clock = core.Clock()
        rt = event.waitKeys(keyList = continue_key, 
                            timeStamped = clock)[0][1]


        row_response = get_grid_response(win, 
                                        positions,
                                        rectangles,
                                        row_color = color2, 
                                        col_color = color,
                                        is_training = is_training,
                                        row_response = True)

        col_response = get_grid_response(win, 
                                        positions,  
                                        rectangles,
                                        row_color = color, 
                                        col_color = color2,
                                        is_training = is_training,)


        # Converts target's position list index into row and column numbers and checks if it matches given input
        target_index = positions.index(target_loc)
        target_row = 1 + target_index // cols
        target_col = 1 + target_index % cols

        if int(row_response) == target_row and int(col_response) == target_col:
            accuracy = True
            feedback = "Ihre Antwort ist richtig."

        else:
            accuracy = False
            feedback = "Ihre Antwort ist falsch."
        
        core.wait(feedback_delay)

        if is_training and not accuracy:
            present_text(win,
                         text = feedback + f"\n\nSie haben Reihe: {row_response} und Spalte: {col_response} geantwortet. \n\nRichtige wäre Reihe: {target_row} und Spalte: {target_col}.",
                         flip = True)
            core.wait(feedback_duration * 4)
            
        else:
            present_text(win, 
                         text = feedback,
                         flip = True)
        
            core.wait(feedback_duration)


        logging.info(f"Trial Data: RT: {rt}, ACC: {accuracy}, SIZE: {set_size}, STATE: {target_state}, LOC: {(target_row, target_col)}, RES: {(int(row_response), int(col_response))}")
        

        return {
            "block": 0,
            "trial_num": 0,
            "set_size": set_size,
            "target_state": target_state,
            "target_position": (target_row, target_col),
            "reaction_time": rt,
            "response": (int(row_response), int(col_response)),
            "accuracy": accuracy,
        }
    
    except Exception as e:
        logging.error(f"Error running trial: {e}")



def run_training(win: visual.Window, 
                 positions: List[Tuple[float, float]],
                 rectangles: List[visual.Rect],
                 training_set_size: int,
                 stimuli: List[Dict[str, Any]],
                 training_trials: int,
                 continue_key: str) -> None:
    """
    Runs the training phase of the experiment, repeating trials until the participant answers 
    the required number of trials correctly.

    Parameters
    ----------
    win : visual.Window
        The window where stimuli, grid and feedback will be presented.
    positions : list of tuple
        A list of positions for the stimuli.
    rectangles : list of visual.Rect
        A list of visual.Rect objects that will be displayed at the positions.
    training_set_size : int
        The number of stimuli to present during each training trial.
    stimuli : list of dict
        The preloaded smiley stimuli used during the training trials.
    training_trials : int
        The number of correctly answered trials required to complete training.
    continue_key : str
        The key the participant presses to continue between trials.
    """

    try:
        logging.info("Starting training phase")
        correct_train_trials = 0
        total_train_trials = 0

        unused_target_states = target_states.copy()
        random.shuffle(unused_target_states)

        while correct_train_trials < training_trials:
            if not unused_target_states:
                unused_target_states = target_states.copy() 
                random.shuffle(unused_target_states) 

            target_state = unused_target_states.pop()
            trial_data = run_trial(win, 
                                   training_set_size, 
                                   positions,
                                   rectangles,
                                   target_state,
                                   stimuli,
                                   continue_key,
                                   is_training = True)
            
            total_train_trials += 1

            if trial_data["accuracy"]:
                correct_train_trials += 1

        present_text(win, 
                    text = (f"Training erfolgreich abgeschlossen. \n\nBitte denken Sie daran einen Finger auf die Taste '{continue_key.upper()}' zu legen und so schnell wie möglich zu antworten."
                            f"\n\nDrücken Sie '{continue_key.upper()}' um das Experiment zu starten."),
                    pos = (0, 0),
                    flip = True)

        event.waitKeys(keyList = continue_key)

        logging.info(f"Training completed in {total_train_trials} trials")

    except Exception as e:
        logging.error(f"Error during training: {e}")



def get_participant_info(info: Dict[str, str]) -> Dict[str, str]:
    """
    Collects participant information using a graphical user interface.

    Parameters
    ----------
    info : dict
        A dictionary containing the fields and default values for the participant information to enter.

    Returns
    -------
    dict
        The updated dictionary with the input.
    """

    try:
        info_data = gui.DlgFromDict(title = "Supervisor Input", dictionary = info)
        if info_data.OK:
            print("Info: Data entry succesful")
            return info
        
        else:
            print("Warning: Exited setup during data input.")
            core.quit()

    except Exception as e:
        print(f"Error collecting participant info: {e}")
        core.quit()



def save_experiment_data(subject_info: Dict[str, str], 
                         trial_data: Dict[str, Any], 
                         output_file: Union[str, None] = None) -> str:
    """
    Organizes and saves the data collected during an experimental trial into a csv file. If an output file is not specified, 
    the function will create a new file in a "results" directory, located in the same directory the script is in and named according to the subject's ID. 
    If a file with the same name already exists, the function will append a timestamp to create a unique filename in order to prevent overwriting off an already existing file.

    Parameters
    ----------
    subject_info : dict
        A dictionary containing information about the participant.
    trial_data : dict
        A dictionary containing the data from an individual trial.
    output_file : str, optional
        The file path for saving the results. If None, a new file is created based on the subject's ID.
    """
    try:
        directory = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(directory, "results")
        if not os.path.exists(output_path):
            os.makedirs(output_path)


        trial_data_frame = pd.DataFrame({
            "sub_id": [subject_info["sub_id"]],
            "age": [subject_info["age"]],
            "sex": [subject_info["sex"]],
            "vision": [subject_info["vision"]],
            "handedness": [subject_info["handedness"]],
            "block": [trial_data["block"]],
            "trial": [trial_data["trial_num"]],
            "target_state": [trial_data["target_state"]],
            "set_size": [trial_data["set_size"]],
            "reaction_time": [trial_data["reaction_time"]],
            "target_position": [trial_data["target_position"]],
            "response": [trial_data["response"]],
            "accuracy": [trial_data["accuracy"]]
        })


        if output_file is None:
            output_file = os.path.join(output_path, f"results_subject_{subject_info['sub_id']}.csv")

            if os.path.exists(output_file):
                timestamp = time.strftime("%d%m%Y-%H%M%S")
                output_file = os.path.join(output_path, f"results_subject_{subject_info['sub_id']}_{timestamp}.csv")


        if not os.path.exists(output_file):
            trial_data_frame.to_csv(output_file, 
                                    index = False)

        else:
            trial_data_frame.to_csv(output_file, 
                                    mode = "a", 
                                    header = False, 
                                    index = False)
            
        logging.info(f"Data saved to {output_file}")
        return output_file
    
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")

    except PermissionError as e:
        logging.error(f"PermissionError: {e}")

    except Exception as e:
        logging.error(f"Unexpected error saving data: {e}")



def configure_logging(subject_info,
                      log_level: Optional[int] = logging.WARNING,) -> None:
    """
    Sets up logging path, file and configuration.

    Parameters
    ----------
    log_level : int, optional
        The logging level (e.g., logging.DEBUG, logging.INFO, logging.WARNING). Defaults to "logging.WARNING".
    """
    try: 
        directory = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(directory, "logs")
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        time_stamp = time.strftime("%d%m%Y-%H%M%S")
        log_file_path = os.path.join(log_path, f"log-subject_{subject_info['sub_id']}_{time_stamp}.log")
        logging.basicConfig(
                    filename = log_file_path,
                    filemode = "a",
                    format = "%(asctime)s - %(levelname)s - %(message)s",
                    level = log_level)
    
    except Exception as e:
        print(f"Error setting up logging: {e}")



def setup_experiment(info: Dict[str, str],
                     rows: int, 
                     cols: int,
                     set_sizes: List[int],
                     target_states: List[str],
                     trials_per_condition: int,
                     log_level: int) -> Tuple[Dict[str, str], visual.Window, List[Tuple[float, float]], List[Tuple[int, str]], List[Dict[str, Any]], List[visual.Rect]]:
    """
    Initializes the experiment by setting up logging, returning preloaded stimuli, participant info, a window, stimulus positions and a randomized list of trial conditions.

    Parameters
    ----------
    info : dict
        A dictionary containing the fields and default values for data that needs to be entered in the GUI.
    rows : int
        The number of rows in the grid for stimulus positions.
    cols : int
        The number of columns in the grid for stimulus positions.
    set_sizes : list of int
        A list of set sizes (number of stimuli) to be displayed in the experiment.
    target_states : list of str
        A list of possible target emotional expressions (e.g., "positive", "negative").
    trials_per_condition : int
        The number of trials to run for each combination of set size and target state.
    log_level : int
        The logging level.

    Returns
    -------
    tuple
        Returns a tuple containing the participant information, the window, stimulus positions, trial conditions, preloaded stimuli and rectangles.
    """

    subject_info = get_participant_info(info)

    configure_logging(subject_info,
                      log_level)
    try:
        win = visual.Window(
            size = my_monitor.getSizePix(),
            units = "cm",
            color = "black",
            fullscr = True,
            screen = 0,
            monitor = my_monitor)
        win.flip()

        positions = calculate_positions(win, 
                                        rows, 
                                        cols)

        trial_conditions = [(set_size, target_state) 
                            for set_size in set_sizes 
                            for target_state in target_states 
                            for _ in range(trials_per_condition)]

        random.shuffle(trial_conditions)
        logging.info(f"Generated {len(trial_conditions)} trial conditions")

        max_set_size = max(set_sizes)
        stimuli = preload_stimuli(win, 
                                  max_set_size)
        
        rectangles = load_rectangles(win,
                                     positions)

        logging.info(f"Setup completed for subject_{subject_info['sub_id']}")


        return subject_info, win, positions, trial_conditions, stimuli, rectangles
    

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")

    except PermissionError as e:
        logging.error(f"PermissionError: {e}")

    except ValueError as e:
        logging.error(f"Value error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise



def run_main_trials(subject_info: Dict[str, str], 
                    win: visual.Window,
                    trials_per_condition: int,
                    positions: List[Tuple[float, float]],
                    rectangles: List[visual.Rect], 
                    trial_conditions: List[Tuple[int, str]],  
                    stimuli: List[Dict[str, Any]],
                    continue_key: str,
                    return_key: str) -> None:
    """
    Presents the main experimental trials structured in blocks and saves the data after every trial.

    Parameters
    ----------
    subject_info : dict
        A dictionary containing the information about the participant.
    win : visual.Window
        The window where stimuli and feedback will be presented.
    trials_per_condition : int
        The number of trials for every combination of set size and target state.
    positions : list of tuple
        A list of positions for the stimuli on the screen.
    rectangles : list of visual.Rect
        A list of visual.Rect objects that will be displayed at the positions.
    trial_conditions : list of tuple
        A list of tuples representing the trial conditions (set size and target state).
    stimuli : list of dict
        The preloaded stimuli to be used during the trials.
    continue_key : str
        The key the participant presses to continue between trials and blocks.
    return_key : str
        The key to press to exit the experiment at the end.
    """

    try:
        trial_num = 1
        total_trials = len(trial_conditions)
        trials_per_block = trials_per_condition
        num_blocks = total_trials // trials_per_block

        output_file = None


        for block in range(num_blocks):
            present_text(win, 
                        text = (f"Block: {block + 1} von {num_blocks}.\
                                \n\nWenn Sie bereit sind drücken Sie '{continue_key.upper()}' um den nächsten Block zu starten."),
                        flip = True)
            core.wait(skip_prot)

            event.waitKeys(keyList = continue_key)
            logging.info(f"Starting block {block + 1}")


            for _ in range(trials_per_block):
                if not trial_conditions:
                    logging.warning(f"Trial conditions list is empty before trial {trial_num}. Exiting trial loop.")
                    break

                set_size, target_state = trial_conditions.pop(0)
                logging.info(f"Starting trial {trial_num}")

                trial_data = run_trial(win, 
                                       set_size, 
                                       positions, 
                                       rectangles,
                                       target_state,
                                       stimuli,
                                       continue_key)
                    
                trial_data["trial_num"] = trial_num
                trial_data["block"] = block + 1

                try:
                    output_file = save_experiment_data(subject_info, 
                                                        trial_data, 
                                                        output_file = output_file)
                except Exception as e:
                        logging.error(f"Error saving data for trial {trial_num}: {e}")
                   
                trial_num += 1

            logging.info(f"Block {block + 1} completed")

    except Exception as e:
        logging.error(f"Error running main trials: {e}")


    present_text(win, 
                 text = f"Das Experiment ist beendet." 
                "\n\nVielen Dank für Ihre Teilnahme!"
                "\n\nIn diesem Experiment mussten Sie Gesichter mit einem positiven oder negativen Ausdruck in Mitten von unterschiedlich vielen neutralen Gesichtern finden."
                "\n\nZiel des Experiments ist es, durch die Analyse der Reaktionszeiten, in Abhängigkeit \nvom emotionalen Ausdruck der Gesichter und der Anzahl der neutralen Gesichter, zu untersuchen, wie emotionale Gesichtsaudrücke die Aufmerksamkeitslenkung beeinflussen."
                "\n\nWir möchten herausfinden, ob negative oder positive Gesichtsausdrücke die Aufmerksamkeit unterschiedlich stark auf sich ziehen können."
                f"\n\nDrücken Sie '{return_key.upper()}' um das Fenster zu schließen.", 
                flip = True)
    
    event.waitKeys(keyList = return_key)



def run_experiment(info: Dict[str, str], 
                   rows: int, 
                   cols: int, 
                   set_sizes: List[int], 
                   target_states: List[str], 
                   trials_per_condition: int, 
                   instructions: str, 
                   continue_key: str, 
                   return_key: str, 
                   training_set_size: int,
                   training_trials: int, 
                   debug_mode: bool = False) -> None:
    """
    Runs the entire experiment by initializing the experimental environment, then proceeds to present the instructions, the training trials and main experimental trials to the participant.

    Parameters
    ----------
    info : dict
        A dictionary containing the fields and default values for GUI.
    win_size : tuple or list
        The size of the window where the experiment will be displayed.
    rows : int
        The number of rows in the grid for stimulus positions.
    cols : int
        The number of columns in the grid for stimulus positions.
    set_sizes : list of int
        A list of set sizes (number of stimuli) to be tested in the experiment.
    target_states : list of str
        A list of possible target emotional expressions.
    trials_per_condition : int
        The number of trials to run for each combination of set size and target state.
    instructions : str
        The experimental instructions to be presented to the participant.
    continue_key : str
        The key the participant presses to continue between phases.
    return_key : str
        The key the participant presses to exit the experiment at the end.
    training_set_size : int
        The number of stimuli to present during each training trial.
    training_trials : int
        The number of correct trials required to complete the training phase.
    debug_mode : bool, optional
        If True, sets the logging level to "logging.DEBUG" for more detailed logging. Defaults to False.
    """

    log_level = logging.DEBUG if debug_mode else logging.WARNING

    subject_info, win, positions, trial_conditions, stimuli, rectangles = setup_experiment(info,
                                                                                           rows,
                                                                                           cols,
                                                                                           set_sizes,
                                                                                           target_states,
                                                                                           trials_per_condition,
                                                                                           log_level)
    try:
        present_instructions(win, 
                            instructions, 
                            continue_key, 
                            return_key)

        run_training(win, 
                    positions, 
                    rectangles,
                    training_set_size,
                    stimuli,
                    training_trials,
                    continue_key)
                                                                            
        run_main_trials(subject_info, 
                        win,
                        trials_per_condition,
                        positions, 
                        rectangles,
                        trial_conditions,
                        stimuli,
                        continue_key,
                        return_key)
        
        logging.info("Experiment completed")

    except Exception as e:
        logging.critical(f"Critical error during experiment run: {e}")


    finally:
        win.close()



run_experiment(info = info,
               cols = cols,
               rows = rows,
               set_sizes = set_sizes,
               target_states = target_states,
               trials_per_condition = trials_per_condition,
               instructions = instruction,
               continue_key = continue_key,
               return_key = return_key,
               training_set_size = training_set_size,
               training_trials = training_trials,
               debug_mode = True)