from bitarray import bitarray
import hashlib
import struct
import math

class BloomFilter(object):

    def __init__(self, aHasher = None):
        if ( aHasher is None ):
            self.myHasher = Hasher()
        else:
            self.myHasher = aHasher

        theBitArraySize = self.myHasher.getBitArraySize()
        self.myBitArray = bitarray( theBitArraySize )
        self.myBitArray.setall(False)

    def addWord(self, aWord):
        theIndexes = self.myHasher.getIndexesForWord(aWord, True)
        for theIndex in theIndexes:
            self.myBitArray[theIndex] = True

    def checkWord(self, aWord):
        theIndexes = self.myHasher.getIndexesForWord(aWord)
        for theIndex in theIndexes:
            if not self.myBitArray[theIndex]:
                return False

        return True

    def printDebuggingData(self, aWord):
        theIndexes = self.myHasher.getIndexesForWord(aWord)
        print 'theIndexes = ' + str( theIndexes )

        theBits = []
        for theIndex in theIndexes:
            theBits.append( self.myBitArray[theIndex] )

        print 'theBits = ' + str( theBits )


class Hasher(object):

    NUM_BYTES_ENCODE = 3
    NUM_INDEXES = 5

    def getBitArraySize(self):
        return 2**(8*self.NUM_BYTES_ENCODE)

    def getHashForWord(self, aWord):
        return hashlib.sha256(aWord).digest()

    def getIndexesForWord(self, aWord, aGoingToAddWordFlag = False):
        theHash = Hash( self.getHashForWord(aWord), self.NUM_BYTES_ENCODE, self.NUM_INDEXES )
        theResult = theHash.getIndexes()
        return theResult


class TrackingHasher(Hasher):

    def __init__(self):
        super(TrackingHasher, self).__init__()
        self.myIndexCounts = {}
        self.myNumCollisions = 0
        self.myNumWordsAdded = 0

    def getIndexesForWord(self, aWord, aGoingToAddWordFlag = False):
        theResult = super(TrackingHasher, self).getIndexesForWord( aWord, aGoingToAddWordFlag )

        if aGoingToAddWordFlag:
            self.myNumWordsAdded = self.myNumWordsAdded + 1

        for theIndex in theResult:
            if theIndex in self.myIndexCounts:
                self.myIndexCounts[theIndex] = self.myIndexCounts[theIndex] + 1
                self.myNumCollisions = self.myNumCollisions + 1
            else:
                self.myIndexCounts[theIndex] = 1

        return theResult

    def getNumBitsUsed(self):
        return len(self.myIndexCounts)

    def calculateOptimalArraySize(self):
        return int( math.ceil( -( float( self.myNumWordsAdded ) * math.log( 0.0001 ) ) / math.pow( math.log(2.0), 2.0 ) ) )

    def calculateSaturation(self):
        return 100.0 * float(self.getNumBitsUsed()) / float(self.getBitArraySize())

    def calculateOptimalNumHashesForCurrentBitArray(self):
        return self.calculateOptimalHashesForArraySize( self.getBitArraySize() )

    def calculateOptimalNumHashesForOptimalBitArray(self):
        return self.calculateOptimalHashesForArraySize( self.calculateOptimalArraySize() )

    def calculateOptimalHashesForArraySize(self, anArraySize):
        if self.myNumWordsAdded > 0:
            return int( math.ceil( ( float(anArraySize) * math.log(2.0) ) / float( self.myNumWordsAdded ) ) )

        return 0

    def calculateFalsePositiveProbabilityForNumberOfHashes(self, aNumberOfHashes):
        theInnerPower = -1.0 * (float( aNumberOfHashes ) * float(self.myNumWordsAdded)) / float(self.getBitArraySize())
        theInnerExpression = -1.0 * math.expm1(theInnerPower)

        theOuterPower = float( aNumberOfHashes )
        theOuterExpression = math.pow(theInnerExpression, theOuterPower)

        return theOuterExpression * 100.0

    def calculateCurrentFalsePositiveProbability(self):
        return self.calculateFalsePositiveProbabilityForNumberOfHashes(self.NUM_INDEXES)

    def calculateOptimalFalsePositiveProbability(self):
        return self.calculateFalsePositiveProbabilityForNumberOfHashes(self.calculateOptimalNumHashesForCurrentBitArray())

    def hasCollisions(self):
        return self.getNumBitsUsed() < self.myNumWordsAdded * self.NUM_INDEXES

    def getBins(self):
        theBins = []
        theRangeSize = 1 + ( self.getBitArraySize() / 10 )
        for i in xrange( 0, self.getBitArraySize(), theRangeSize ):
            if i > 0:
                theBins.append( i )

        theBins.append( self.getBitArraySize() + 1 )

        return theBins

    def sumIndexCountsForRange(self, aMinValue, aMaxValueExclusive):
        return sum( v for k,v in self.myIndexCounts.iteritems() if k >= aMinValue and k < aMaxValueExclusive )

    def sumIndexCountsIntoBins(self):
        theBinCounts = {}
        theCurrentBinStart = 0

        for theBinEnd in self.getBins():
            theBinCounts[theCurrentBinStart] = self.sumIndexCountsForRange(theCurrentBinStart, theBinEnd)
            theCurrentBinStart = theBinEnd

        return theBinCounts

    def getCollisionsPerWord(self):
        if self.myNumWordsAdded > 0:
            return float(self.myNumCollisions) / float(self.myNumWordsAdded)

        return 0

    def printTrackingData(self):
        print '# words: ' + str( self.myNumWordsAdded )
        print '# collisions: ' + str( self.myNumCollisions )
        print '# collisions / word: ' + str( self.getCollisionsPerWord() )
        print '# bits used: ' + str( self.getNumBitsUsed() )
        print '# bits unused: ' + str( self.getBitArraySize() - self.getNumBitsUsed() )
        print '# bits = ' + str( self.getBitArraySize() )

        print 'optimal # bits = ' + str( self.calculateOptimalArraySize() )
        print 'optimal # hashes for current array = ' + str( self.calculateOptimalNumHashesForCurrentBitArray() )
        print 'optimal # hashes for optimal array = ' + str( self.calculateOptimalNumHashesForOptimalBitArray() )
        print 'saturation: ' + str( self.calculateSaturation() )
        print 'ideal false positive probability: ' + str( self.calculateOptimalFalsePositiveProbability() )
        print 'current false positive probability: ' + str( self.calculateCurrentFalsePositiveProbability() )
#        print 'has collisions: ' + str( self.hasCollisions() )

#        theBinCounts = self.sumIndexCountsIntoBins()
#        print 'theBinCounts = ' + str( theBinCounts )


class Hash(object):

    def __init__(self, aHashString, aNumberOfBytesToEncode, aNumberOfIndexesToReturn):
        self.myHashString = aHashString
        self.myNumberOfBytesToEncode = aNumberOfBytesToEncode
        self.myNumberOfIndexesToReturn = aNumberOfIndexesToReturn

    def getFormatCode(self):
        if self.myNumberOfBytesToEncode == 1:
            return '>B'
        if self.myNumberOfBytesToEncode == 2:
            return '>H'
        elif self.myNumberOfBytesToEncode == 3:
            return '>I'
        elif self.myNumberOfBytesToEncode == 4:
            return '>I'
        elif self.myNumberOfBytesToEncode == 8:
            return '>Q'

    def getEffectiveHashPartLength(self):
        if self.myNumberOfBytesToEncode == 3:
            return 4
        return self.myNumberOfBytesToEncode

    def getPartFromHashString(self, aPartIndex):
        theStartIndex = aPartIndex * self.myNumberOfBytesToEncode
        theEndIndex = theStartIndex + self.myNumberOfBytesToEncode

        thePart = self.myHashString[theStartIndex:theEndIndex]
        if self.myNumberOfBytesToEncode == 3:
            thePart = '\x00' + thePart
        return thePart

    def convertHashToUnsignedNumber(self, aHash):
        theFormatCode = self.getFormatCode()
        theResult = struct.unpack(theFormatCode, aHash)[0]
        return theResult

    def getIndexes(self):
        theNumberOfIndexesInTheHashString = int( math.floor( len(self.myHashString) / self.myNumberOfBytesToEncode) )
        theNumberOfIndexesToParse = min(self.myNumberOfIndexesToReturn, theNumberOfIndexesInTheHashString)

        theResults = []
        for i in xrange( 0, theNumberOfIndexesToParse ):
            theHashPart = self.getPartFromHashString( i )

            if len( theHashPart ) == self.getEffectiveHashPartLength():
                theInt = self.convertHashToUnsignedNumber(theHashPart)
                theResults.append( theInt )

        return theResults
