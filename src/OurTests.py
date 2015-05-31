import unittest
from SpellChecker import SpellChecker

class Test(unittest.TestCase):


    def setUp(self):
        self.mySpellChecker = SpellChecker()
        [self.mySpellChecker.addWord( line.strip() ) for line in open('/usr/share/dict/words')]

    def tearDown(self):
        pass


    def CheckResult(self, anExpected, anInput ):
        theResult = self.mySpellChecker.checkWord( anInput )
        if theResult != anExpected:
            print "Input " + anInput + " failed: expected = " + anExpected + ", actual = " + theResult

    def testCheckResult(self):
        self.CheckResult( "Aaron", "Aaron" )
        self.CheckResult( "aardvark", "aardvark" )
        self.CheckResult( "aardvark", "AARDvark" )
        self.CheckResult( "aardvark", "AaRDvark" )
        self.CheckResult( "aardvark", "AAAAAAAaRDvark" )
        self.CheckResult( "aardvark", "aaaaaarddddvaaaaaark" )
        self.CheckResult( "platypus", "platypus" )
        self.CheckResult( "bookkeeper", "bookkeeper" )
        self.CheckResult( "bookkeeper", "boOkKeEper" )
        self.CheckResult( "bookkeeper", "boookkkeeeper" )
        self.CheckResult( "subbookkeeper", "subbookkeeper" )
        self.CheckResult( "subbookkeeper", "sUbbOOkkEEpEr" )
        self.CheckResult( "mele", "mele" )
        self.CheckResult( "melee", "melee" )
        self.CheckResult( "melee", "mellee" ) #// or "mele" can also be a valid correction
        self.CheckResult( "melee", "mmeelleeee" ) #// or "mele" can also be a valid correction
        self.CheckResult( "melee", "mMEelLeEEe" ) #// or "mele" can also be a valid correction
        self.CheckResult( "carrot", "CaRrOt" )
        self.CheckResult( "phone", "pPhone" )
        self.CheckResult( "Boolian", "Boolian" )
        self.CheckResult( "Boolian", "BOOLian" )
        self.CheckResult( "Boolian", "boolian" )
        self.CheckResult( "Boolian", "boolIaN" )
        self.CheckResult( "Boolian", "bOoLiAn" )
        self.CheckResult( "Xyris", "Xyris" )
        self.CheckResult( "Xyris", "xyris" )
        self.CheckResult( "Xyris", "XYRIS" )
        self.CheckResult( "Xyris", "XyRiS" )
        self.CheckResult( "Xyris", "xYrIs" )
        self.CheckResult( "Xyris", "xYRIs" )

        self.CheckResult( "duck", "duck" )
        self.CheckResult( "duck", "duucck" )

        self.CheckResult( "no correction found", "Shyela" )
        self.CheckResult( "no correction found", "Toyota" )

        self.CheckResult( "carrot", "CarOt" )  #// extra credit

        # --------------------- ADDITIONAL

        self.CheckResult( "poop", "poop" )
        self.CheckResult( "pop", "pop" )
        self.CheckResult( "Pop", "Pop" )
        self.CheckResult( "loop", "looooopppp" )



if __name__ == "__main__":
    #import syssys.argv = ['', 'Test.testName']
    unittest.main()