import tkinter as tk
from tkinter import scrolledtext, messagebox
import flashcard_backend  # Your backend file
import random

def main_gui():
    root = tk.Tk()
    root.title("Flashcard Study App")
    root.geometry("750x650")  # Wider to fit the listbox

    # --- NOTEBOOK TABS (Add vs Quiz) ---
    tab_frame = tk.Frame(root)
    tab_frame.pack(fill=tk.X, pady=5)

    def show_add_frame():
        add_frame.pack(fill=tk.BOTH, expand=True)
        quiz_frame.pack_forget()
        btn_add_tab.config(bg="lightblue")
        btn_quiz_tab.config(bg="SystemButtonFace")
        refresh_card_list()  # Refresh when switching to this tab

    def show_quiz_frame():
        quiz_frame.pack(fill=tk.BOTH, expand=True)
        add_frame.pack_forget()
        btn_quiz_tab.config(bg="lightblue")
        btn_add_tab.config(bg="SystemButtonFace")

    btn_add_tab = tk.Button(tab_frame, text="➕ Add / Edit Cards", command=show_add_frame, width=15)
    btn_add_tab.pack(side=tk.LEFT, padx=5)

    btn_quiz_tab = tk.Button(tab_frame, text="🎯 Study", command=show_quiz_frame, width=15)
    btn_quiz_tab.pack(side=tk.LEFT, padx=5)

    # =========================================================
    # FRAME 1: ADD / EDIT CARDS (FULL REPLACEMENT)
    # =========================================================
    add_frame = tk.Frame(root)

    # --- Left Side: Listbox to select existing cards ---
    list_frame = tk.Frame(add_frame)
    list_frame.grid(row=0, column=0, rowspan=6, padx=10, pady=5, sticky="n")

    tk.Label(list_frame, text="Your Cards:", font=("Arial", 10, "bold")).pack()

    listbox = tk.Listbox(list_frame, width=35, height=12)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # --- Right Side: Input fields ---
    input_frame = tk.Frame(add_frame)
    input_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=5, sticky="n")

    tk.Label(input_frame, text="Category:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_category = tk.Entry(input_frame, width=35)
    entry_category.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Question:").grid(row=1, column=0, sticky="ne", padx=5, pady=5)
    text_question = tk.Text(input_frame, height=4, width=35)
    text_question.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Answer:").grid(row=2, column=0, sticky="ne", padx=5, pady=5)
    text_answer = tk.Text(input_frame, height=4, width=35)
    text_answer.grid(row=2, column=1, padx=5, pady=5)

    # --- Output Area ---
    add_output = scrolledtext.ScrolledText(add_frame, height=6, width=70)
    add_output.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    # --- Buttons ---
    btn_frame = tk.Frame(add_frame)
    btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

    # Global state to track which card we are editing
    current_edit_id = None

    def show_add_msg(msg):
        add_output.delete(1.0, tk.END)
        add_output.insert(tk.END, msg)

    def refresh_card_list():
        """Load all card titles into the listbox and reset the form."""
        nonlocal current_edit_id
        listbox.delete(0, tk.END)
        cards = flashcard_backend.get_all_cards()
        for card in cards:
            # Show ID and question in the list
            listbox.insert(tk.END, f"{card['id']}: {card['question']}")
        current_edit_id = None
        entry_category.delete(0, tk.END)
        text_question.delete("1.0", tk.END)
        text_answer.delete("1.0", tk.END)
        btn_add.config(text="Add Card", command=cmd_add_card)
        show_add_msg("Select a card to edit, or fill in fields to add a new one.")

    def on_select_card(event):
        """When a card is clicked in the listbox, load its data into the form."""
        nonlocal current_edit_id
        selection = listbox.curselection()
        if not selection:
            return
        
        # Get the text from the listbox (e.g., "1: What is a list?")
        text = listbox.get(selection[0])
        card_id = int(text.split(":")[0])  # Extract the ID
        
        # Fetch the full card data from the database
        all_cards = flashcard_backend.get_all_cards()
        for card in all_cards:
            if card["id"] == card_id:
                current_edit_id = card_id
                entry_category.delete(0, tk.END)
                entry_category.insert(0, card["category"])
                text_question.delete("1.0", tk.END)
                text_question.insert("1.0", card["question"])
                text_answer.delete("1.0", tk.END)
                text_answer.insert("1.0", card["answer"])
                
                # Change the button to "Update"
                btn_add.config(text="Update Card", command=cmd_update_card)
                show_add_msg(f"Editing Card ID {card_id}")
                break

    def cmd_add_card():
        cat = entry_category.get().strip()
        q = text_question.get("1.0", tk.END).strip()
        a = text_answer.get("1.0", tk.END).strip()
        if not cat or not q or not a:
            show_add_msg("ERROR: Please fill in all fields.")
            return
        result = flashcard_backend.add_card(cat, q, a)
        show_add_msg(result)
        refresh_card_list()

    def cmd_update_card():
        nonlocal current_edit_id
        if current_edit_id is None:
            show_add_msg("ERROR: No card selected for update.")
            return
        
        cat = entry_category.get().strip()
        q = text_question.get("1.0", tk.END).strip()
        a = text_answer.get("1.0", tk.END).strip()
        if not cat or not q or not a:
            show_add_msg("ERROR: Please fill in all fields.")
            return
        
        result = flashcard_backend.update_card(current_edit_id, cat, q, a)
        show_add_msg(result)
        refresh_card_list()

    # Pack the buttons
    btn_add = tk.Button(btn_frame, text="Add Card", command=cmd_add_card, width=15)
    btn_add.pack(side=tk.LEFT, padx=5)

    btn_clear = tk.Button(btn_frame, text="Clear Fields", command=refresh_card_list, width=15)
    btn_clear.pack(side=tk.LEFT, padx=5)

    # Populate the listbox on startup and bind click event
    refresh_card_list()
    listbox.bind('<<ListboxSelect>>', on_select_card)

    # =========================================================
    # FRAME 2: QUIZ (UNCHANGED)
    # =========================================================
    quiz_frame = tk.Frame(root)
    
    quiz_info = tk.Label(quiz_frame, text="Click 'Load New Deck' to start", font=("Arial", 12))
    quiz_info.pack(pady=5)

    q_label = tk.Label(quiz_frame, text="Question", font=("Arial", 14), wraplength=500)
    q_label.pack(pady=20)

    entry_answer = tk.Entry(quiz_frame, width=50)
    entry_answer.pack(pady=10)

    quiz_output = scrolledtext.ScrolledText(quiz_frame, height=6, width=60)
    quiz_output.pack(pady=10)

    def show_quiz_msg(msg):
        quiz_output.delete(1.0, tk.END)
        quiz_output.insert(tk.END, msg)

    current_deck = []
    current_index = 0
    score_correct = 0
    score_wrong = 0

    def cmd_load_deck():
        nonlocal current_deck, current_index, score_correct, score_wrong
        all_cards = flashcard_backend.get_all_cards()
        if not all_cards:
            show_quiz_msg("No cards found! Add some cards first.")
            return
        random.shuffle(all_cards)
        current_deck = all_cards
        current_index = 0
        score_correct = 0
        score_wrong = 0
        show_next_card()

    def show_next_card():
        nonlocal current_index
        if current_index < len(current_deck):
            card = current_deck[current_index]
            q_label.config(text=card["question"])
            entry_answer.delete(0, tk.END)
            show_quiz_msg(f"Card {current_index + 1} of {len(current_deck)}\nCategory: {card['category']}")
            entry_answer.focus()
        else:
            q_label.config(text="QUIZ FINISHED!")
            entry_answer.delete(0, tk.END)
            show_quiz_msg(f"✅ Correct: {score_correct}\n❌ Wrong: {score_wrong}")

    def cmd_check_answer():
        nonlocal current_index, score_correct, score_wrong
        if current_index >= len(current_deck):
            show_quiz_msg("Quiz is over! Click 'Load New Deck' to restart.")
            return
        user_ans = entry_answer.get().strip()
        correct_ans = current_deck[current_index]["answer"]
        
        if user_ans.lower() == correct_ans.lower():
            score_correct += 1
            msg = "✅ Correct!"
        else:
            score_wrong += 1
            msg = f"❌ Wrong. The answer was: {correct_ans}"
        
        current_index += 1
        show_quiz_msg(f"{msg}\n\nScore: Correct: {score_correct} | Wrong: {score_wrong}")
        
        if current_index < len(current_deck):
            root.after(1500, show_next_card)
        else:
            root.after(1500, show_next_card)

    btn_load = tk.Button(quiz_frame, text="Load New Deck", command=cmd_load_deck, width=15)
    btn_load.pack(side=tk.LEFT, padx=10, pady=10)

    btn_check = tk.Button(quiz_frame, text="Check Answer", command=cmd_check_answer, width=15)
    btn_check.pack(side=tk.LEFT, padx=10, pady=10)

    # Start on the Add Frame
    show_add_frame()
    root.mainloop()

if __name__ == "__main__":
    main_gui()