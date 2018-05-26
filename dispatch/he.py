import subprocess

from util import YAPDD, register


@register("he", "heblex")
class HEBLEX(YAPDD):
    CITATIONS = ["Itai, A. and Wintner, S. (2008).\n" +
    "\tLanguage resources for Hebrew. Language Resources and Evaluation, 42(1):75–98, March",
    "More, A. and Tsarfaty, R. (2016). Data-driven morphological analysis and disambiguation for morphologically rich languages and universal dependencies.\n" +
    "\tIn Proceedings of COLING 2016, the 26th International Conference on Computational Linguistics: Technical Papers, pages 337–348, Osaka, Japan, December. The COLING 2016 Organizing Committee."]


    def __init__(self, *args, **kwargs):
        super().__init__('he', **kwargs)


    @classmethod
    def name(cls):
        return "heblex"


    def description(self):
        print("HEBLEX Morphological Analyzer based on the BGU Lexicon")


    def execute(self, input_file, output_file):
        subprocess_kwargs = {}
        if self.options['quiet']:
            devnull = open(os.devnull, 'w')
            subprocess_kwargs['stdout'] = devnull
            subprocess_kwargs['stderr'] = devnull
        command = [self.yap, 'hebma', '-raw', input_file, '-format', 'ud', '-out', output_file]
        if not self.options['quiet']:
            print("Calling %s" % " ".join(command))
        result = subprocess.call(command, **subprocess_kwargs)
        if result != 0:
            raise Exception("yap failed")
