from BloomFilter import BloomFilter

class BloomSpellChecker(object):

    def __init__(self):
        self.myBloomFilter = BloomFilter()

    def addWord( self, aWord ):
        self.myBloomFilter.addWord(aWord)

    def checkWord( self, aWordToCheck ):
        for theWordToCheck in self.generateWordOptions(aWordToCheck):
            if self.myBloomFilter.checkWord( theWordToCheck ):
                return theWordToCheck
        return "no correction found"

    def generateWordOptions( self, aWordToCheck ):
        theWordOptions = [ aWordToCheck, aWordToCheck.lower(), aWordToCheck.capitalize() ]
        theWordOptions.extend( self.generateWordOptionsByRemovingRepeatingCharacters( aWordToCheck ) )
        theWordOptions.extend( self.generateWordOptionsByRemovingRepeatingCharacters( aWordToCheck.lower() ) )
        theWordOptions.extend( self.generateWordOptionsByRemovingRepeatingCharacters( aWordToCheck.capitalize() ) )
        return theWordOptions

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

    theSpellChecker = BloomSpellChecker()

    [theSpellChecker.addWord( line.strip() ) for line in open('/usr/share/dict/words')]

    while True:
        theInput = raw_input( 'Enter a word: ' )

        if theInput == 'q!':
            break

        print theSpellChecker.checkWord( theInput )
