import random


class Answer:
    """Contains all the answer"""

    answer_stupid = [
        "Je n'y comprend rien !",
        "Qu'est ce que tu me racontes là !",
        "N'as tu pas été à l'école ?",
        "Arrête de parler dans ta barbe !",
        "Tiens voilà un dictionnaire, reviens me voir après l'avoir lu ...",
    ]

    answer_location_find = [
        "C'est un endroit magnifique !",
        "Ah quand j'étais jeune, je passais mon temps là-bas...",
        "J'y ai rencontré ma première femme !",
        "Tu devrais absolument visiter cette endroit !",
    ]

    def random_answer(self, list):
        """Return a random answer"""
        return random.choice(list)
