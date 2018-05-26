import os
import subprocess

class MA:
    CITATIONS = None
    def __init__(self, **kwargs):
        self.options = kwargs


    def parameters(self):
        return {}


    def name(self):
        raise Exception("Not implemented")


    def execute(self, in_file, output_file):
        raise Exception("Not implemented")


    def run(self, input_file, output_file):
        self.execute(input_file, output_file)


    def metadata(self):
        raise Exception("Not implemented")


    def citations(self):
        if self.CITATIONS:
            return "\n".join(self.CITATIONS)
        return None


class YAPDD(MA):
    CITATIONS = [u'Amir More, Özlem Çetinoğlu, Çağrı Çöltekin, Nizar Habash, Benoît Sagot, Djamé Seddah, Dima, Taji '+
                 u'and Reut Tsarfaty (2018) CoNLL-UL: Universal Morphological Lattices for Universal Dependency Parsing\n' +
                 u'\tIn: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC’18)']
    options = {}
    def __init__(self, lang, **kwargs):
        super(YAPDD).__init__(**kwargs)
        self.lang = lang


    def name(self):
        return "baseline"


    def description(self):
        print("Baseline CoNLL-UL data-driven morphological analyzer (lexicon extracted from UD train-set files)")


    def execute(self, input_file, output_file):
        result = subprocess.call(['/home/gopath/src/yap/yap', 'ma', '-dict', "%s.json" % self.lang, '-raw', input_file, '-format', 'ud', '-out', output_file])
        if result != 0:
            raise Exception("yap failed")


class YAPUDLEX(MA):
    CITATIONS = [u'Amir More, Özlem Çetinoğlu, Çağrı Çöltekin, Nizar Habash, Benoît Sagot, Djamé Seddah, Dima, Taji '+
                 u'and Reut Tsarfaty (2018) CoNLL-UL: Universal Morphological Lattices for Universal Dependency Parsing\n' +
                 u'\tIn: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC’18)']
    options = {}
    def __init__(self, lang, lexicon, **kwargs):
        super(YAPUDLEX).__init__(**kwargs)
        self.lang = lang
        self.udlex = lexicon


    def name(self):
        return "udlex"


    def description(self):
        print("YAP morphological analyzer backed by a CoNLL-UL-compliant UD Lexicon")


    def execute(self, input_file, output_file):
        result = subprocess.call(['/home/gopath/src/yap/yap', 'ma', '-dict', "%s.json" % self.lang, '-udlex', self.udlex, '-raw', input_file, '-format', 'ud', '-out', output_file])
        if result != 0:
            raise Exception("yap failed")


    @classmethod
    def lexicons():
        # TODO: parse lexfile names
        lexfiles = os.listdir('udlexicons')
        return lexfiles
