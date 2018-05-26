import subprocess

from util import MA


class HEBLEX(MA):
    CITATIONS = ["Itai, A. and Wintner, S. (2008).\n" +
    "\tLanguage resources for Hebrew. Language Resources and Evaluation, 42(1):75–98, March",
    "More, A. and Tsarfaty, R. (2016). Data-driven morphological analysis and disambiguation for morphologically rich languages and universal dependencies.\n" +
    "\tIn Proceedings of COLING 2016, the 26th International Conference on Computational Linguistics: Technical Papers, pages 337–348, Osaka, Japan, December. The COLING 2016 Organizing Committee."]


    def name(self):
        return "yap"


    def description(self):
        print("HEBLEX Morphological Analyzer based on the BGU Lexicon")


    def execute(self, input_file, output_file):
        result = subprocess.call(['/home/gopath/src/yap/yap', 'hebma', '-raw', input_file, '-format', 'ud', '-out', output_file])
        if result != 0:
            raise Exception("yap failed")
