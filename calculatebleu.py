import sys
import math
import os


class BleuScore:
    candLines = []
    refLines = []
    bleuScoreList = []

    candNgrams = []
    refNgrams = []

    candCorpusLen = 0
    refCorpusLen = 0

    multipleRef = False

    def readFiles(self, candidateFile, referenceFile):

        #candidateFile = "cand4.txt"
        #referenceFile = "files/"

        if os.path.isdir(referenceFile):
            self.multipleRef = True
            referenceDir = referenceFile
            for everyRefFile in os.listdir(referenceDir):
                with open(referenceDir + everyRefFile, encoding='utf8') as ref:
                    linesList = []
                    for line in ref:
                        linesList.append(line.strip())
                    self.refLines.append(linesList)

            with open(candidateFile, encoding='utf8') as candFile:
                for line in candFile:
                    self.candLines.append(line.strip())


        else:
            # Read candidate File
            # with open("cand.txt",encoding='utf8') as candFile:
            with open(candidateFile, encoding='utf8') as candFile:
                for line in candFile:
                    self.candLines.append(line.strip())

            # with open("ref.txt",encoding='utf8') as refFile:
            with open(referenceFile, encoding='utf8') as refFile:
                for line in refFile:
                    self.refLines.append(line.strip())

                    # print(self.candLines)

    def getNgrams(self, lines, n):
        nGramsList = []
        for line in lines:
            lineNgramsDict = {}

            words = line.split()
            # print(words)

            if len(words) < n:
                combinedStr = ""
                count = 0
                for word in words:
                    if count == 0:
                        combinedStr = word
                    else:
                        combinedStr = combinedStr + " " + word
                    count = count + 1

                # print(str(n) + "    " + combinedStr)
                if combinedStr not in lineNgramsDict:
                    lineNgramsDict[combinedStr] = 1
                else:
                    lineNgramsDict[combinedStr] += 1
                # print(lineNgramsDict)
                nGramsList.append(lineNgramsDict)

            else:
                for wordIndex in range(0, len(words) - n + 1):
                    # for index in range(0,n):
                    firstIndex = wordIndex
                    lastIndex = wordIndex + n
                    combinedStr = ""
                    count = 0
                    for nGramIndex in range(firstIndex, lastIndex):
                        if count == 0:
                            combinedStr = words[nGramIndex]
                        else:
                            combinedStr = combinedStr + " " + words[nGramIndex]
                        count = count + 1
                    # print(str(n) + "    " + combinedStr)
                    if combinedStr not in lineNgramsDict:
                        lineNgramsDict[combinedStr] = 1
                    else:
                        lineNgramsDict[combinedStr] += 1
                # print(lineNgramsDict)
                nGramsList.append(lineNgramsDict)

        return nGramsList


    def getNgramsForMultipleRef(self, refList, n):
        nGramsList = []
        for reference in refList:
            nGramsListForRef = []
            for line in reference:
                lineNgramsDict = {}

                words = line.split()
                # print(words)

                if len(words) < n:
                    combinedStr = ""
                    count = 0
                    for word in words:
                        if count == 0:
                            combinedStr = word
                        else:
                            combinedStr = combinedStr + " " + word
                        count = count + 1

                    # print(str(n) + "    " + combinedStr)
                    if combinedStr not in lineNgramsDict:
                        lineNgramsDict[combinedStr] = 1
                    else:
                        lineNgramsDict[combinedStr] += 1
                    # print(lineNgramsDict)
                    nGramsList.append(lineNgramsDict)

                else:
                    for wordIndex in range(0, len(words) - n + 1):
                        # for index in range(0,n):
                        firstIndex = wordIndex
                        lastIndex = wordIndex + n
                        combinedStr = ""
                        count = 0
                        for nGramIndex in range(firstIndex, lastIndex):
                            if count == 0:
                                combinedStr = words[nGramIndex]
                            else:
                                combinedStr = combinedStr + " " + words[nGramIndex]
                            count = count + 1
                        # print(str(n) + "    " + combinedStr)
                        if combinedStr not in lineNgramsDict:
                            lineNgramsDict[combinedStr] = 1
                        else:
                            lineNgramsDict[combinedStr] += 1
                    # print(lineNgramsDict)
                    nGramsListForRef.append(lineNgramsDict)
            nGramsList.append(nGramsListForRef)
        return nGramsList



    def countNgrams(self, n):
        nGramCandCount = 0
        if n == 1:
            wordCount = 0
            for innerDict in self.candNgrams:
                for word in innerDict:
                    wordCount += innerDict[word]
            self.candCorpusLen = wordCount
            nGramCandCount = self.candCorpusLen


            if self.multipleRef:
                reference1 = self.refNgrams[0]
                lenOfRef = len(reference1)
                refCorpusLen = 0
                for index in range(0,lenOfRef):
                    refCorpusLenList = []
                    prevWordCountRef = 9999999999
                    for reference in self.refNgrams:
                        wordCountRef = 0
                        wordCountCand = 0
                        innerDictRef = reference[index]
                        innerDictCand = self.candNgrams[index]
                        for word in innerDictRef:
                            wordCountRef += innerDictRef[word]
                        for word in innerDictCand:
                            wordCountCand += innerDictCand[word]

                        if abs(wordCountCand-wordCountRef) < abs(wordCountCand-prevWordCountRef):
                             prevWordCountRef = wordCountRef
                    refCorpusLen += prevWordCountRef

                self.refCorpusLen = refCorpusLen
                print(self.refCorpusLen)

            else:
                wordCount=0
                for innerDict in self.refNgrams:
                    for word in innerDict:
                        wordCount += innerDict[word]
                self.refCorpusLen = wordCount

        else:
            count = 0
            for innerDict in self.candNgrams:
                for word in innerDict:
                    count += innerDict[word]
            nGramCandCount = count

        return nGramCandCount

    def calBleuScoreForEachNGram(self):
        for n in range(1, 5):
            self.candNgrams = self.getNgrams(self.candLines, n)


            if self.multipleRef:
                self.refNgrams = self.getNgramsForMultipleRef(self.refLines, n)
            else:
                self.refNgrams = self.getNgrams(self.refLines, n)

            nGramCandCount = self.countNgrams(n)
            # print(str(n) + "   Ref NGrams   " + str(self.refNgrams))


            if self.multipleRef:
                mainRefCorpus = []
                index = 0
                scoreForNGram = 0
                #refCorpus = []
                for candLine in self.candNgrams:
                    lineScore = 0
                    for cand in candLine:
                        refCountList = []
                        candCount = 0
                        wordInRef = False
                        for reference in self.refNgrams:
                            refLine = reference[index]
                            if cand in refLine:
                                wordInRef = True
                                candCount = candLine[cand]
                                refCountList.append(refLine[cand])
                                #refCorpus.append(refLine)

                        if wordInRef:
                            refCount = max(refCountList)

                            if candCount < refCount:
                                lineScore += candCount
                            else:
                                lineScore += refCount
                    scoreForNGram += lineScore
                    index += 1
                nGramPercent = scoreForNGram / nGramCandCount
                self.bleuScoreList.append(nGramPercent)


            else:
                index = 0
                scoreForNGram = 0
                for candLine in self.candNgrams:
                    refLine = self.refNgrams[index]
                    lineScore = 0
                    for cand in candLine:
                        if cand in refLine:
                            candCount = candLine[cand]
                            refCount = refLine[cand]

                            if candCount < refCount:
                                lineScore += candCount
                            else:
                                lineScore += refCount
                    scoreForNGram += lineScore
                    index += 1
                nGramPercent = scoreForNGram / nGramCandCount
                self.bleuScoreList.append(nGramPercent)

        #print(self.bleuScoreList)

    # BLEU= BP· exp(∑wn log pn)

    def calBleuScore(self):
        blueScore = 0

        sum = 0
        for ngramResult in self.bleuScoreList:
            precision = math.log(ngramResult)
            weight = 1 / 4  # N = 4
            sum += weight * precision
        expValue = math.exp(sum)

        BrevityPenalty = 0
        if self.candCorpusLen > self.refCorpusLen:
            BrevityPenalty = 1
        else:
            BrevityPenalty = math.exp(1 - (self.refCorpusLen / self.candCorpusLen))

        blueScore = BrevityPenalty * expValue

        # print(blueScore)

        outFile = open('bleu_out.txt', 'w')
        outFile.write(str(blueScore))
        outFile.close()


bleuObj = BleuScore()
bleuObj.readFiles(sys.argv[1], sys.argv[2])
#bleuObj.readFiles("candy.txt", "refy.txt")
bleuObj.calBleuScoreForEachNGram()
bleuObj.calBleuScore()