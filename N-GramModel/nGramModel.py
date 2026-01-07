import requests
import random
import re
from collections import defaultdict, Counter

class Sherlock5Gram:
    def __init__(self):
        self.model = defaultdict(Counter)
        self.n = 5

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.split()

    def train_from_link(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            tokens = self.clean_text(response.text)
            for i in range(len(tokens) - self.n + 1):
                context = tuple(tokens[i : i + self.n - 1])
                target = tokens[i + self.n - 1]
                self.model[context][target] += 1
            print("--- Training Complete ---")
        except Exception as e:
            print(f"Error: {e}")

    def generate(self, seed_text, length=15):
        tokens = self.clean_text(seed_text)
        if len(tokens) < self.n - 1:
            return f"Error: Need {self.n-1} words."
        
        result = tokens[:]
        for _ in range(length):
            context = tuple(result[-(self.n - 1):])
            if context not in self.model:
                break
            
            choices = list(self.model[context].keys())
            weights = list(self.model[context].values())
            next_word = random.choices(choices, weights=weights)[0]
            result.append(next_word)
        return " ".join(result)

model = Sherlock5Gram()
model.train_from_link("https://www.gutenberg.org/cache/epub/1661/pg1661.txt")

print("\nSample 1:")
print(model.generate("And what of Irene", length=12))

print("\nSample 2:")
print(model.generate("He has come back", length=12))

print("\nSample 3:")
print(model.generate("My dear Watson, you", length=12))