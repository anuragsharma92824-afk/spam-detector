import tkinter as tk
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# file check
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
else:
    df = pd.DataFrame({
        'text': ["Win money now", "Hello friend", "Free offer", "Good morning"],
        'label': [1, 0, 1, 0]
    })
    df.to_csv("data.csv", index=False)

# train
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

model = MultinomialNB()
model.fit(X, y)

# accuracy
y_pred = model.predict(X)
acc = accuracy_score(y, y_pred)

# functions
def check_spam():
    msg = entry.get()

    if msg == "":
        output.config(text="⚠️ Please enter message", fg="orange")
        return

    msg_vec = vectorizer.transform([msg])
    result = model.predict(msg_vec)

    if result[0] == 1:
        output.config(text="🚫 Spam Message", fg="red")
        label = 1
    else:
        output.config(text="✅ Not Spam", fg="green")
        label = 0

    # save data
    new_data = pd.DataFrame({'text': [msg], 'label': [label]})
    new_data.to_csv("data.csv", mode='a', header=False, index=False)

    # show history
    history.insert(tk.END, "➤ " + msg + "\n")


def clear_text():
    entry.delete(0, tk.END)
    output.config(text="")
    
def clear_history():
    # only screen clear (file safe)
    history.delete(1.0, tk.END)

    # hover effect
def on_enter(e):
    e.widget['bg'] = "#0056b3"

def on_leave(e):
    e.widget['bg'] = "#007bff"

# GUI
root = tk.Tk()
root.title("Spam Detector")
root.geometry("520x550")
root.configure(bg="#dfe9f3")
# 🔥 Card Frame (center box)
card = tk.Frame(root, bg="white", bd=3, relief="ridge")
card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)


# heading
tk.Label(card, text="📩 Spam Email Detector",
         font=("Arial", 18, "bold"),
         bg="white", fg="#333").pack(pady=15)

# accuracy
tk.Label(card, text=f"Accuracy: {round(acc*100,2)}%",
         font=("Arial", 11),
         bg="white", fg="#777").pack(pady=5)

# input
entry = tk.Entry(card, width=32, font=("Arial", 13),bd=2, relief="solid")
entry.pack(pady=15)

# buttons
btn = tk.Button(card, text="Check Message",
          command=check_spam,
          bg="#007bff",
            fg="white",
          font=("Arial", 12, "bold"),
          cursor="hand2", padx=10, pady=5)
btn.pack(pady=8)
# hover bind
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)
#clear text button
tk.Button(card, text="Clear",
          command=clear_text,
          bg="#6c757d", fg="white",
          cursor="hand2", padx=10, pady=5).pack(pady=5)

# clear history button (screen only)
tk.Button(card, text="Clear History",
          command=clear_history,
          bg="red", fg="white",
          cursor="hand2",
          padx=10, pady=5).pack(pady=5)

# output
output = tk.Label(card, text="",
                  font=("Arial", 14, "bold"),
                  bg="white")
output.pack(pady=10)

# history
tk.Label(card, text="History:", font=("Arial", 12, "bold"),
         bg="white").pack(pady=5)
# scrollable history
frame = tk.Frame(card)
frame.pack()

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

history = tk.Text(frame, height=6, width=32, yscrollcommand=scroll.set, bd=2, relief="solid")
history.pack()
scroll.config(command=history.yview)

# load history from file
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
    for msg in df['text']:
        history.insert(tk.END, "➤ " + msg + "\n")
root.mainloop()