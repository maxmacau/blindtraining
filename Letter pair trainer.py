import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Checkbutton, IntVar,Canvas, Scrollbar, Frame
import random
import sys
import os

def get_file_path(filename):
    if getattr(sys, '_MEIPASS', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

letter_pairs_path = get_file_path('letter_pairs_words.txt')
high_scores_path = get_file_path('high_score.txt')

print(f"Current directory: {os.getcwd()}")
print(f"Looking for file at: {letter_pairs_path}")

endless_quiz_running = False
alphabet = 'ABCDEFGHIJKLMNOPYRRSTUVWX'

def import_pairs_words(letter_pairs_path):
    pairs_words = {}
    try:
        with open(letter_pairs_path, 'r') as file:
            for line in file:
                pair, word = line.strip().split(':')
                pairs_words[pair] = word
    except FileNotFoundError:
        print(f"File not found: {letter_pairs_path}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return pairs_words

def letter_pair_toggle(alphabet, selected_pairs):
    toggle_window = tk.Toplevel()
    toggle_window.title("Letter Pair Toggle")

    canvas = tk.Canvas(toggle_window)
    scrollbar_x = tk.Scrollbar(toggle_window, orient="horizontal", command=canvas.xview)
    scrollbar_y = tk.Scrollbar(toggle_window, orient="vertical", command=canvas.yview)
    canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    pair_vars = {f"{a}{b}": tk.IntVar(value=1) for a in alphabet for b in alphabet}

    def update_selected_pairs():
        selected_pairs.clear()
        selected_pairs.update({pair for pair, var in pair_vars.items() if var.get() == 1})
        toggle_window.destroy()

    def toggle_row(letter, state):
        for b in alphabet:
            pair_vars[f"{letter}{b}"].set(state)

    def toggle_column(letter, state):
        for a in alphabet:
            pair_vars[f"{a}{letter}"].set(state)

    def select_all():
        for var in pair_vars.values():
            var.set(1)

    def clear_all():
        for var in pair_vars.values():
            var.set(0)

    for i, a in enumerate(alphabet):
        for j, b in enumerate(alphabet):
            pair = f"{a}{b}"
            tk.Checkbutton(scrollable_frame, text=pair, variable=pair_vars[pair]).grid(row=i+1, column=j+1, sticky="w")
    for i, letter in enumerate(alphabet):
        tk.Button(scrollable_frame, text=f"Row {letter}", command=lambda l=letter: toggle_row(l, 1)).grid(row=i+1, column=0)
        tk.Button(scrollable_frame, text=f"Col {letter}", command=lambda l=letter: toggle_column(l, 1)).grid(row=0, column=i+1)
    tk.Button(scrollable_frame, text="Select All", command=select_all).grid(row=len(alphabet) + 1, column=0, columnspan=len(alphabet) + 1)
    tk.Button(scrollable_frame, text="Clear All", command=clear_all).grid(row=len(alphabet) + 2, column=0, columnspan=len(alphabet) + 1)
    tk.Button(scrollable_frame, text="Apply", command=update_selected_pairs).grid(row=len(alphabet) + 3, column=0, columnspan=len(alphabet) + 1)
    scrollbar_x.pack(side="bottom", fill="x")
    scrollbar_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    
def clear_text():
    output_text.delete('1.0', tk.END)
    
def generate_sequence(length, alphabet):
    return ''.join(random.choices(alphabet, k=length))

def training_mode(pairs_words, output_text, selected_letters, alphabet):
    num_pairs = simpledialog.askinteger("Input", "How many letter pairs do you want?")
    selected_letters_list = list(selected_letters)
    if num_pairs:
        length = num_pairs * 2
        sequence = ''.join(random.choice(selected_letters_list) + random.choice(alphabet) for _ in range(num_pairs))
        split_sequence = [sequence[i:i+2] for i in range(0, length, 2)]
        output = "Generated Letter Pairs: " + ' '.join(split_sequence) + "\n"
        output += "Corresponding Words: " + ' '.join([pairs_words.get(pair, "Unknown") for pair in split_sequence])
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, output)

def quiz_mode(pairs_words, output_text, high_score_file, selected_letters, alphabet):
    high_score = read_high_score(high_scores_path)
    selected_letters_list = list(selected_letters)
    num_pairs = simpledialog.askinteger("Quiz", "How many letter pairs do you want?")
    if num_pairs is not None:
        length = num_pairs * 2
        sequence = ''.join(random.choice(selected_letters_list) + random.choice(alphabet) for _ in range(num_pairs))
        split_sequence = [sequence[i:i+2] for i in range(0, length, 2)]

        incorrect_answers = 0
        output_text.delete('1.0', tk.END)

        for pair in split_sequence:
            user_answer = simpledialog.askstring("Quiz", f"What is the word for {pair}?")
            correct_word = pairs_words.get(pair, "Unknown")

            if correct_word.lower() == user_answer.lower():
                output_text.insert(tk.END, f"Correct! {pair} is '{correct_word}'.\n")
                output_text.update_idletasks()  
                output_text.see(tk.END)
            else:
                incorrect_answers += 1
                output_text.insert(tk.END, f"Incorrect. {pair} is '{correct_word}', not '{user_answer}'.\n")
                output_text.update_idletasks()  
                output_text.see(tk.END)

        score = max(0, num_pairs - incorrect_answers)
        output_text.insert(tk.END, f"Your score: {score}\n")
        
        if score > high_score:
            messagebox.showinfo("New High Score!", "Congratulations! You've set a new high score!")
            update_high_score(high_score_file, score)

def endless_quiz_mode(pairs_words, output_text, selected_letters, alphabet):
    selected_letters_list = list(selected_letters)  

    def run_quiz():
        pair = random.choice(selected_letters_list) + random.choice(alphabet)

        user_answer = simpledialog.askstring("Endless Quiz", f"What is the word for {pair}?")
        if user_answer is None:
            output_text.insert(tk.END, "Endless Quiz Mode stopped.\n")
            return 

        correct_word = pairs_words.get(pair, "Unknown")
        if correct_word.lower() == user_answer.lower():
            output_text.insert(tk.END, f"Correct! {pair} is '{correct_word}'.\n")
            output_text.update_idletasks()  
            output_text.see(tk.END)
        else:
            output_text.insert(tk.END, f"Incorrect. {pair} is '{correct_word}'.\n")
            output_text.update_idletasks()  
            output_text.see(tk.END)

        run_quiz() 

    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, "Starting Endless Quiz Mode...\n")
    run_quiz()
    
def lookup_mode(pairs_words, output_text):
    pair = simpledialog.askstring("Lookup", "Enter a letter pair to look up its word:")
    if pair:
        word = pairs_words.get(pair.upper(), "No word defined for this pair")
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, f"The word for {pair.upper()} is: {word}")

def read_high_score(high_scores_path):
    try:
        with open(high_scores_path, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def update_high_score(file_path, high_score):
    with open(file_path, 'w') as file:
        file.write(str(high_score))


def edit_pairs_words(pairs_words, output_text, letter_pairs_path):
    def update_pairs():
        lines = edit_text.get("1.0", tk.END).strip().split("\n")
        pairs_words.clear()
        for line in lines:
            if ':' in line:
                pair, word = line.split(':', 1)
                pairs_words[pair.strip()] = word.strip()
        save_edits()

    def save_edits():
        try:
            with open(file_path, 'w') as file:
                for pair, word in pairs_words.items():
                    file.write(f"{pair}:{word}\n")
            output_text.insert(tk.END, "Changes saved successfully.\n")
        except Exception as e:
            output_text.insert(tk.END, f"Error saving changes: {e}\n")

    edit_window = tk.Toplevel()
    edit_window.title("Edit Letter Pairs")

    edit_text = scrolledtext.ScrolledText(edit_window, height=15, width=50)
    edit_text.pack()

    for pair, word in pairs_words.items():
        edit_text.insert(tk.END, f"{pair}:{word}\n")

    save_button = tk.Button(edit_window, text="Save Changes", command=update_pairs)
    save_button.pack()

        
def about_message():
    about_text = (
        "This program is made by Max Kwok U Sam for BLD Letter Pair Training. "
        "You can change the words corresponding to letters in this program by "
        "going to the letter_pairs_words text file. Note that 'Q' has been replaced with 'Y'.\n\n"
        "Training mode: Generates the number of letter pairs you input and shows the corresponding words in the dictionary.\n\n"
        "Quiz mode: Generates the number of letter pairs you input, quizzes you, and keeps track of the number of words you got right/wrong. "
        "The point system is same as MBLD.\n\n"
        "Lookup mode: Lets you look up words for the letter pairs you want.\n\n"
        "Endless Quiz Mode: Endless quiz mode without user input. No high scores are tracked."
    )
    messagebox.showinfo("About", about_text)

    
def main_app():
    window = tk.Tk()
    window.title("Memory Training Program")

    pairs_words = import_pairs_words('letter_pairs_words.txt')
    alphabet = 'ABCDEFGHIJKLMNOPYRRSTUVWX'
    selected_letters = set(alphabet)  

    output_text = scrolledtext.ScrolledText(window, height=15, width=50, wrap=tk.WORD)
    output_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    window.grid_rowconfigure(0, weight=1)
    for i in range(4):
        window.grid_columnconfigure(i, weight=1)

    training_button = tk.Button(window, text="Training Mode", command=lambda: training_mode(pairs_words, output_text, selected_letters, alphabet))
    training_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    quiz_button = tk.Button(window, text="Quiz Mode", command=lambda: quiz_mode(pairs_words, output_text, 'high_score.txt', selected_letters, alphabet))
    quiz_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    lookup_button = tk.Button(window, text="Lookup Mode", command=lambda: lookup_mode(pairs_words, output_text))
    lookup_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
 
    endless_quiz_button = tk.Button(window, text="Endless Quiz Mode", command=lambda: endless_quiz_mode(pairs_words, output_text, selected_letters, alphabet))
    endless_quiz_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

    edit_button = tk.Button(window, text="Letter Pair Toggle", command=lambda: letter_pair_toggle(alphabet, selected_letters))
    edit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    about_button = tk.Button(window, text="Edit Letter Pairs", command=lambda: edit_pairs_words(pairs_words, output_text, 'letter_pairs_words.txt'))
    about_button.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

    letter_pair_toggle_button = tk.Button(window, text="About", command=about_message)
    letter_pair_toggle_button.grid(row=3, column=0, columnspan=4, sticky="ew")

    window.mainloop()

if __name__ == "__main__":
    main_app()
