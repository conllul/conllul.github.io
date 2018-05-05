# CoNLL-UL: Universal Morphological Lattices for Universal Dependency Parsing

This directory is a place for the lexicon and resources produced by the CoNLL-UL initiative and presented in the LREC 2018 paper:

Amir More, Özlem Çetinoğlu, Çağrı Çöltekin, Nizar Habash, Benoît Sagot,
Djamé Seddah, Dima, Taji and Reut Tsarfaty (2018)
[CoNLL-UL: Universal Morphological Lattices for Universal Dependency Parsing.](http://coltekin.net/cagri/papers/more2018.pdf)
In: Proceedings of the Eleventh International Conference
on Language Resources and Evaluation (LREC'18) 

## Abstract
Following the development of the [universal dependencies (UD) framework](http://universaldependencies.org) and the [CoNLL 2017 Shared Task](http://universaldependencies.org/conll17/) on end-to-end UD
parsing, we address the need for a universal representation of morphological analysis which on the one hand can capture a range
of different alternative morphological analyses of surface tokens, and on the other hand is compatible with the segmentation and
morphological annotation guidelines prescribed for UD treebanks. We propose the CoNLL universal lattices (CoNLL-UL) format, a
new annotation format for word lattices that represent morphological analyses, and provide resources that obey this format for a range
of typologically different languages. The resources we provide are harmonized with the two-level representation and morphological
annotation in their respective UD v2 treebanks, thus enabling research on universal models for morphological and syntactic parsing,
in both pipeline and joint settings, and presenting new opportunities in the development of UD resources for low-resource languages.

## Morphological Analyzers
* Arabic [Calima-star](https://camel.abudhabi.nyu.edu/calima-star/)
* Hebrew [yap](https://github.com/habeanf/yap)
* Turkish [TRMorph2](https://github.com/coltekin/TRmorph/tree/trmorph2)

## Lexicons
[INRIA UD Lexicons adapted from Alexina, Apertium, and Giellatekno](http://alpage.inria.fr/~sagot/udlexicons.html)

## Citation
```
@inproceedings{more2018,
 author  = {More, Amir and \c{C}etino\u{g}lu, \"{O}zlem and  \c{C}\"{o}ltekin, \c{C}a\u{g}r{\i} and  Habash, Nizar and  Sagot, Benoît and  Seddah, Djamé and  Taji, Dima, and  Tsarfaty, Reut},
 year  = {2018},
 title  = { {CoNLL-UL}: Universal Morphological Lattices for {U}niversal {D}ependency Parsing},
 booktitle  = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC'18})},
}
```

