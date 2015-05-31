
class SpellChecker(object):

    def __init__(self):
        self.myWords = []

    def addWord( self, aWord ):
        self.myWords.append( aWord )

    def checkWord( self, aWordToCheck ):
        theWordsToCheck = self.generateWordOptions(aWordToCheck)
        #print list(theWordsToCheck)
        for theWordToCheck in theWordsToCheck:
            if theWordToCheck in self.myWords:
                return theWordToCheck
        return "no correction found"

    def generateWordOptions( self, aWordToCheck ):
        theWordOptions = [ aWordToCheck, aWordToCheck.lower(), aWordToCheck.capitalize() ]
        theWordOptions.extend( self.generateWordOptionsByRemovingRepeatingCharactersWithCaseVariations( aWordToCheck ) )
        self.sortTheWordOptionsByDescendingLengthToPreferTheLongestMatch(theWordOptions)
        return theWordOptions

    def generateWordOptionsByRemovingRepeatingCharactersWithCaseVariations(self, aWordToCheck):
        theLowerCaseWordOptions = list( self.generateWordOptionsByRemovingRepeatingCharacters( aWordToCheck.lower() ) )
        theLowerCaseWordOptions.extend( self.convertWordsToMixedCase( theLowerCaseWordOptions ) )
        return theLowerCaseWordOptions

    def sortTheWordOptionsByDescendingLengthToPreferTheLongestMatch(self, aWordOptions):
        aWordOptions.sort(key=len, reverse=True)

    def convertWordsToMixedCase(self, aWords):
        return [ self.convertToMixedCase( theWord ) for theWord in aWords ]

    def convertToMixedCase(self, aWord):
        return self.capitalizeLettersAfterPunctuation( aWord.capitalize() )

    def capitalizeLettersAfterPunctuation(self, aWord):
        theResult = aWord
        for i, c in enumerate(aWord):
            if i < len(aWord) - 1 and not c.isalnum():
                theResult = aWord[:i + 1] + aWord[i + 1:i + 2].upper() + aWord[i + 2:]
        return theResult

    def generateWordOptionsByRemovingRepeatingCharacters(self, aWord):
        theWordOptions = set()

        if len(aWord) <= 1:
            theWordOptions.add(aWord)
        else:
            theFirstLetter = aWord[0:1]
            for theIntermediateWordOption in self.generateWordOptionsByRemovingRepeatingCharacters(aWord[1:]):
                if theFirstLetter == theIntermediateWordOption[0]:
                    theWordOptions.add( theFirstLetter + theIntermediateWordOption[1:] )

                theWordOptions.add( theFirstLetter + theIntermediateWordOption[0:] )

        return theWordOptions

if __name__ == '__main__':

    theSpellChecker = SpellChecker()

    [theSpellChecker.addWord( line.strip() ) for line in open('/usr/share/dict/words')]

    while True:
        theInput = raw_input( 'Enter a word: ' )

        if theInput == 'q!':
            break

        print theSpellChecker.checkWord( theInput )
