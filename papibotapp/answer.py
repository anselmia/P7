import random


class Answer:
    """Contains all the answer"""

    answer_stupid = [
        "Tu es bon en algèbre mon petit !",
        "Tu es bien silencieux mon petit !",
        "Ne soit pas interloqué mon petit !",
        "Réveille toi mon petit !",
        "Arrête de grommeler mon petit !",
        "Mais de rien mon petit !",
    ]

    answer_location_find = [
        "C'est un endroit magnifique !",
        "J'y ai été quand j'étais jeune.",
        "J'y passe tout mes dimanches !",
    ]

    def random_answer(self, list):
        """Return a random answer"""
        return random.choice(list)
