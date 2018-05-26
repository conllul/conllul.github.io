import os
import sys

from util import MA


class TRMorph(MA):
    CITATIONS = u'Çağrı Çöltekin (2010). A Freely Available Morphological Analyzer for Turkish In Proceedings of the 7th International Conference on Language Resources and Evaluation (LREC2010)'

    def __init__(self, **kwargs):
        super(TRMorph).__init__(**kwargs)
        sys.path.append(os.getcwd() + '/TRmorph/tools')


    def name(self):
        return "TRMorph2"


    def description(self):
        return "TRMorph 2.0, an open source finite-state morphological analyzer for Turkish"



    def write_analysis(self, out_target, analysis):
        for lattice in analysis:
            if lattice.end - lattice.begin == 1:
                out_target.write("%d-%d\t%s\t%s\n" % (lattice.begin, lattice.end, lattice.form, lattice.misc))
            out_target.write(str(lattice))
        out_target.write("\n")

    def analyze(self, out_target, data):
        from trmorph import Trmorph
        trm = Trmorph()
        analysis = list()
        for val in data:
            if not val:
                self.write_analysis(out_target, analysis)
                continue
            begin = analysis[-1].end if analysis else 0
            analysis.append(trm.to_conll_ul(val, begin=begin))
        if analysis:
            self.write_analysis(out_target, analysis)


    def execute(self, input_file, output_file):
        try:
            f = open(input_file) 
            data = [line.strip() for line in f.readlines()]
        finally:
            f.close()
        try:
            out_file = open(output_file, 'w')
            self.analyze(out_file, data)
        finally:
            out_file.close()
