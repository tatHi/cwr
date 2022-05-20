# Compositional Word Replacement
Official implementation of [Word-level Perturbation Considering Word Length and Compositional Subwords](https://aclanthology.org/2022.findings-acl.258.pdf) (Findings of ACL2022).

This repository includes modules for the perturbation:
- `wordReplacer.py`
    - Word replacement
    - Word replacement with a restriction considering subword length
- `compositWordReplacer.py`
    - Compositional word replacement
    - Compositional word replacement with a restriction considering subword length

`example.py` overviews the usage of each perturbation module.
You can see the outputs of each perturbation just run this code as the following (the results depends on random seeds):

```
$ python example.py
Vocabulary:
>>> {'thing': 0, '▁book': 1, '▁ti': 2, '▁read': 3, '▁do': 4, 'er': 5, '▁beg': 6, '▁sist': 7, 'y': 8, 't': 9, '▁hav': 10, '▁it': 11, '▁to': 12, '▁she': 13, '▁no': 14, '▁sit': 15, 'r': 16, '▁picture': 17, 'ed': 18, '▁her': 19, '▁or': 20, '▁bank': 21, '▁twice': 22, 'tions': 23, '▁was': 24, '▁wa': 25, 'in': 26, 'e': 27, '▁get': 28, '▁sis': 29, '▁ver': 30, '▁into': 31, 's': 32, '▁peep': 33, '▁of': 34, '▁the': 35, 'd': 36, '▁:': 37, '▁he': 38, '▁ha': 39, '▁ali': 40, '▁th': 41, '▁but': 42, 'ing': 43, 'ter': 44, '▁conver': 45, '▁in': 46, '▁had': 47, 'a': 48, '▁by': 49, '▁and': 50, 'ce': 51, 'n': 52, '▁on': 53}
Input Text:
>>> ['▁hav', 'ing', '▁no', 'thing', '▁to', '▁do']
Input Ids:
>>> [10, 43, 14, 0, 12, 4]
### Original Word Replacement (p=0.5)###
Trial-1:
	TEXT >>> ['▁hav', '▁book', '▁no', 'thing', '▁to', '▁do']
	IDS  >>> [10, 1, 14, 0, 12, 4]
Trial-2:
	TEXT >>> ['▁hav', '▁th', '▁her', 'thing', '▁into', '▁and']
	IDS  >>> [10, 41, 19, 0, 31, 50]
Trial-3:
	TEXT >>> ['▁he', '▁but', '▁no', 'er', '▁to', '▁sis']
	IDS  >>> [38, 42, 14, 5, 12, 29]
Trial-4:
	TEXT >>> ['▁hav', 'ing', '▁to', 'thing', '▁to', '▁do']
	IDS  >>> [10, 43, 12, 0, 12, 4]
Trial-5:
	TEXT >>> ['n', 'ing', '▁no', 'thing', '▁sis', '▁do']
	IDS  >>> [52, 43, 14, 0, 29, 4]
### Word Replacement + Poisson (p=0.5)###
>>> BUILD SAMPLING TABLE
>>> BUILD CAHCE TABLE
Trial-1:
	TEXT >>> ['▁hav', 'ce', '▁no', 'thing', '▁to', '▁do']
	IDS  >>> [10, 51, 14, 0, 12, 4]
Trial-2:
	TEXT >>> ['▁hav', 'ce', '▁no', '▁the', '▁bank', '▁do']
	IDS  >>> [10, 51, 14, 35, 21, 4]
Trial-3:
	TEXT >>> ['ed', '▁sit', 'a', '▁and', 'er', '▁do']
	IDS  >>> [18, 15, 48, 50, 5, 4]
Trial-4:
	TEXT >>> ['▁she', '▁her', '▁no', 'thing', '▁to', '▁do']
	IDS  >>> [13, 19, 14, 0, 12, 4]
Trial-5:
	TEXT >>> ['▁hav', 'e', '▁no', 'thing', '▁by', '▁do']
	IDS  >>> [10, 27, 14, 0, 49, 4]
### Compositional Word Replacement (p=0.5)###
BUILD...
DONE
BUILD SAMPLING TABLE...
DONE
Trial-1:
	TEXT >>> ['▁hav', 'ing', 'n', 'thing', 't', '▁do']
	IDS  >>> [10, 43, 52, 0, 9, 4]
Trial-2:
	TEXT >>> ['▁ha', 'in', '▁no', 'thing', 't', 'd']
	IDS  >>> [39, 26, 14, 0, 9, 36]
Trial-3:
	TEXT >>> ['▁ha', 'n', '▁no', 'thing', 't', '▁do']
	IDS  >>> [39, 52, 14, 0, 9, 4]
Trial-4:
	TEXT >>> ['a', 'in', '▁no', 'n', '▁to', '▁do']
	IDS  >>> [48, 26, 14, 52, 12, 4]
Trial-5:
	TEXT >>> ['▁hav', 'ing', '▁no', 'thing', 't', 'd']
	IDS  >>> [10, 43, 14, 0, 9, 36]
### Compositional Word Replacement + Poisson (p=0.5)###
BUILD...
DONE
BUILD SAMPLING TABLE...
DONE
Trial-1:
	TEXT >>> ['▁ha', 'in', '▁no', 'thing', 't', 'd']
	IDS  >>> [39, 26, 14, 0, 9, 36]
Trial-2:
	TEXT >>> ['▁ha', 'in', 'n', 'ing', '▁to', '▁do']
	IDS  >>> [39, 26, 52, 43, 12, 4]
Trial-3:
	TEXT >>> ['▁hav', 'n', 'n', 'n', 't', 'd']
	IDS  >>> [10, 52, 52, 52, 9, 36]
Trial-4:
	TEXT >>> ['▁hav', 'in', '▁no', 'thing', '▁to', '▁do']
	IDS  >>> [10, 26, 14, 0, 12, 4]
Trial-5:
	TEXT >>> ['▁ha', 'ing', 'n', 'in', 't', 'd']
	IDS  >>> [39, 43, 52, 26, 9, 36]
```
