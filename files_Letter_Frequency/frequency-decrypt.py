from typing import Any
import time
from string import ascii_lowercase


class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in this stack. The end of the list represents
    #     the top of the stack.
    _items: list

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return self._items == []

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if this stack is empty.

        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError('Cannot pop empty stack')
        else:
            return self._items.pop()


class LimitedStack(Stack):
    """
    A last-in-first-out (LIFO) stack of items, but contains a limited number
    of items within.

    === Public Attributes ===
    limit:
        The size limit of the stack

    === Representation Invariants ===
    - 0 <= len(self._items) <= self.limit
    """
    # Attribute Types:
    limit: int

    def __init__(self, limit: int) -> None:
        Stack.__init__(self)
        self.limit = limit

    # the only overridden method - there's no need to override pop since it will
    # function the same
    def push(self, item: Any) -> None:
        """
        Push to the stack if there is space available. Otherwise, make space by
        popping the least-recently added item.
        """
        if len(self._items) < self.limit:
            super().push(item)
        else:
            self._items.pop(0)  # shortcut to remove first item
            super().push(item)

            """
            # or, alternatively, 
            
            temp_stack = []
            while not self.is_empty():
                temp_stack.append(self.pop())
            temp_stack.pop()    # removes first element
            for i in range(len(temp_stack-1)):
                super().push(temp_stack.pop())
            """


class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass


def clear_stack(s: Stack) -> list:
    """
    Clear the stack of all elements, returning a list of elements that were in
    the stack.

    If the stack is already empty, return an empty lit

    >>> my_stack = Stack()
    >>> my_stack.push(1)
    >>> my_stack.push(2)
    >>> my_stack.push(3)
    >>> clear_stack(my_stack)
    [3, 2, 1]
    """
    res = []
    while not s.is_empty():
        res.append(s.pop())
    return res


def peek(s: Stack) -> Any:
    """
    Return the top item on the stack <s>.

    >>> my_stack = Stack()
    >>> my_stack.push(1)
    >>> my_stack.push(2)
    >>> peek(my_stack)
    2
    >>> my_stack.pop()
    2
    """
    if s.is_empty():
        raise EmptyStackError
    top_item = s.pop()
    s.push(top_item)
    return top_item


def size(s: Stack) -> int:
    """Return the number of items in s.

    >>> my_stack = Stack()
    >>> size(my_stack)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size(s)
    3
    """
    side_stack = Stack()
    count = 0
    # Pop everything off <s> and onto <side_stack>, counting as we go.
    while not s.is_empty():
        side_stack.push(s.pop())
        count += 1
    # Now pop everything off <side_stack> and back onto <s>.
    while not side_stack.is_empty():
        s.push(side_stack.pop())
    # <s> is restored to its state at the start of the function call.
    # We consider that it was not mutated.
    return count


def file_to_str(filename: str) -> str:
    """
    Returns the contents of a file <filename> as a string

    (maybe not the best way to carry this out since larger files will
    absolutely crash my macbook)
    """
    with open(filename, 'r') as read_file:
        return read_file.read().lower()


def str_to_dict_char_frequency(letters: str, text_str: str) -> dict[str, int]:
    """
    Returns a dictionary with keys-value pairs of characters in <letters> and
    their occurrences in <text_str> respectively
    """
    occurrences = {letter: 0 for letter in letters.lower()}
    for ch in text_str:
        # only accounts for characters already in the dict: If a character is
        # not already present, it is ignored
        if ch in occurrences:
            occurrences[ch] += 1
    return occurrences


def sort_pairs(freq_dict: dict[str, int]) -> list[tuple[int, str]]:
    """
    Sorts the dictionary into a list by their numerical values
    (i.e., higher occurrence values are at the start of the list)
    """
    return sorted([(val, key) for (key, val) in freq_dict.items()],
                  reverse=True)


def swap_letters(text_str: str, ch1: str, ch2: str) -> str:
    """
    Swap all occurrences of <ch1> in the string <text> with <ch2>.
    Note: The swapping is case-sensitive. It is ideal to have every character
    in text be lowercase, along with each of <ch1> and <ch2>

    Preconditions:
    - len(ch1) == 1
    - len(ch2) == 1
    - <ch1> and <ch2> are present in <text_str>
    """
    return text_str.translate({ord(ch1): ord(ch2),
                               ord(ch2): ord(ch1)})


def frequency_decrypt(text_file: str,
                      characters: str = ascii_lowercase) -> str:
    """
    Frequency Analysis Decryption

    Has some delays to allow user to read messages between inputs if any errors
    arise
    """
    # The text in the file
    text = file_to_str(text_file)

    # A copy of the text if revert is needed
    original_text = text

    # bool to determine whether to print each character and its corresponding
    # frequency in the text
    show_frequency = True

    # makes use of limited stack
    undo_stack, redo_stack = LimitedStack(15), LimitedStack(10)

    while True:
        print(text)
        letters_dict = str_to_dict_char_frequency(characters, text)
        total_num_letters = sum(letters_dict.values())
        sorted_pairs = sort_pairs(letters_dict)

        # since the user may choose to not have the frequency print every time
        # (to save screen space, but this kinda defeats the purpose of using the
        # character frequency for decryption... oh well)
        if show_frequency:
            print('==== Character  Frequency ====')
            for value, char in sorted_pairs:
                percentage = 100 * value / total_num_letters
                print(f'Ch: \'{char}\' || Oc: {value}\t\t{percentage:.2f}%')

        while True:
            user_input = input('\nEnter two characters to swap or type '
                               '\'END\' to exit the program. \nEnter \'HELP\' '
                               'for a list of commands: ')
            if user_input != 'HELP':
                print()
                break
            else:
                # =========
                # help info
                # =========
                print('\n============================')
                print('Enter two (2) characters to swap in the format (s1s2), '
                      '\nwhere s1, s2 are\two unique alphabetic characters. '
                      '\n(example inputs: \'pw\', \'iu\', \'ox\', \'an\')')
                print('========= Commands =========')
                print('\'SHOW\': Shows the character frequency table.\n\t'
                      '- Ch: The character in the string\n\t'
                      '- Oc: The number of occurrences of the letter in the '
                      'string,\n\t\t  along with the percentage.\n'
                      '\'HIDE\': Hides the character frequency table.\n'
                      '\'UNDO\': Undoes the most recent swap operation, '
                      'reverting the \n\t\textracted string to the previous '
                      'iteration.\n'
                      '\'REDO\': Undoes the most recent \'UNDO\' operation.\n'
                      '\'REVERT\': Reverts the text string to the starting '
                      'instance.\n'
                      '\'END\': Exits program\n'
                      '\nNote: Refer to https://en.wikipedia.org/wiki/'
                      'Letter_frequency \nfor chart on relative letter '
                      'frequency in the English language')
                print('============================')
                time.sleep(3.5)

        if user_input == 'END':
            return text
        elif user_input == 'UNDO':
            try:
                text = undo_stack.pop()
                redo_stack.push(text)
            except EmptyStackError:
                pass
        elif user_input == 'REDO':
            try:
                text = redo_stack.pop()
                undo_stack.push(text)
            except EmptyStackError:
                pass
        elif user_input == 'REVERT':
            # reverts to start
            undo_stack.push(text)
            text = original_text
        elif user_input == 'SHOW':
            show_frequency = True
        elif user_input == 'HIDE':
            show_frequency = False
        else:
            # swap the two characters
            try:
                # in case any characters of the user input are not alphabetic
                if not user_input.isalpha():
                    print('Invalid String: Input must be in the format s1s2, '
                          'where s1, s2 are two (2) alphabetic characters '
                          '(i.e., \'dt\', \'hg\', \'px\', \'au\')')
                    time.sleep(2.5)
                    continue
                # previous text instance is stored first, so the very first
                # instance of the text string can still be 'undone' to if
                # needed (without directly reverting)
                undo_stack.push(text)
                text = swap_letters(text, user_input[0].lower(),
                                    user_input[1].lower())

                # since the current text is the latest version (nothing to
                # "redo" anymore)
                clear_stack(redo_stack)
            except IndexError:
                print('Invalid String: Input must be in the format s1s2, where'
                      's1, s2 are two (2) alphabetic characters (i.e., \'dt\', '
                      '\'hg\', \'px\', \'au\')')
                time.sleep(2.5)


if __name__ == '__main__':
    actual = frequency_decrypt('files_Letter_Frequency/sample_text_1.txt')
    expected = file_to_str('files_Letter_Frequency/'
                           'sample_text_1_decrypted.txt')
    print(f"Decrypted? {actual == expected}")
