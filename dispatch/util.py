from collections import defaultdict
import csv
import os
import re
import subprocess

class MA:
    CITATIONS = None
    def __init__(self, **kwargs):
        self.options = defaultdict(None)
        self.options.update(kwargs)


    def parameters(self):
        return {}


    @classmethod
    def name(cls):
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
    def __init__(self, lang, **kwargs):
        super().__init__(**kwargs)
        self.lang = lang
        self.base_dir = kwargs.get('dir', os.environ.get('YAP', os.getcwd()))
        self.yap = os.path.join(self.base_dir, 'yap')


    @classmethod
    def name(cls):
        return "baseline"


    def description(self):
        print("Baseline CoNLL-UL data-driven morphological analyzer (lexicon extracted from UD train-set files)")


    def execute(self, input_file, output_file):
        subprocess_kwargs = {}
        if self.options['quiet']:
            devnull = open(os.devnull, 'w')
            subprocess_kwargs['stdout'] = devnull
            subprocess_kwargs['stderr'] = devnull
        command = [self.yap, 'ma', '-dict', "%s.json" % self.lang, '-raw', input_file, '-format', 'ud', '-out', output_file]
        result = subprocess.call(command, **subprocess_kwargs)
        if result != 0:
            raise Exception("yap failed")


class YAPUDLEX(MA):
    CITATIONS = [u'Amir More, Özlem Çetinoğlu, Çağrı Çöltekin, Nizar Habash, Benoît Sagot, Djamé Seddah, Dima, Taji '+
                 u'and Reut Tsarfaty (2018) CoNLL-UL: Universal Morphological Lattices for Universal Dependency Parsing\n' +
                 u'\tIn: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC’18)']
    options = {}
    def __init__(self, lang, lexicon=None, **kwargs):
        super().__init__(**kwargs)
        self.lang = lang
        self.udlex = "UDLex_%s-%s.conllul" % (CODE_TO_LANG[lang].capitalize(), lexicon)
        self.base_dir = kwargs.get('dir', os.environ.get('YAP', os.getcwd()))
        self.yap = os.path.join(self.base_dir, 'yap')

    @classmethod
    def name(cls):
        return "udlex"


    def description(self):
        print("YAP morphological analyzer backed by a CoNLL-UL-compliant UD Lexicon")


    def execute(self, input_file, output_file):
        subprocess_kwargs = {}
        if self.options['quiet']:
            devnull = open(os.devnull, 'w')
            subprocess_kwargs['stdout'] = devnull
            subprocess_kwargs['stderr'] = devnull
        LEX_DIR = os.environ.get('LEX_DIR', os.getcwd())
        DICT_FILE = os.path.join(LEX_DIR, "%s.json" % self.lang)
        LEX_FILE = os.path.join(LEX_DIR, self.udlex)
        command = [self.yap, 'ma', '-dict', DICT_FILE, '-udlex', LEX_FILE, '-raw', input_file, '-format', 'ud', '-out', output_file]
        result = subprocess.call(command, **subprocess_kwargs)
        if result != 0:
            raise Exception("yap failed")


    @classmethod
    def data_files(cls):
        LEX_DIR = os.environ.get('LEX_DIR', os.getcwd())
        data_files = os.listdir(LEX_DIR)
        name_regex = re.compile("^UDLex_([A-Z][a-z]*)-(.*).conllul$")
        for f in data_files:
            m = name_regex.match(f)
            if m:
                yield f

    @classmethod
    def langs(cls):
        lang_set = set()
        langs = list()
        name_regex = re.compile("^UDLex_([A-Z][a-z]*)-(.*).conllul$")
        for f in YAPUDLEX.data_files():
            m = name_regex.match(f)
            lang = m.group(1)
            if lang not in lang_set:
                lang_set.add(lang)
                langs.append(LANG_TO_CODE[lang.lower()])
        return langs

    @classmethod
    def lexicons(cls):
        lex_files = defaultdict(list)
        name_regex = re.compile("^UDLex_([A-Z][a-z]*)-(.*).conllul$")
        for f in YAPUDLEX.data_files():
            m = name_regex.match(f)
            lex_files[LANG_TO_CODE[m.group(1).lower()]].append(m.group(2))
        return lex_files


HOME = os.environ.get('DISPATCH', os.getcwd())
LANGUAGE_CODE_MAP_FILENAME = 'lang_name_code.csv'
LANGUAGE_CODE_MAP_FILE = os.path.join(HOME, LANGUAGE_CODE_MAP_FILENAME)
with open(LANGUAGE_CODE_MAP_FILE, 'r') as LANG_FILE:
    LANG_TO_CODE = dict(list(csv.reader(LANG_FILE)))
CODE_TO_LANG = dict(map(reversed, LANG_TO_CODE.items()))

LANGUAGES = "af,ar,bg,bxr,ca,cs,cu,da,de,el,en,es,et,eu,fa,fi,fr,fro,ga,gl,got,grc,he,hi,hr,hsb,hu,hy,id,it,ja,kk,kmr,ko,la,lv,nl,no,pl,pt,ro,ru,sk,sl,sme,sr,sv,tr,ug,uk,ur,vi,zh".split(',')
LANG_NAMES = list(map(CODE_TO_LANG.get, LANGUAGES))

LANG_MA = defaultdict(dict)

def register(lcode, name):
    def decorator(cls):
        LANG_MA[lcode][name] = cls
        return cls
    return decorator
