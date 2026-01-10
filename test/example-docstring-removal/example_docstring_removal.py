""" This module helps little sister with her vocabulary homework.

    And this is a multi-line module level docstring. It should be
    removed when the representation is processed.
 """


# This function has a docstring, but without a first descriptive
# sentence.  The docstring should be removed.
def add_prefix_un(word):
    """

    :param word: str of a root word
    :return:  str of root word with un prefix

    This function takes `word` as a parameter and
    returns a new word with an 'un' prefix.
    """
    return 'un' + word


def make_word_groups(vocab_words):
    """Create word groups from a list of vocab words.

    :param vocab_words: list of vocabulary words with a prefix.
    :return: str of prefix followed by vocabulary words with
             prefix applied, separated by ' :: '.

    This function takes a `vocab_words` list and returns a string
    with the prefix  and the words with prefix applied, separated
     by ' :: '.
    """

    multi_line_string = """This is a multi-line string.
    This should NOT get cleaned as a docstring, but retained, because it is assigned
    a name, and is therefore a plain string, and not a docstring."""

    return (" :: " + vocab_words[0]).join(vocab_words)


def remove_suffix_ness(word):
    """Remove the suffix of a word.

    :param word: str of word to remove suffix from.
    :return: str of word with suffix removed & spelling adjusted.

    This function takes in a word and returns the base word with `ness` removed.
    """

    MULTI_LINE_CONSTANT = """This is a multi-line string constant.
       This should NOT get cleaned as a docstring, but retained, because it is assigned
       a name, and is therefore a plain string, and not a docstring."""

    return word[:-4] if word[-5] != 'i' else word[:-5] + 'y'


def adjective_to_verb(sentence, index):
    """Turn an adjective form into a verb form.

    :param sentence: str that uses the word in sentence
    :param index:  index of the word to remove and transform
    :return:  str word that changes the extracted adjective to a verb.

    A function takes a `sentence` using the
    vocabulary word, and the `index` of the word once that sentence
    is split apart.  The function should return the extracted
    adjective as a verb.
    """
    return sentence.split()[index].strip(".") + 'en'


# Function with doctests and using single quotes instead of double.
def function_with_doctest():
        '''Generate a list of formatted report strings for tournament results.

         >>> test = (tally(["Courageous Californians;Devastating Donkeys;win",\
                            "Allegoric Alaskans;Blithering Badgers;win",\
                            "Devastating Donkeys;Allegoric Alaskans;loss",\
                            "Courageous Californians;Blithering Badgers;win",\
                            "Blithering Badgers;Devastating Donkeys;draw",\
                            "Allegoric Alaskans;Courageous Californians;draw"]))
         >>> print(type(test))
         <class 'list'>
         >>> print(test[0])
         Team                           | MP |  W |  D |  L |  P
         >>> print(test[1])
         Allegoric Alaskans             |  3 |  2 |  1 |  0 |  7
         >>> print(test[2])
         Courageous Californians        |  3 |  2 |  1 |  0 |  7
         >>> print(test[3])
         Blithering Badgers             |  3 |  0 |  1 |  2 |  1
         >>> print(test[4])
         Devastating Donkeys            |  3 |  0 |  1 |  2 |  1
        '''

        try:
            results = (row.split(';') for row in tournament_results)
            tournament_stats = compile_statistics(results)

        except AttributeError:
            logger.exception(f'There is a problem with the tournament results string: ')
            raise

        except IndexError:
            logger.exception(f'Compiling team statistics failed: ')
            raise

        return make_report(tournament_stats)

# Docstrings for both a class and a function within the class
# (code from std lib datetime class)
class date:
    """Concrete date type.

    Constructors:

    __new__()
    fromtimestamp()
    today()
    fromordinal()

    Operators:

    __repr__, __str__
    __eq__, __le__, __lt__, __ge__, __gt__, __hash__
    __add__, __radd__, __sub__ (add/radd only with timedelta arg)

    Methods:

    timetuple()
    toordinal()
    weekday()
    isoweekday(), isocalendar(), isoformat()
    ctime()
    strftime()

    Properties (readonly):
    year, month, day
    """
    __slots__ = '_year', '_month', '_day', '_hashcode'

    def __new__(cls, year, month=None, day=None):
        """Constructor.

        Arguments:

        year, month, day (required, base 1)
        """
        if (month is None and
            isinstance(year, (bytes, str)) and len(year) == 4 and
            1 <= ord(year[2:3]) <= 12):
            # Pickle support
            if isinstance(year, str):
                try:
                    year = year.encode('latin1')
                except UnicodeEncodeError:
                    # More informative error message.
                    raise ValueError(
                        "Failed to encode latin1 string when unpickling "
                        "a date object. "
                        "pickle.load(data, encoding='latin1') is assumed.")
            self = object.__new__(cls)
            self.__setstate(year)
            self._hashcode = -1
            return self


def only_a_docstring():
    """This s a docstring-only function.

    It is valid, but only because of the docstring (an Expr).
    Removing the docstring creates a fatal error during formatting
    if the docstring is not replaced with pass.
    """

class docstringOny:
    """This is a docstring-only class.

    It should be normalized in the same way the function
    def above is normalized.
    """


class docstringPlusmethod:
    """This is a docstring-only class with a docstring-only method.

    This should be normalized with a pass for
    the class and a pass for the method.

    """

    def docstring_only_method(self):
        """This is a docstring only method.

        This should be normalized with a pass.
        """


def docstring_plus_ellipsis():
    """Function using an Ellipsis object.

    This is a def that uses a docstring and an ellipsis in luie 
    of pass.  The normalizer should remove the docstring but keep 
    the ellipsis.
    """
    ...


class docstringPlusmethod:
    """This is a docstring class with a docstring method.

    Ellipsis is used for a code placeholder.
    This should be normalized with the Ellipsis retained.

    """
    ...

    def docstring_only_method(self):
        """This is a docstring with Ellipsis method.

        This should be normalized with the Ellipsis retained.
        """
        ...
