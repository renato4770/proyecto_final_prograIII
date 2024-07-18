import random
from card import BabyUnicornCard, UnicornCard, PandaCard
from card_effects import unicorn_effect, panda_effect

class Deck:
    def __init__(self, cards):
        self.cards = cards

    def draw_card(self):
        return self.cards.pop(0) if self.cards else None

class DeckBuilder:
    def __init__(self):
        self.cards = []
        self.card_names = ["Alluring Narwhal", "Americorn", "Angel Unicorn", "Annoying Flying", "Baby Narwhal", "Baby Unicorn Black", "Baby Unicorn Blue", "Baby Unicorn Brown", "Baby Unicorn Death", "Baby Unicorn Green",
        "Baby Unicorn Orange", "Baby Unicorn Pink", "Baby Unicorn Purple", "Baby Unicorn Rainbow", "Baby Unicorn Red", "Baby Unicorn White", "Baby Unicorn Yellow", "Back Kick", "Barbed Wire", "Basic Unicorn Blue",
        "Basic Unicorn Green", "Basic Unicorn Indigo", "Basic Unicorn Orange", "Basic Unicorn Purple", "Basic Unicorn Red", "Basic Unicorn Yellow", "Black Knight Unicorn", "Blatant Thievery", "Blinding Light"
        "Broken Stable", "Chainsaw Unicorn", "Change Of Luck", "Classy Narwhal", "Double Dutch", "Extra Tail", "Extremely Destructive Unicorn", "Extremely Fertile Unicorn", "Ginormous Unicorn", "Glitter Bomb",
        "Glitter Tornado", "Good Deal", "Greedy Flying Unicorn", "Llamacorn", "Magical Flying Unicorn", "Magical Kittencorn", "Majestic Flying Unicorn", "Mermaid Unicorn", "Mystical Vortex", "Nanny Camp",
        "Narwhal", "Narwhal Torpedo", "Neigh", "Pandamonium", "Puppicorn", "Queen Bee Unicorn", "Rainbow Aura", "Rainbow Mane", "Rainbow Unicorn", "Reset Button", "Re-Target", "Rhinocorn", "Sadistic Ritual",
        "Seductive Unicorn", "Shabby The Narwhal", "Shake Up", "Shark With A Horn", "Slowdown", "Stabby The Unicorn", "Summoning Ritual", "Super Neigh", "Swift Flying Unicorn", "Targeted Destruction",
        "The Great Narwh", "Tiny Stable", "Two For One", "Unfair Bargain", "Unicorn Lasso", "Unicorn On The Cob", "Unicorn Phoenix", "Unicorn Poison", "Unicorn Shrinkra", "Unicorn Swap", "Yay", "Zombie Unicorn"]

        self.baby_unicorn_names = [
            "Baby Unicorn (Black)", "Baby Unicorn (Blue)", "Baby Unicorn (Brown)", "Baby Unicorn (Death)",
            "Baby Unicorn (Green)", "Baby Unicorn (Orange)", "Baby Unicorn (Pink)", "Baby Unicorn (Purple)",
            "Baby Unicorn (Rainbow)", "Baby Unicorn (Red)", "Baby Unicorn (White)", "Baby Unicorn (Yellow)"
        ]
    
    def add_cards(self, count):
        for i in range(count):
            name = self.card_names[i % len(self.card_names)]
            if "Panda" in name:
                self.cards.append(PandaCard(i, name, panda_effect))
            else:
                self.cards.append(UnicornCard(i, name, unicorn_effect))

    def get_baby_unicorn(self, index):
        return BabyUnicornCard(index, self.baby_unicorn_names[index % len(self.baby_unicorn_names)])            

    def shuffle(self):
        random.shuffle(self.cards)

    def build(self):
        return Deck(self.cards)
