import numpy as np
from tqdm import tqdm
from scipy.stats import poisson
import random

'''
This word perturbator does not hold compositional subwords information 
for each sentence, but for words in vocabulary by sharing their context
over the entire corpus.
'''

class CompositWordReplacer:
    def __init__(self, word2id, segData,
                 segDataPath=None, 
                 usePoisson=False,
                 wordPieceMode=False, wordPieceSplitSymbol=None,
                 unkToken='<unk>', samplingCacheSize=1000):
        '''
        word2id is a dictionary whose key and value are word and id, respectively.
        segData is a tokenized data, and each sentence must be a list of words. *not ids*
        segDataPath is a path to tokenized raw data. When handling large text data, you can
        use this argument for saving memory usage by open the file with readline(). When
        specifying segDataPath, you can give None as segData to this method.
        
        If wordPieceMode is True, convert intra-word subwords symbol like ##/@@ into 
        sentencepiece format. Say, 'unfortunate ##lly' -> '_unfortunate lly' only when
        building the perturbation candidate list.
        You can specify the type of split symbol of wordpiece using wordPieceSplitSymbol
        '''
        super().__init__()


        self.id2len = {i:len(w) for w,i in word2id.items()}
        self.maxLength = max([len(w) for w in word2id])
        self.splitSymbol = '▁'
        self.wordPieceMode = wordPieceMode
        self.wordPieceSplitSymbol = wordPieceSplitSymbol
        if wordPieceMode:
            assert wordPieceSplitSymbol is not None, 'wordPieceSplitSymbol must be specified when wordPieceMode==True'
        self.unkToken = unkToken

        self.usePoisson = usePoisson
        if self.usePoisson:
            self.poissonTable = [[poisson.pmf(mu=mu+1,k=k+1) for k in range(self.maxLength)] 
                                  for mu in range(self.maxLength)]

        self.__build(word2id, segData, segDataPath)

        # cache for sampling:
        # Cache K=1000 words for each target word as a list, and sample one from the list 
        # can avoid sampling from nonuniform distributino.
        self.samplingCacheSize = samplingCacheSize
        self.__buildSamplingTable(self.samplingCacheSize)

    def __build(self, word2id, segData, segDataPath):
        '''
        compositWordList = [0: [[composit subwords], [weights]]] each row corresponds to wordID
        '''
        if self.wordPieceMode:
            # handle word2id and segdata for wordpiecemode
            def convertWordWP(w):
                if w==self.unkToken:
                    return w
                w = w.replace(self.wordPieceSplitSymbol, '') \
                        if w.startswith(self.wordPieceSplitSymbol) \
                        else self.splitSymbol+w 
                return w
            word2id = {convertWordWP(w):i for w,i in word2id.items()}
            # ---

        print('BUILD...')

        self.compositWordList = [set() for _ in range(len(word2id))]

        if segDataPath is None:
            for line in tqdm(segData):
                compList = self.__extractCompositions(line, word2id)
                for w,cs in zip(compList[0], compList[1]):
                    self.compositWordList[w] |= set(cs)
        else:
            f = open(segDataPath)
            lineCount = 0
            line = f.readline()
            while line:
                line = line.strip().split()
                compList = self.__extractCompositions(line, word2id)
                for w,cs in zip(compList[0], compList[1]):
                    self.compositWordList[w] |= set(cs)
                line = f.readline()
                
                lineCount += 1
                print('\r%d'%lineCount, end='')
            print('')

        id2word = {i:w for w,i in word2id.items()}
        self.compositWeightList = []
        for i,cs in enumerate(self.compositWordList):
            # set to list
            cs = list(cs)
            
            if len(cs)==0:
                # if there is no composit element, use the target word itself for replacement
                cs = [i]
            
            self.compositWordList[i] = cs
            
            size = self.id2len[i]
            weis = [self.poissonTable[size-1][self.id2len[c]-1] 
                    if self.usePoisson else 1 for c in cs]
            sumw = sum(weis)
            weis = [w/sumw for w in weis]            
            self.compositWeightList.append(weis)
         
        print('DONE')
        
    def __buildSamplingTable(self, k=1000):
        print('BUILD SAMPLING TABLE...')
        self.samplingTable = [random.choices(self.compositWordList[i], 
                                             k=k, 
                                             weights=self.compositWeightList[i])
                              for i in range(len(self.id2len))] 
        print('DONE')

    def __extractCompositions(self, line, word2id):

        if self.wordPieceMode:
             line = [w.replace(self.wordPieceSplitSymbol, '')
                     if w.startswith(self.wordPieceSplitSymbol)
                     else self.splitSymbol+w for w in line]
        
        compositions = [[word2id[w] if w in word2id else word2id[self.unkToken] for w in line],
                        [[] for _ in range(len(line))],
                        [[] for _ in range(len(line))]]

        endPoints = np.cumsum([len(w) for w in line])

        raw = ''.join(line)
        
        p = 0 # word position
        for i in range(len(raw)):
            # shift point
            if endPoints[p]<=i:
                p += 1       
            for j in range(min(len(raw)-i, self.maxLength)):
                sw = raw[i:i+j+1]
                
                if sw!=line[p] and sw in word2id:
                    pcs = []
                    for pa,pb in enumerate(endPoints[p:]):
                        pcs.append(p+pa)
                        if i+j+1<=pb:
                            break
                    for pc in pcs:
                        swid = word2id[sw]
                        if swid not in compositions[1][pc]:
                            compositions[1][pc].append(swid)
                            compositions[2][pc].append(1/len(pcs))

        return compositions

    # for ids
    def perturb(self, idss, rate, ignoreIdx=None):
        # idss is a batch of ids like [[1,2,3], [3,4,5,6]]
        
        if rate==0.0:
            return idss

        idss = [[self.sampleWord(i)
               if i!=ignoreIdx and random.random()<rate else i
               for i in ids] for ids in idss]

        return idss

    def sampleWord(self, wordid):
        return self.samplingTable[wordid][random.randint(0,self.samplingCacheSize-1)]

if __name__=='__main__':
    word2id = {'a':0, 'b':1, 'c':2, 'ab':3, 'bc':4, 'abc':5, '<unk>':6} 
    segData = [['ab','c'], ['a','b','c'], ['a', 'bc'], ['abc']]
    wp = CompositWordReplacer(word2id, segData, usePoisson=True,
                         wordPieceMode=False, wordPieceSplitSymbol='##', unkToken='<unk>')
    id2word = {i:w for w,i in word2id.items()}

    print('---COMPOSIT WORD LIST---')
    print('TARGET WORD / [LIST OF REPLACEMENT CANDIDATES]')
    for i, cs in enumerate(wp.compositWordList):
        w = id2word[i]
        wcs = [(id2word[c], wp.compositWeightList[i][j]) for j, c in enumerate(cs)]
        print(w, wcs)
    
    # you can get perturbed sequence as the following:
    print('---PERTURBATION EXAMPLE---')
    inp = [5, 0, 4]
    print('ORIGINAL:', inp, '=', [id2word[i] for i in inp])
    for i in range(3):
        pt = wp.perturb([inp], 0.5)[0]
        print('SAMPLE %d:'%i, pt, '=', [id2word[j] for j in pt])
