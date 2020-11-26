import random
import string

WORDLIST_FILENAME = "words.txt"
WARNING_TYPES = ['BAD_LETTER', 'ALREADY_TYPED']


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if set(secret_word)&set(letters_guessed) == set(secret_word):
        return True
    else:
        return False

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    res = ''
    guessed_letters = set(secret_word) & set(letters_guessed)
    for i in secret_word:
        if i not in guessed_letters:
            res += '_ '
        else:
            res += i
    return res


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    letters_list_new = sorted(set(all_letters)-set(letters_guessed))
    return "".join(letters_list_new)

def greetings(warnings_remaining, guesses_remaining, secret_word, letters_guessed):
    print(f'Welcome to the game Hangman!\nI am thinking of a word that is {len(choose_word(wordlist))} letters long.')
    print(f'You have {warnings_remaining} warnings left.')
    print(f'You have {guesses_remaining} guesses left.')
    print(f'Available letters: {get_available_letters(letters_guessed)}')

def warning(secret_word, letters_guessed, warnings_remaining, warning_type):
    if warning_type == WARNING_TYPES[0]:
        print(f'Oops! That is not a valid letter. You have {warnings_remaining} '
              f'warnings left: {get_guessed_word(secret_word, letters_guessed)}')
    elif warning_type == WARNING_TYPES[1]:
        print(f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: "
              f"{get_guessed_word(secret_word, letters_guessed)}")

def incorrect_letter(secret_word, letters_guessed):
    print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')

def show_status(guesses_remaining, warnings_remaining):
    print(f'You have {guesses_remaining} guessed left \n'
          f'You have {warnings_remaining} warnings left')

def say_word_guessed(secret_word, letters_guessed):
    print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')


def end(secret_word, letters_guessed, guesses_remaining):
    if is_word_guessed(secret_word, letters_guessed):
        print(f'Congratulations, you won!\n Your total score for this game is: {guesses_remaining*len(set(list(secret_word)))}')
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''

    vowels = 'aeiou'

    warnings_remaining = 3
    guesses_remaining = 6
    letters_guessed = []
    user_input = set()

    greetings(warnings_remaining, guesses_remaining, letters_guessed, secret_word)

    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        letter = input('Please guess a letter: ').lower()
        print(letter)

        if letter not in list(string.ascii_lowercase):
            if warnings_remaining > 0:
                warnings_remaining -= 1
            else:
                guesses_remaining -= 1
            warning(secret_word, letters_guessed, warnings_remaining, WARNING_TYPES[0])
        elif letter in user_input:
            if warnings_remaining > 0:
                warnings_remaining -= 1
            else:
                guesses_remaining -= 1
            warning(secret_word, letters_guessed, warnings_remaining, WARNING_TYPES[1])
        elif letter in secret_word:
            letters_guessed.append(letter)
            say_word_guessed(secret_word, letters_guessed)
        else:
            incorrect_letter(secret_word, letters_guessed)
            guesses_remaining -= 2 if letter in vowels else 1

        show_status(guesses_remaining, warnings_remaining)
        user_input.add(letter)
        print('-------------')
    end(secret_word, letters_guessed, guesses_remaining)

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    my_word = my_word.replace(' ', '')
    if len(my_word) != len(other_word):
        return False

    pos = 0
    letters = set()

    while pos < len(my_word):
        if my_word[pos] == '_':
            letters.add(other_word[pos])
        elif my_word[pos] != other_word[pos]:
            return False
        pos += 1

    if len(letters & set(my_word)) > 0:
        return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word, end=' ')



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []
    user_input = set()
    vowels = 'aeiou'

    greetings(warnings_remaining, guesses_remaining, secret_word, letters_guessed)

    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        letter = input('Please guess a letter: ').lower()
        print(letter)
        if letter == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        elif letter not in list(string.ascii_lowercase):
            if warnings_remaining > 0:
                warnings_remaining -= 1
            else:
                guesses_remaining -= 1
            warning(secret_word, letters_guessed, warnings_remaining, WARNING_TYPES[0])
        elif letter in user_input:
            if warnings_remaining > 0:
                warnings_remaining -= 1
            else:
                guesses_remaining -= 1
            warning(secret_word, letters_guessed, warnings_remaining, WARNING_TYPES[1])
        elif letter in secret_word:
            letters_guessed.append(letter)
            say_word_guessed(secret_word, letters_guessed)
        else:
            incorrect_letter(secret_word, letters_guessed)
            guesses_remaining -= 2 if letter in vowels else 1

        show_status(guesses_remaining, warnings_remaining)
        user_input.add(letter)
        print('-------------')
    end(secret_word, letters_guessed, guesses_remaining)
if __name__ == "__main__":
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
    #hangman(secret_word)
