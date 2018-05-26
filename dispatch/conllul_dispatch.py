#!/usr/bin/python3

import argparse
from collections import defaultdict
import os
import sys

from util import YAPDD, YAPUDLEX


from tr import TRMorph
from he import HEBLEX


analyzers = defaultdict(dict)
analyzers['he']['HEBLEX'] = HEBLEX
analyzers['tr']['TRMorph'] = TRMorph

LANGUAGES = "af,ar,bg,bxr,ca,cs,cu,da,de,el,en,es,et,eu,fa,fi,fr,fro,ga,gl,got,grc,he,hi,hr,hsb,hu,hy,id,it,ja,kk,kmr,ko,la,lv,nl,no,pl,pt,ro,ru,sk,sl,sme,sr,sv,tr,ug,uk,ur,vi,zh".split(',')


def analyze(analyzer, in_file, out_file, cite=True):
    print("Using %s MA for analysis" % analyzer.name())
    # if cite and analyzer.citations():
    #     print(analyzer.description())
    #     print("Please consider the following citation(s) when using the generated output for research")
    #     print(analyzer.citations())
    analyzer.run(in_file, out_file)


def list_providers():
    retval = ["Morphological Analyzers (by UD language code):"]
    for lang, providers in analyzers.items():
        retval.append("%s - %s" % (lang, ", ".join(providers.keys())))
    retval.append("Languages supported by the data-driven baseline MA:\n%s" % ", ".join(LANGUAGES))
    retval.append("Languages with a UD lexicon (use lexicon=<file> with -o to disambiguate if multiple lexicons exist):\n%s" % YAPUDLEX.lexicons())
    return "\n".join(retval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dispatcher for CoNLL-UL-compliant morphological analyzers",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=list_providers())
    parser.add_argument("--nocite", action="store_false", help="Skip citation output")
    parser.add_argument("-p", "--provider", help="Use a given MA provider. If a language has a non-baseline provider, that provider will be the default. If multiple providers exist one must be chosen.")
    parser.add_argument("-o", "--options", help="Optional values to pass on to the providers, as a comma-separated list of <key>=<value> pairs")
    parser.add_argument("lang", help="Language (run with -h to see options)")
    parser.add_argument("input", help="Input File")
    parser.add_argument("output", help="Output File")
    args = parser.parse_args()

    analyzer_cls = None
    if args.lang not in LANGUAGES:
        print("The following languages are supported:\n%s" % ", ".join(LANGUAGES))
    lang_providers = analyzers.get(args.lang)
    if lang_providers:
        if len(lang_providers) == 1:
            analyzer_cls = list(lang_providers.values())[0]
        else:
            print("Please specify an analysis provider (-p), options are %s" % ", ".join(lang_providers.keys()))
            sys.exit(1)
    options = {}
    if args.options:
        option_list = options.split(',')
        user_options = {v.split('=') for v in option_list}
        options.update(user_options)
    if analyzer_cls:
        analyzer = analyzer_cls(**options)
    else:
        analyzer = YAPDD(args.lang, **options)
    analyze(analyzer, args.input, args.output, cite=args.nocite)
