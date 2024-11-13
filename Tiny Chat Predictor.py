import random
import re
from collections import defaultdict, Counter

class TinyChatPredictor:
    def __init__(self):
        # Initializes a dictionary where each key is a tuple of words (representing a sentence context),
        # and the value is a Counter object that tracks occurrences of possible next words.
        self.context_dict = defaultdict(Counter)

    def load_phrases(self, filename):
        """Loads phrases from a specified file and trains the model on these phrases."""
        with open(filename, 'r') as file:
            text = file.read()
        self.train(text)

    def train(self, text):
        """Trains the model on a given text, splitting context by periods."""
        # Split the text into sentences based on periods
        sentences = text.split('.')
        
        for sentence in sentences:
            # Remove punctuation and split each sentence into words
            words = re.findall(r'\b\w+\b', sentence.lower())
            # Iterate through the sequence, using the full context (all previous words in the sentence)
            for i in range(1, len(words)):
                context = tuple(words[:i])  # Context includes all words up to i
                next_word = words[i]
                # Update the Counter for the current context with the next word
                self.context_dict[context][next_word] += 1

    def predict_next_word(self, context):
        """Predicts the next word based on the context with fallback to shorter contexts."""
        context_tuple = tuple(context.lower().split())
        
        # Try to match with the longest context first and gradually reduce it
        for i in range(len(context_tuple), 0, -1):
            sub_context = context_tuple[-i:]
            if sub_context in self.context_dict:
                possible_words = self.context_dict[sub_context]
                total_count = sum(possible_words.values())
                probabilities = {word: count / total_count for word, count in possible_words.items()}
                return random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
        
        return None  # Fallback to None if no context is found

    def predict_with_letter(self, context, letter):
        """Predicts the next word that starts with a specified letter given the context, with fallbacks."""
        context_tuple = tuple(context.lower().split())
        
        # Try progressively shorter contexts
        for i in range(len(context_tuple), 0, -1):
            sub_context = context_tuple[-i:]
            if sub_context in self.context_dict:
                possible_words = self.context_dict[sub_context]
                # Filter words that start with the specified letter
                filtered_words = {word: count for word, count in possible_words.items() if word.startswith(letter)}
                
                if filtered_words:
                    total_count = sum(filtered_words.values())
                    probabilities = {word: count / total_count for word, count in filtered_words.items()}
                    return random.choices(list(probabilities.keys()), list(probabilities.values()))[0]
        
        return "No suggestion available"  # Fallback message

    def generate_one_word(self, start_words):
        """Generates a single word based on full context."""
        next_word = self.predict_next_word(' '.join(start_words))
        return next_word if next_word else "No suggestion available"

# Usage
predictor = TinyChatPredictor()

# Load phrases from a file
filename = 'written_habits.txt'  # This is the 'I have a dream' speech from MLK. You can change it as will
predictor.load_phrases(filename)

# Prompting the user to input their starting phrase
start_words_input = input('Enter your starting phrase: ').lower().replace(',', '').split()
print("Generated one word:", predictor.generate_one_word(start_words_input))

# Predicting a word starting with a specific letter
letter = input('What\'s the first letter of the next word? ').lower()
print(f"Next word prediction starting with '{letter}':", predictor.predict_with_letter(' '.join(start_words_input), letter))



