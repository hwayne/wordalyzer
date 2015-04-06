import wordalyzer as w
import unittest

add_words = w.add_to_word_counter
class Tests(unittest.TestCase):

    def testDoesNothingToWord(self):
        self.assertEqual(w.trim_punctuation("yesoch"), "yesoch")

    def testRemovesPeriodsAtEnd(self):
        self.assertEqual(w.trim_punctuation("yesoch."), "yesoch")

    def testRemovesPeriodsInMiddle(self):
        self.assertEqual(w.trim_punctuation("yes.?och."), "yesoch")

    def testDoesNotRemoveSpaces(self):
        self.assertEqual(w.trim_punctuation("hail yesoch"), "hail yesoch")

    def testDoesNothingToEmptyString(self):
        self.assertEqual(w.trim_punctuation(""), "")

    def testAddingNoWordsAddsNoWords(self):
        word_list = {'a': 3}
        self.assertDictEqual(w.add_to_word_counter("", word_list), word_list)

    def testAddsOneWordToCounter(self):
        word_list = {'a': 2}
        self.assertDictEqual(w.add_to_word_counter("a", word_list), {'a': 3})

    def testCreatesWordIfNotInDict(self):
        word_list = {}
        self.assertDictEqual(w.add_to_word_counter("a", word_list), {'a': 1})

    def testAddsTwoWords(self):
        word_list = {'a': 1, 'b': 1}
        self.assertDictEqual(add_words("a b", word_list), {'a': 2, 'b': 2})

    def testIgnoresCase(self):
        word_list = {'a': 1}
        self.assertDictEqual(w.add_to_word_counter("A", word_list), {'a': 2})

    def testIgnoresPunctuation(self):
        word_list = {'a': 1}
        self.assertDictEqual(w.add_to_word_counter(".a", word_list), {'a': 2})

    def testIgnoresNewlines(self):
        word_list = {'a': 1}
        to_test = """a
        """
        self.assertDictEqual(w.add_to_word_counter(to_test, word_list), {'a': 2})

    def testTurnsDictToTuple(self):
        word_list = {'a': 1}
        self.assertEqual(w.make_readable(word_list), [('a', 1)])

    def testSortsItemsByFreq(self):
        word_list = {'a': 1, 'b': 3, 'c': 2}
        self.assertEqual(w.make_readable(word_list), [('b', 3), ('c', 2), ('a', 1)])

    def testAddsTwoItems(self):
        words = "I am red"
        self.assertEqual(w.markov_chain(words)[("I", "am")], ["red"])

    def testKeepsPunctuation(self):
        words = "I am. red"
        self.assertEqual(w.markov_chain(words)[("I", "am.")], ["red"])

    def testMakesMultiplePrefixes(self):
        words = "I am red and blue"
        output = w.markov_chain(words)
        self.assertEqual(output[("I", "am")], ["red"])
        self.assertEqual(output[("red", "and")], ["blue"])

    def testMakesMultipleSuffixes(self):
        words = "I am red I am blue"
        output = w.markov_chain(words)
        self.assertEqual(output[("I", "am")], ["red", "blue"])

    def testTakesThree(self):
        words = "I am red and blue"
        output = w.markov_chain(words, 3)
        self.assertEqual(output[("I", "am", "red")], ["and"])

    def testTurnsChainsToText(self):
        chain = w.markov_chain("I am red and blue", 2)
        output = w.chain_to_text(chain, 1)
        self.assertEqual(output[0], "I")

    def testDoesNotBreakIfNoMatchingPrefix(self):
        chain = w.markov_chain("I", 2)
        output = w.chain_to_text(chain, 200)
        # No error

    def testHasSizeWords(self):
        chain = w.markov_chain("I am red and blue", 2)
        output = w.chain_to_text(chain, 20)
        self.assertEqual(len(output), 20)

    def testUsesMostRecentWords(self):
        chain = w.markov_chain("I am red", 2)
        output = w.chain_to_text(chain, 3)
        self.assertEqual(output, ['I', 'am', 'red'])

    def testUsesRandomSample(self):
        chain = w.markov_chain("I am red I am blue", 2)
        output = w.chain_to_text(chain, 30)
        self.assertIn('red', output)
        self.assertIn('blue', output)

    def testUsesSizeOfDict(self):
        chain = w.markov_chain("I am red", 3)
        output = w.chain_to_text(chain, 3)
        self.assertEqual(output, ['I', 'am', 'red'])

if __name__ == "__main__":
    unittest.main()
