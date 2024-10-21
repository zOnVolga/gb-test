import tkinter as tk
import random

# Определяем карты и их старшинство
suits = ['♠', '♥', '♦', '♣']
ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Создаем колоду
deck = [rank + suit for suit in suits for rank in ranks]

class DurakGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Игра в Дурака")
        
        self.player_hand = []
        self.ai_hand = []
        
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()
        
        self.deal_button = tk.Button(master, text="Раздать карты", command=self.deal_cards)
        self.deal_button.pack()
        
        self.player_label = tk.Label(master, text="Ваши карты:")
        self.player_label.pack()
        
        self.ai_label = tk.Label(master, text="Карты ИИ:")
        self.ai_label.pack()
        
        self.message_label = tk.Label(master, text="")
        self.message_label.pack()

    def deal_cards(self):
        random.shuffle(deck)
        self.player_hand = deck[:6]
        self.ai_hand = deck[6:12]
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")
        self.player_label.config(text="Ваши карты: " + ' '.join(self.player_hand))
        self.ai_label.config(text="Карты ИИ: " + ' '.join(self.ai_hand))
        self.message_label.config(text="Выберите карту для хода.")

    def player_turn(self, card):
        if card in self.player_hand:
            self.player_hand.remove(card)
            self.update_display()
            self.ai_turn()

    def ai_turn(self):
        if self.ai_hand:
            card = self.ai_hand[0]  # ИИ просто играет первую карту
            self.ai_hand.remove(card)
            self.update_display()
            self.message_label.config(text=f"ИИ сыграл: {card}")

if __name__ == "__main__":
    root = tk.Tk()
    game = DurakGame(root)
    root.mainloop()
