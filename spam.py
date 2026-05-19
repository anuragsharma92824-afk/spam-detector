import tkinter as tk
import pandas as pd
import os
import pyttsx3
import matplotlib.pyplot as plt
import re
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# file check
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
else:
    df = pd.DataFrame({
        'text': ["Win money now", "Hello friend", "Free offer", "Good morning", "Free lottery", "Lottery winner", "Claim your prize", "Click here to win", "Urgent response needed", 
                 "How are you", "Let's meet tomorrow", "Thank you", "Anurag", "hello"],
        'label': [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,]
    })
    df.to_csv("data.csv", index=False)

# train
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

model = MultinomialNB()
model.fit(X, y)
spam_count = 0
ham_count = 0


# accuracy
y_pred = model.predict(X)
acc = accuracy_score(y, y_pred)

dark = False

# functions
def check_spam():
    global spam_count, ham_count
    email = email_entry.get()
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(pattern,email):
        output.config(text="Invalid Email", fg="red")
        return
    msg = entry.get()

    full_text = email +""+ msg

    if msg == "":
        output.config(text="⚠️ Please enter message", fg="orange")
        return

    msg_vec = vectorizer.transform([full_text])
    result = model.predict(msg_vec)

    if result[0] == 1:
        output.config(text="🚫 Spam Message", fg="red")
        engine = pyttsx3.init()
        engine.say("Spam Message Detected")
        engine.runAndWait()
        spam_count += 1
        label = 1
    else:
        output.config(text="✅ Not Spam", fg="green")
        engine = pyttsx3.init()
        engine.say("Not Spam Message")
        engine.runAndWait()
        ham_count += 1
        label = 0

    # save data
    new_data = pd.DataFrame({'text': [msg], 'label': [label]})
    new_data.to_csv("data.csv", mode='a', header=False, index=False)

    # show history
    current_time = datetime.now().strftime("%H:%M:%S")
    history.insert(
    tk.END,
    f"[{current_time}] ➤ {msg} \n")


def clear_text():
    entry.delete(0, tk.END)
    output.config(text="")
    
def clear_history():
    # only screen clear (file safe)
    history.delete(1.0, tk.END)

def show_graph():
    labels =["Spam", "Not Spam"]
    values =[spam_count, ham_count]
    plt.figure(figsize=(5,4))
    plt.bar(labels, values, color=["red","green"])
    plt.title("Spam Detection Report", fontsize=16)

    plt.xlabel("Message Type")
    plt.ylabel("Count")
    plt.show()

def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_Label.config(text=current_time)
    root.after(1000, update_time)

#dark mode

def dark_mode():

     global dark
     if dark == False:
       root.configure(bg="#1e1e1e")
       card.configure(bg="#2d2d2d")
       output.configure(bg="#2d2d2d",fg="white")
       dark = True
     else:
       root.configure(bg="#dfe9f3")
       card.configure(bg="white")
       output.configure(bg="white",fg="black")
       dark = False

    # hover effect
def on_enter(e):
    e.widget['bg'] = "#0056b3"

def on_leave(e):
    e.widget['bg'] = "#007bff"

# GUI
root = tk.Tk()
root.title("Spam Detector")
root.geometry("650x850")
root.configure(bg="#dfe9f3")
# 🔥 Card Frame (center box)
card = tk.Frame(root, bg="white", bd=4, relief="ridge")
card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=750)


# heading
tk.Label(card, text="📩 Spam Email Detector",
         font=("Arial", 18, "bold"),
         bg="white", fg="#333").pack(pady=15)

time_Label = tk.Label(card, font=("Arial", 12, "bold"),bg="black", fg="lime", width=12, relief="ridge",bd=3) 
time_Label.pack(pady=5)

# accuracy
tk.Label(card, text=f"Accuracy: {round(acc*100,2)}%",
         font=("Arial", 11),
         bg="white", fg="#555").pack(pady=5)
# email label
tk.Label(card, text="Sender Email",font=("Arial",11,"bold"),bg="white").pack()

#emial input

email_entry = tk.Entry(card, width=32, font=("Arial", 13),bd=2, relief="solid")
email_entry.pack(pady=5)



# input label
tk.Label(card, text="Message",font=("Arial",11,"bold"),bg="white").pack()


# input
entry = tk.Entry(card, width=32, font=("Arial", 13),bd=2, relief="solid")
entry.pack(pady=15)

# buttons
btn = tk.Button(card, text="Check Message",width=15,
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
tk.Button(card, text="Clear", width=15,
          command=clear_text,
          bg="#ff9800", fg="white", font=("Arial",9, "bold"),
          cursor="hand2", padx=10, pady=5).pack(pady=6)

# clear history button (screen only)
tk.Button(card, text="Clear History",width=15,
          command=clear_history,
          bg="red", fg="white",
          cursor="hand2",
          padx=10, pady=5).pack(pady=6)

#Dark mode button
tk.Button(card, text="Dark Mode", width=15,
          command=dark_mode, bg="black", fg="white", 
          cursor="hand2",
          padx=10, pady=5).pack(pady=6)
#Graph button
tk.Button(card, text="Show Graph",width=15,
          command=show_graph, bg="green", fg="white", 
          cursor="hand2",
          padx=10, pady=5).pack(pady=6)


# output
output = tk.Label(card, text="",
                  font=("Arial", 16, "bold"),
                  bg="white",padx=10, pady=5)
output.pack(pady=10)

# history
tk.Label(card, text="History:", font=("Arial", 12, "bold"),
         bg="white").pack(pady=5)
# scrollable history
frame = tk.Frame(card)
frame.pack()
# scroll button
scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

history = tk.Text(frame, height=6, width=35, font=("Consolas",10,"bold"), bg="#f5f5f5",fg="black", yscrollcommand=scroll.set, bd=2, relief="solid")
history.pack(pady=5)

# load history from file
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
    for msg in df['text']:
        history.insert(tk.END, "➤ " + msg + "\n")
        update_time()
root.mainloop()