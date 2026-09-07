import sqlite3
import random  

def init_database():
    
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            question TEXT,
            answer TEXT
        )
    ''')
    conn.commit()
    conn.close()

#  CORE FUNCTIONS  

def add_card(category, question, answer):
    """
    Add a new flashcard to the database.
    Return a success or error message.
    """
    if not category or category == "N/A":
        return "Error: Category cannot be empty or 'N/A'."
    try:
        init_database()  
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO flashcards (category, question, answer) VALUES (?, ?, ?)", (category, question, answer))
        conn.commit()

        if cursor.rowcount > 0:
            result = "Card added successfully!"
        else:
            result = "Error: Failed to add card."

        return result
    except sqlite3.Error as e:
        return f"Database error: {e}"


def get_all_cards():
   

    init_database()
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, question, answer FROM flashcards")
    rows = cursor.fetchall()
    card_list = []
    for row in rows:
        card_dict = {
            "id": row[0],
            "category": row[1],
            "question": row[2],
            "answer": row[3]
        }
        card_list.append(card_dict)
    conn.close()
    return card_list


def update_card(card_id, category, question, answer):
    if not category or not question or not answer:
        return "Error: All fields must be filled."

    try:
        init_database()  
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE flashcards SET category = ?, question = ?, answer = ? WHERE id = ?", (category, question, answer, card_id))
        conn.commit()

        if cursor.rowcount > 0:
            result = "Card updated successfully!"
        else:
            result = "Error: No card found with the given ID."

        return result

    except sqlite3.Error as e:
        return f"Database error: {e}"


