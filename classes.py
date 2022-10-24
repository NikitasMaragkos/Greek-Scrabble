from random import randint
import itertools
from itertools import permutations

class SakClass:
    # Class constructor
    def __init__(self):
        self.letters = {'Α': 1, 'Β': 8, 'Γ': 4, 'Δ': 4, 'Ε': 1, 'Ζ': 10, 'Η': 1, 'Θ': 10, 'Ι': 1, 'Κ': 2, 'Λ': 3,
                        'Μ': 3, 'Ν': 1, 'Ξ': 10, 'Ο': 1, 'Π': 2, 'Ρ': 2, 'Σ': 1, 'Τ': 1, 'Υ': 2, 'Φ': 8, 'Χ': 8,
                        'Ψ': 10, 'Ω': 3}
        self.sack = ['Α'] * 12 + ['Β'] + ['Γ'] * 2 + ['Δ'] * 2 + ['Ε'] * 8 + ['Ζ'] + ['Η'] * 7 + ['Θ'] + ['Ι'] * 8 + [
            'Κ'] * 4 + ['Λ'] * 3 + ['Μ'] * 3 + ['Ν'] * 6 + ['Ξ'] + ['Ο'] * 9 + ['Π'] * 4 + ['Ρ'] * 5 + ['Σ'] * 7 + [
                        'Τ'] * 8 + ['Υ'] * 4 + ['Φ'] + ['Χ'] + ['Ψ'] + ['Ω'] * 3

    # Getter for the sack, i.e. the set of letters
    def get_Sack(self):
        return self.sack

    # Getter of the dictionary that contains the letters with their points
    def get_Letter(self):
        return self.letters

    # Random generator for choosing letters when initializing the game or when a word has been played
    def choose_Letters(self):
        self.pickedLetters = []
        for i in range(0, 7):
            random_pick = self.sack[randint(0, len(self.sack) - 1)]
            self.pickedLetters.append(random_pick)
            self.sack.remove(random_pick)
        return self.pickedLetters

    # Reloading a player's "hand" with letters from the remaining in the sack.
    def reload_letters(self, pickedLetters):
        for i in range(0, 7 - len(pickedLetters)):
            random_pick = self.sack[randint(0, len(self.sack) - 1)]
            pickedLetters.extend(random_pick)
            self.sack.remove(random_pick)
        return pickedLetters

    # Replace a player's "hand" with letters from the remaining in the sack.
    def replace_letters(self, pickedLetters):
        for letter in pickedLetters:
            self.sack.append(letter)
        return self.reload_letters([])


# This is the parent class, defining a  player. Each player has two "attributes". Their letters and their score
class Player:
    pickedLetters = []
    points = int()

    def __init__(self, pickedLetters, points):
        self.pickedLetters = pickedLetters
        self.points = points

    def pickLetters(self, sack):
        self.pickedLetters = sack.choose_Letters()

    def reloadLetters(self, sack):
        self.pickedLetters = sack.reload_letters(self.pickedLetters)

    def replaceLetters(self, sack):
        self.pickedLetters = sack.replace_letters(self.pickedLetters)

    # Thus function gives points based on the given word and removes the letters from the list
    def playCorrectWord(self, word, sack):
        score = 0
        for x in word:
            score += sack.get_Letter()[x]
            self.pickedLetters.remove(x)
        self.reloadLetters(sack)
        self.points += score
        print('Word score: %d' % score)

# This is a class for the CPU, inheriting attributes from Player class
class CPU(Player):
    currentPlay = 1
    percentage = 70

    def chooseWord(self, sack):
        print('Letters in sack: %d letters - CPU plays:' % len(sack.get_Sack()))
        print('CPU letters:')
        print(self.pickedLetters)
        if self.currentPlay == '1':
            print("Min Algorithm executing....")
            word_length = 2
            while word_length <= 7:
                print('Searching for word with %d letters' % word_length)
                per = list(map("".join, itertools.permutations(self.pickedLetters, word_length)))

                greek7 = open('greek7.txt', 'r', encoding="utf8")
                content = ''
                for line in greek7:
                    if len(line) == word_length + 1:
                        content = content + line
                greek7.close()

                for word in per:
                    if word in content:
                        print('CPUs word: %s' % word)
                        self.playCorrectWord(word, sack)
                        print('CPU points: %d' % self.points)
                        return 0
                print('No word with %d letters' % word_length)
                word_length += 1
            print("No word found. CPU passes.")
            self.replaceLetters(sack)
        elif self.currentPlay == '2':
            print("Max Algorithm executing....")
            word_length = 7
            while word_length >= 2:
                print('Searching for word with %d letters' % word_length)
                per = list(map("".join, itertools.permutations(self.pickedLetters, word_length)))

                greek7 = open('greek7.txt', 'r', encoding="utf8")
                content = ''
                for line in greek7:
                    if len(line) == word_length + 1:
                        content = content + line
                greek7.close()

                for word in per:
                    if word in content:
                        found = True
                        print("CPU word: " + word)
                        self.playCorrectWord(word, sack)
                        print('CPU points: %d' % self.points)
                        return 0
                print('No word with %d letters' % word_length)
                word_length -= 1
            print("No word found. CPU passes.")
            self.replaceLetters(sack)
        elif self.currentPlay == '3':
            print("Smart Algorithm executing....")
            word_length = 2
            max_score = 0
            best_word = ''
            found = False
            while word_length <= 7:
                per = list(map("".join, itertools.permutations(self.pickedLetters, word_length)))
                print(per)

                greek7 = open('greek7.txt', 'r', encoding="utf8")
                content = ''
                for line in greek7:
                    if len(line) == word_length + 1:
                        content = content + line
                greek7.close()

                for word in per:
                    if word in content:
                        found = True
                        score = 0
                        for x in word:
                            score += sack.get_Letter()[x]
                        if score >= max_score:
                            max_score = score
                            best_word = word
                word_length += 1
            if not found:
                print("No word found. CPU passes.")
                self.replaceLetters(sack)
            else:
                print('CPUs word: %s' % best_word)
                self.playCorrectWord(best_word, sack)
                print('CPU points: %d' % self.points)
                return 0
        elif self.currentPlay == '4':
            print("Smart - Fail Algorithm executing....")
            word_length = 2
            max_score = 0
            best_word = ''
            found = False
            while word_length <= 7:
                per = list(map("".join, itertools.permutations(self.pickedLetters, word_length)))
                print(per)

                greek7 = open('greek7.txt', 'r', encoding="utf8")
                content = ''
                for line in greek7:
                    if len(line) == word_length + 1:
                        content = content + line
                greek7.close()

                for word in per:
                    if word in content:
                        if randint(1, 100) > self.percentage:
                            continue
                        found = True
                        score = 0
                        for x in word:
                            score += sack.get_Letter()[x]
                        if score >= max_score:
                            max_score = score
                            best_word = word
                word_length += 1
            if not found:
                print("No word found. CPU passes.")
                self.replaceLetters(sack)
            else:
                print("CPU word: " + best_word)
                self.playCorrectWord(best_word, sack)
                print('CPU points: %d' % self.points)
                return 0


# This is a class for the human player, inheriting attributes from Player class
class Human(Player):
    def chooseWord(self, sack):
        print('Letters remaining: %d letters - Human plays: ' % len(sack.get_Sack()))
        print('Available letters to create a word:')
        print(self.pickedLetters)
        word = ''
        while True:
            word = input('Play a word: (If you want to pass, press "p". To exit game, press "q"): ')
            if word == 'p':  # if player chooses p then letters will be changed!
                print("Human passes the turn and reload the picked letters.")
                self.replaceLetters(sack)
                return 0
            elif word == 'q':  # Quit game if q is pressed
                return 1
            elif len(word) > 7:
                print('You can play words with maximum length 7, not %d.' % (len(word)))
                continue
            else:
                if checkCorrectness(word, self.pickedLetters):
                    if validateWord(word):
                        self.playCorrectWord(word, sack)
                        print('Player points: %d' % self.points)
                        return 0
                    print('Given word does not exist in our current dictionary. Try again.')
                    continue
                print('Given word cannot be played based on the letters you currently have. Try again.')


# In this class we implemented every function that is needed for the execution. More could have been implemented to
# make the code more elegant.
class Game:
    def __init__(self):
        pass

    # Initializing menu, showing the player its choices
    def initialize_menu(self):
        print('~~~~~~~~~ PySCRABBLE ~~~~~~~~~')
        print('                    ')
        print('1) New game')
        print('2) Score')
        print('3) Implementation Information')
        print('q)- Quit game')
        print('                   ')

    # Loading dictionary with words from local drive
    def load_dictionary_7(self):
        dictionary_7 = 'greek7.txt'
        return dictionary_7

    # This function implements how the player will choose what to do from the menu
    def select_mode(self):
        mode = input('Select how to proceed: ')
        while (mode != '1' and mode != '2' and mode != '3' and mode != 'q'):
            mode = input()
        return mode

    # This function opens the file with the saved previous scores, the log file.
    def open_score_file(self):
        try:
            f = open('log.txt')
            print('History of matches:')
            for line in f:
                print(line)
            f.close()
        except IOError:
            print("There is not any record yet")

    # This function will provide the player with the ability to select how the CPU will play.
    def options(self):
        print("CPU can use the following algorithms: ")
        print("1) Min")
        print("2) Max")
        print("3) Smart")
        print("4) Smart-Fail")
        print("Select an algorithm: ")
        selection = input()
        while (selection != '1' and selection != '2' and selection != '3' and selection != '4'):
            selection = input("Not correct. Pick again.")
        return selection

    # This function is important to create the FAIL part in the Smart - Fail Algorithm.
    def fail_probability(self):
        percentage = input(
            "Set an integer number from 1 to 100. The higher the number the fewer missplays will the CPU perform.")
        while (isinstance(percentage, int) != True and percentage < '1' and percentage > '100'):
            percentage = input()
        return int(percentage)

    # This function will print scores when game ends
    def final_scores(self, cpu_points, human_points):
        print('Final scores: ')
        print('Human score: %d' % human_points)
        print('CPU score: %d' % cpu_points)
        if cpu_points < human_points:
            print("Human Wins!")
        else:
            print("CPU wins")

    # This functions saves scores into the txt file
    def save_scores(self, cpu_points, human_points):
        log = open('log.txt', 'a')
        log.write('Match: Human: ' + str(human_points) + '  ' + 'CPU: ' + str(cpu_points))
        log.write('\n')
        log.close()


# This function checks if the given word is correct based Player's letters
def checkCorrectness(word, pickedLetters):
    copyLetters = pickedLetters.copy()
    for x in word:
        if x in copyLetters:
            copyLetters.remove(x)
        else:
            return False
    return True


# This function checks if the given word exists in our library
def validateWord(word):
    dictionary_7 = 'greek7.txt'
    with open(dictionary_7, encoding="utf8") as f:
        found = False
        for line in f:
            if ('%s' % (line)) == word + '\n':
                return True
    return False
