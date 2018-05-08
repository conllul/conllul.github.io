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

## CoNLL-UL Morphological Analyses
We provide morphological analyses with the above analyzers and lexicons for the UD 2.2 treebanks participating in the [CoNLL 2018 Shared Task](http://universaldependencies.org/conll18/data.html).

Arabic, Hebrew, and Turkish treebanks were analyzed with their respective morphological analyzers, and treebanks with associated UD lexicons were analyzed with yap. In addition, all treebanks have baseline analyses generated by a data-driven lexicon induced from the train set.

For the convenience of the community and shared task participants, we provide the set of train and dev conllul files treebanks in a single archive for download [here](https://storage.googleapis.com/conllul/ud22st2018conllul.tar.gz) (note 800MB/~7.3GB w/o compression). Test set files are deliberately missing in the archive, and will be added after the full release of UD 2.2 (July 1, 2018). The test files should not be used in the shared task test environment as they would reveal gold sentence segmentation and tokenization.

The text of all analyses are bound to the licenses of their respective UD treebanks, lexicons and morphological analyzers where appropriate. We also request that you cite resources accordingly.

| UD Language         | Morphologically Analyzed Treebanks                                                                                          |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Afrikaans           | [AfriBooms](https://github.com/conllul/UL_Afrikaans-AfriBooms)                                                              |
| Ancient_Greek       | [Perseus](https://github.com/conllul/UL_Ancient_Greek-Perseus), [PROIEL](https://github.com/conllul/UL_Ancient_Greek-PROIEL)|
| Arabic              | [PADT](https://github.com/conllul/UL_Arabic-PADT)                                                                           |
| Armenian            | [ArmTDP](https://github.com/conllul/UL_Armenian-ArmTDP)                                                                     |
| Basque              | [BDT](https://github.com/conllul/UL_Basque-BDT)                                                                             |
| Bulgarian           | [BTB](https://github.com/conllul/UL_Bulgarian-BTB)                                                                          |
| Buryat              | [BDT](https://github.com/conllul/UL_Buryat-BDT)                                                                             |
| Catalan             | [AnCora](https://github.com/conllul/UL_Catalan-AnCora)                                                                      |
| Chinese             | [GSD](https://github.com/conllul/UL_Chinese-GSD)                                                                            |
| Croatian            | [SET](https://github.com/conllul/UL_Croatian-SET)                                                                           |
| Czech               | [CAC](https://github.com/conllul/UL_Czech-CAC)[PDT](https://github.com/conllul/UL_Czech-PDT)                                |
| Danish              | [DDT](https://github.com/conllul/UL_Danish-DDT)                                                                             |
| Dutch               | [Alpino](https://github.com/conllul/UL_Dutch-Alpino), [LassySmall](https://github.com/conllul/UL_Dutch-LassySmall)          |
| English             | [EWT](https://github.com/conllul/UL_English-EWT), [LinES](https://github.com/conllul/UL_English-LinES)                      |
| Estonian            | [EDT](https://github.com/conllul/UL_Estonian-EDT)                                                                           |
| Finnish             | [FTB](https://github.com/conllul/UL_Finnish-FTB), [TDT](https://github.com/conllul/UL_Finnish-TDT)                          |
| French              | [GSD](https://github.com/conllul/UL_French-GSD), [Spoken](https://github.com/conllul/UL_French-Spoken)                      |
| Galician            | [CTG](https://github.com/conllul/UL_Galician-CTG), [TreeGal](https://github.com/conllul/UL_Galician-TreeGal)                |
| German              | [GSD](https://github.com/conllul/UL_German-GSD)                                                                             |
| Gothic              | [PROIEL](https://github.com/conllul/UL_Gothic-PROIEL)                                                                       |
| Greek               | [GDT](https://github.com/conllul/UL_Greek-GDT)                                                                              |
| Hebrew              | [HTB](https://github.com/conllul/UL_Hebrew-HTB)                                                                             |
| Hindi               | [HDTB](https://github.com/conllul/UL_Hindi-HDTB)                                                                            |
| Hungarian           | [Szeged](https://github.com/conllul/UL_Hungarian-Szeged)                                                                    |
| Indonesian          | [GSD](https://github.com/conllul/UL_Indonesian-GSD)                                                                         |
| Irish               | [IDT](https://github.com/conllul/UL_Irish-IDT)                                                                              |
| Italian             | [ISDT](https://github.com/conllul/UL_Italian-ISDT), [PoSTWITA](https://github.com/conllul/UL_Italian-PoSTWITA)              |
| Japanese            | [GSD](https://github.com/conllul/UL_Japanese-GSD)                                                                           |
| Kazakh              | [KTB](https://github.com/conllul/UL_Kazakh-KTB)                                                                             |
| Korean              | [GSD](https://github.com/conllul/UL_Korean-GSD), [Kaist](https://github.com/conllul/UL_Korean-Kaist)                        |
| Kurmanji            | [MG](https://github.com/conllul/UL_Kurmanji-MG)                                                                             |
| Latin               | [ITTB](https://github.com/conllul/UL_Latin-ITTB), [PROIEL](https://github.com/conllul/UL_Latin-PROIEL)                      |
| Latvian             | [LVTB](https://github.com/conllul/UL_Latvian-LVTB)                                                                          |
| North_Sami          | [Giella](https://github.com/conllul/UL_North_Sami-Giella)                                                                   |
| Norwegian           | [Bokmaal](https://github.com/conllul/UL_Norwegian-Bokmaal), [NynorskLIA](https://github.com/conllul/UL_Norwegian-NynorskLIA)|
| Old_Church_Slavonic | [PROIEL](https://github.com/conllul/UL_Old_Church_Slavonic-PROIEL)                                                          |
| Old_French          | [SRCMF](https://github.com/conllul/UL_Old_French-SRCMF)                                                                     |
| Persian             | [Seraji](https://github.com/conllul/UL_Persian-Seraji)                                                                      |
| Polish              | [LFG](https://github.com/conllul/UL_Polish-LFG)                                                                             |
| Polish              | [SZ](https://github.com/conllul/UL_Polish-SZ)                                                                               |
| Portuguese          | [Bosque](https://github.com/conllul/UL_Portuguese-Bosque)                                                                   |
| Romanian            | [RRT](https://github.com/conllul/UL_Romanian-RRT)                                                                           |
| Russian             | [SynTagRus](https://github.com/conllul/UL_Russian-SynTagRus), [Taiga](https://github.com/conllul/UL_Russian-Taiga)          |
| Serbian             | [SET](https://github.com/conllul/UL_Serbian-SET)                                                                            |
| Slovak              | [SNK](https://github.com/conllul/UL_Slovak-SNK)                                                                             |
| Slovenian           | [SSJ](https://github.com/conllul/UL_Slovenian-SSJ), [SST](https://github.com/conllul/UL_Slovenian-SST)                      |
| Spanish             | [AnCora](https://github.com/conllul/UL_Spanish-AnCora)                                                                      |
| Swedish             | [LinES](https://github.com/conllul/UL_Swedish-LinES), [Talbanken](https://github.com/conllul/UL_Swedish-Talbanken)          |
| Turkish             | [IMST](https://github.com/conllul/UL_Turkish-IMST)                                                                          |
| Ukrainian           | [IU](https://github.com/conllul/UL_Ukrainian-IU)                                                                            |
| Upper_Sorbian       | [UFAL](https://github.com/conllul/UL_Upper_Sorbian-UFAL)                                                                    |
| Urdu                | [UDTB](https://github.com/conllul/UL_Urdu-UDTB)                                                                             |
| Uyghur              | [UDT](https://github.com/conllul/UL_Uyghur-UDT)                                                                             |
| Vietnamese          | [VTB](https://github.com/conllul/UL_Vietnamese-VTB)                                                                         |

## Citation
```
@inproceedings{more2018,
 author  = {More, Amir and \c{C}etino\u{g}lu, \"{O}zlem and  \c{C}\"{o}ltekin, \c{C}a\u{g}r{\i} and  Habash, Nizar and  Sagot, Benoît and  Seddah, Djamé and  Taji, Dima, and  Tsarfaty, Reut},
 year  = {2018},
 title  = { {CoNLL-UL}: Universal Morphological Lattices for {U}niversal {D}ependency Parsing},
 booktitle  = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC'18})},
}
```

