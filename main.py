"""
Μαραγκός Νικήτας (3562)
"""

import classes


def guidelines():
    """
    1. IMPLEMENTED CLASSES
    =========================
    1)SakClass
    2)Player
    3)CPU
    4)Human
    5)Game

    2. INHERITANCE
    =========================
    1)CPU(Player)
    2)Human(Player)

    3. SCALABILITY
    =========================
    Basically, the class Player has the main methods that a player should do during the game of Scrabble.
    For instance, pickLetters(), reloadLetters() and playCorrectWord(). The main difference that we should
    take into account, is the logic that a Human or a Computer would choose a word to play. For the human,
    we just create chooseWord() and asking him/her/it e.t.c. to play. On the other hand, for the Computer
    we hae implement several algorithms that chooseWord() will use in order to choose a word to play. The
    class CPU has two extra fields indicating which one of the algorithm will be played. So, class CPU can
    be extended with new algorithms easily.

    5. DATA STRUCTURES USED
    =========================
    We use lists as our main data structure. Python has a great variety that helps us create readable functions
    with great documentation. So, Human and CPU have a list of seven letters. After choosing which word to play
    we must check if this word exists in our dictionary of word (greek7.txt). We simply create a big string in
    which we save all these words and by simply writing "word in dictionary" we know if this word exists. We
    utilize the simple but efficient way of python.

    6. ALGORITHMS IMPLEMENTED
    =========================
    a) Min-Max-Smart
       Min: The computer produces all the possible permutations starting with 2 letters. If there is a word that
       exists in greek7.txt it chooses it. If there is not any word of this permutation, it will produce all the
       permutations with 3 words and repeat the same process. It is called Min because the chosen word will have
       the minimum length.

       Max: The computer produces all the possible permutations starting with 7 letters. If there is a word that
       exists in greek7.txt it chooses it. If there is not any word in this permutation, it will produce all the
       permutations with 6 words and repeat the same process. It is called Max because the chosen word will have
       the maximum length.

       Smart: The computer produces all the possible permutations of 2, 3, 4, 5, 6, and 7  letters. It chooses to
       play the word that exists in greek7.txt and has the biggest score. It is called smart because it helps the
       computer to gather the maximum score in each round.

    b) Smart-Fail
       It is basically the Smart algorithm that represents the way that a human would play. Of course a Human would
       choose to play the word that has the biggest score, but for many reasons (unknown word, could not think of it,
       not focused e.t.c.) he might not play the best option. So, for this we add a probability indicating if the
       computer will know a word or not. This means that the computer will play only the best option of a sublist,
       so it might be the second-best choice, third or even the first as well.
    """
    return None

# Initializing the game, menu, loading dictionary and giving the choice to the player about the algorithm that the CPU
# will use.
new_game = classes.Game()
new_game.initialize_menu()
dictionary = new_game.load_dictionary_7()
mode = new_game.select_mode()

while mode != '1':
    if mode == 'q':
        print("Exiting game")
        exit(0)
    elif mode == '2':
        new_game.open_score_file()
        new_game.initialize_menu()
        mode = new_game.select_mode()
    elif mode == '3':
        print(help(guidelines))
        new_game.initialize_menu()
        mode = new_game.select_mode()

option_algorithm = new_game.options()
if option_algorithm == '4':  # If the player chooses Smart-Fail algorithm, the following percentage defines how "stupid"
    # the cpu plays.
    percentage = new_game.fail_probability()

# If player chooses new game, then game starts.
if mode == '1':
    # Variables needed for the execution
    temp = []
    current_turn = 0
    keyboard_input = ''
    sack = classes.SakClass()

    # Now the players have to get randomly 7 letters to start their match
    human = classes.Human([], 0)
    cpu = classes.CPU([], 0)
    cpu.currentPlay = option_algorithm
    human.pickLetters(sack)
    cpu.pickLetters(sack)
    if option_algorithm == '4':
        cpu.percentage = percentage
    while len(sack.get_Sack()) >= 7:
        humanAnswer = human.chooseWord(sack)
        if humanAnswer == 1:
            break
        if len(sack.get_Sack()) >= 7:
            cpuAnswer = cpu.chooseWord(sack)
        else:
            break
    new_game.final_scores(cpu.points, human.points)
    new_game.save_scores(cpu.points, human.points)
# In this choice, the player will get a log file with scores

