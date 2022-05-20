import wordReplacer as wr
import compositWordReplacer as cwr

# preparation
## sample data
segdata = [
        '▁ali ce ▁wa s ▁beg in n ing ▁to ▁get ▁ver y ▁ti r ed ▁of ▁sit t ing ▁by ▁her ▁sis ter ▁on ▁the ▁bank'.split(),
        '▁and ▁of ▁hav ing ▁no thing ▁to ▁do ▁:'.split(),
        '▁on ce ▁or ▁twice ▁she ▁ha d ▁peep ed ▁into ▁th e ▁book ▁he r ▁sist er ▁was ▁read ing'.split(),
        '▁but ▁it ▁had ▁no ▁picture s ▁or ▁conver s a tions ▁in ▁it'.split()]
vocab = {w for line in segdata for w in line}


## word2id dictionary
word2id = {}
id2word = {}
for w in vocab:
    word2id[w] = len(word2id)
    id2word[word2id[w]] = w

print('Vocabulary:')
print('>>>', word2id)

# perturbation examples
text = '▁hav ing ▁no thing ▁to ▁do'.split() 
ids = [word2id[w] for w in text]
print('Input Text:')
print('>>>', text)
print('Input Ids:')
print('>>>', ids)

## original word replacement
print('### Original Word Replacement (p=0.5)###')
replacer = wr.WordReplacer(word2id, usePoisson=False)
for t in range(5):
    sampledIds = replacer.perturb([ids], rate=0.5)[0]
    print('Trial-%i:'%(t+1))
    print('\tTEXT >>>', [id2word[i] for i in sampledIds])
    print('\tIDS  >>>', sampledIds)

## word replacement + poisson (WR+L)
print('### Word Replacement + Poisson (p=0.5)###')
replacer = wr.WordReplacer(word2id, usePoisson=True)
for t in range(5):
    sampledIds = replacer.perturb([ids], rate=0.5)[0]
    print('Trial-%i:'%(t+1))
    print('\tTEXT >>>', [id2word[i] for i in sampledIds])
    print('\tIDS  >>>', sampledIds)

## compositional word replacement (CWR)
print('### Compositional Word Replacement (p=0.5)###')
replacer = cwr.CompositWordReplacer(word2id, segdata, usePoisson=False)
for t in range(5):
    sampledIds = replacer.perturb([ids], rate=0.5)[0]
    print('Trial-%i:'%(t+1))
    print('\tTEXT >>>', [id2word[i] for i in sampledIds])
    print('\tIDS  >>>', sampledIds)

## compotisional word replacement + poisson (CWR+L)
print('### Compositional Word Replacement + Poisson (p=0.5)###')
replacer = cwr.CompositWordReplacer(word2id, segdata, usePoisson=False)
for t in range(5):
    sampledIds = replacer.perturb([ids], rate=0.5)[0]
    print('Trial-%i:'%(t+1))
    print('\tTEXT >>>', [id2word[i] for i in sampledIds])
    print('\tIDS  >>>', sampledIds)


