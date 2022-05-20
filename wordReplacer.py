from scipy.stats import poisson
import numpy as np
import random

class WordReplacer:
    def __init__(self, word2id, usePoisson=False, useCache=False, cacheCoef=5.0, ignoreFirst=0):
        '''
        word2id: a dictionary of word to idx like {a:1, b:2, ...}
        usePoisson: use poisson weighting consiering word length if true
        useCache: use cache for fast sampling of length if true
        cacheCoef: sample vocabSize*cacheCoed words for cache
        ignoreFirst: ignore first N tokens of vocabulary.
                     Used for special tokens basically allocated small idxs.
        '''

        self.usePoisson = usePoisson
        self.useCache = useCache
        self.cacheCoef = cacheCoef
        self.vocabSize = len(word2id)
        self.idList = list(range(self.vocabSize))
        self.ignoreFirst = ignoreFirst
        
        if self.usePoisson:
            self.__build(word2id)

    def __build(self, word2id):
        lengths = [len(w) for w, i in sorted(word2id.items(), key=lambda x:x[1])]
        self.id2length = {i:l for i, l in enumerate(lengths)}
        maxLength = max(lengths)

        # poissonTable (maxLength x maxLength)
        poissonTable = [[poisson.pmf(mu=mu+1, k=k+1) for k in range(maxLength)] 
                         for mu in range(maxLength)]
            
        print('>>> BUILD SAMPLING TABLE')
        # table for sampling (maxLength x vocabSize)
        self.samplingTable = [[poissonTable[mu][l-1] for l in lengths]
                              for mu in range(maxLength)]
        self.samplingTable = np.array(self.samplingTable)
        self.samplingTable = self.samplingTable / self.samplingTable.sum(axis=1, keepdims=True)

        print('>>> BUILD CAHCE TABLE')
        if self.useCache:
            # CACHE of sampled words
            self.cacheTable = [random.choices(self.idList[self.ignoreFirst:],
                                              k=int(self.vocabSize*self.cacheCoef),
                                              weights=self.samplingTable[mu][self.ignoreFirst:]) 
                               for mu in range(maxLength)]

    def sampleWord(self, wordId, wordLength=-1):
        if self.usePoisson:
            if wordLength<0:
                wordLength = self.id2length[wordId]
            if self.useCache:
                return random.choice(self.cacheTable[wordLength-1])
            else:
                return random.choices(self.idList[self.ignoreFirst:],
                                      k=1,
                                      weights=self.samplingTable[wordLength-1])[0]
        else:
            return random.randint(self.ignoreFirst, self.vocabSize-1)

    def perturb(self, idss, rate, ignoreIdx=None):
        # idss is a batch of ids like [[1,2,3], [3,4,5,6]]
        if rate==0.0:
            return idss

        idss = [[self.sampleWord(i)
               if i!=ignoreIdx and random.random()<rate else i
               for i in ids] for ids in idss]

        return idss

if __name__=='__main__':
    word2id = {'a'*(i+1):i for i in range(5)}
    word2id['bbb'] = len(word2id)
    wrp = WordReplacer(word2id, True, True)
    print(wrp.sampleWord(2))
