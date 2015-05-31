import unittest
from BloomSpellChecker import BloomSpellChecker

class Test(unittest.TestCase):

    def setUp(self):
        self.mySpellChecker = BloomSpellChecker()

    def tearDown(self):
        pass

    def testCheckWordReturnsSameIfCorrect(self):
        self.mySpellChecker.addWord( "foo" )
        self.assertEqual( "foo", self.mySpellChecker.checkWord( "foo" ), "checkWord() did not return the original when it was correct" )

    def testCheckWordReturnsMessageIfNoCorrectionFound(self):
        self.assertEqual( "no correction found", self.mySpellChecker.checkWord( "foo" ), "checkWord() did not return the correct message when no correction found" )

    def testCheckWordCorrectsMixedAndTitleCaseToLowerCase(self):
        self.mySpellChecker.addWord( "carrot" )
        self.assertEqual( "carrot", self.mySpellChecker.checkWord( "CaRrOT" ), "checkWord() did not correct mixed case to lower case" )
        self.assertEqual( "carrot", self.mySpellChecker.checkWord( "Carrot" ), "checkWord() did not correct title case to lower case" )

    def testCheckWordCorrectsLowerAndMixedCaseToTitleCase(self):
        self.mySpellChecker.addWord( "Moscow" )
        self.assertEqual( "Moscow", self.mySpellChecker.checkWord( "mosCow" ), "checkWord() did not correct mixed case to title case" )
        self.assertEqual( "Moscow", self.mySpellChecker.checkWord( "moscow" ), "checkWord() did not correct lower case to title case" )

    def testCheckWordCorrectsLowerAndTitleCaseToMixedCase(self):
        self.mySpellChecker.addWord( "Jean-Pierre" )
        self.assertEqual( "Jean-Pierre", self.mySpellChecker.checkWord( "Jean-pierre" ), "checkWord() did not correct to mixed case" )
        self.assertEqual( "Jean-Pierre", self.mySpellChecker.checkWord( "jean-pierre" ), "checkWord() did not correct to mixed case" )

    def testCheckWordCorrectsRepeatingCharactersAtBeginning(self):
        self.mySpellChecker.addWord( "phone" )

        self.assertEqual( "phone", self.mySpellChecker.checkWord( "pphone" ), "checkWord() did not correct repeating first character" )
        self.assertEqual( "phone", self.mySpellChecker.checkWord( "ppphone" ), "checkWord() did not correct repeating first character" )

    def testCheckWordCorrectsRepeatingCharactersAtBeginningAndNotLater(self):
        self.mySpellChecker.addWord( "pope" )

        self.assertEqual( "pope", self.mySpellChecker.checkWord( "ppope" ), "checkWord() did not correct repeating first character" )
        self.assertEqual( "pope", self.mySpellChecker.checkWord( "pppope" ), "checkWord() did not correct repeating first character" )

    def testCheckWordCorrectsRepeatingCharactersInMiddle(self):
        self.mySpellChecker.addWord( "phone" )

        self.assertEqual( "phone", self.mySpellChecker.checkWord( "phoone" ), "checkWord() did not correct repeating middle character" )
        self.assertEqual( "phone", self.mySpellChecker.checkWord( "phoooone" ), "checkWord() did not correct repeating middle character" )

    def testCheckWordCorrectsRepeatingCharactersInMultiplePlaces(self):
        self.mySpellChecker.addWord( "phone" )

        self.assertEqual( "phone", self.mySpellChecker.checkWord( "pphhhone" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "phone", self.mySpellChecker.checkWord( "pphooone" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "phone", self.mySpellChecker.checkWord( "pphonnne" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "phone", self.mySpellChecker.checkWord( "pphoneee" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "phone", self.mySpellChecker.checkWord( "pphhoonnee" ), "checkWord() did not correct repeating character all over the place" )

    def testCheckWordCorrectsRepeatingCharactersAtBeginningWithNaturalRepeats(self):
        self.mySpellChecker.addWord( "jazzer" )

        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjazzer" ), "checkWord() did not correct repeating first character" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjjazzer" ), "checkWord() did not correct repeating first character" )

    def testCheckWordCorrectsRepeatingCharactersAtBeginningAndNotLaterWithNaturalRepeats(self):
        self.mySpellChecker.addWord( "sassy" )

        self.assertEqual( "sassy", self.mySpellChecker.checkWord( "ssassy" ), "checkWord() did not correct repeating first character" )
        self.assertEqual( "sassy", self.mySpellChecker.checkWord( "sssassy" ), "checkWord() did not correct repeating first character" )

    def testCheckWordCorrectsRepeatingCharactersInMiddleWithNaturalRepeats(self):
        self.mySpellChecker.addWord( "jazzer" )

        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jaazzer" ), "checkWord() did not correct repeating middle character" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jaaazzer" ), "checkWord() did not correct repeating middle character" )

        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jaazzzer" ), "checkWord() did not correct repeating middle character" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jaaazzzzer" ), "checkWord() did not correct repeating middle character" )

    def testCheckWordCorrectsRepeatingCharactersInMultiplePlacesWithNaturalRepeats(self):
        self.mySpellChecker.addWord( "jazzer" )

        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjazzer" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjaazzer" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjaazzzer" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjaazzzeer" ), "checkWord() did not correct repeating character all over the place" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "jjaazzzeerr" ), "checkWord() did not correct repeating character all over the place" )

    def testCheckWordCorrectsMixedAndTitleCaseToLowerCaseAndRemovesRepeats(self):
        self.mySpellChecker.addWord( "carrot" )
        self.assertEqual( "carrot", self.mySpellChecker.checkWord( "CaRrrOT" ), "checkWord() did not correct mixed case to lower case" )
        self.assertEqual( "carrot", self.mySpellChecker.checkWord( "CarrotT" ), "checkWord() did not correct title case to lower case" )

    def testCheckWordCorrectsMixedAndTitleCaseToLowerCaseAndRemovesRepeatsWithNaturalRepears(self):
        self.mySpellChecker.addWord( "jazzer" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "JaZZzeR" ), "checkWord() did not correct mixed case to lower case" )
        self.assertEqual( "jazzer", self.mySpellChecker.checkWord( "Jazzeer" ), "checkWord() did not correct title case to lower case" )

    def testCheckWordCorrectsLowerAndMixedCaseToTitleCaseAndRemovesRepeats(self):
        self.mySpellChecker.addWord( "Moscow" )
        self.assertEqual( "Moscow", self.mySpellChecker.checkWord( "moscCoow" ), "checkWord() did not correct mixed case to title case" )
        self.assertEqual( "Moscow", self.mySpellChecker.checkWord( "mossscoww" ), "checkWord() did not correct lower case to title case" )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()