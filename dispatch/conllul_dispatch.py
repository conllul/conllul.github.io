#!/usr/bin/python3
"""Dispatch a conll-ul morphological analyzer"""

import argparse
from collections import defaultdict
import os
import sys

import analyzers
from util import *


ANALYZERS = defaultdict(dict)
# add udlex to all relevant languages
for l in YAPUDLEX.langs():
    ANALYZERS[l]['udlex'] = YAPUDLEX

# add registered morphological analyzers
for l, ma_dict in LANG_MA.items():
    ANALYZERS[l].update(ma_dict)


def analyze(analyzer, in_file, out_file, cite=True):
    """Run an analyzer on a given input and output file"""
    print("Using %s MA for analysis" % analyzer.name())
    # if cite and analyzer.citations():
    #     print(analyzer.description())
    #     print("Please consider the following citation(s) when using the generated output for research")
    #     print(analyzer.citations())
    analyzer.run(in_file, out_file)


def list_providers_languages():
    """Returns an array for output with the various MA providers and associated
    languages"""
    retval = list()
    LANG_WITH_NAME = sorted(["%s (%s)" % (CODE_TO_LANG[l].replace('_', ' ').capitalize(), l) for l in LANGUAGES])
    retval.append("Languages supported by the data-driven baseline MA (-p baseline):\n%s" % ", ".join(LANG_WITH_NAME))
    udlexs = sorted(map(lambda item: "%s (%s) - %s" % (CODE_TO_LANG[item[0]].capitalize(), item[0], "/".join(item[1])),
                        YAPUDLEX.lexicons().items()))
    retval.append("Languages with a UD lexicon (-p udlex -o lexicon=<name>):\n%s" % ", ".join(udlexs))
    retval.append("Morphological Analyzers by UD language code (-p <name>):")
    for lang, providers in sorted(LANG_MA.items()):
        retval.append("%s - %s" % (lang, ", ".join(providers.keys())))
    return "\n".join(retval)


def get_analyzer(providers, arg_provider, lang):
    """Finds the class of a morphological analyzer"""
    if len(lang_providers) == 1 and not arg_provider:
        return list(lang_providers.items())[0]
    elif len(lang_providers) > 1 and arg_provider:
        analyzer_cls = lang_providers.get(arg_provider, None)
        if analyzer_cls:
            return arg_provider, analyzer_cls
        else:
            print("Unknown provider %s for language %s, options are %s"  % (arg_provider, lang, ", ".join(['baseline'] + list(lang_providers.keys()))))
            sys.exit(1)
    else:
        print("Please specify an analysis provider (-p <provider>), options are %s" % ", ".join(['baseline'] + list(lang_providers.keys())))
        sys.exit(1)


def get_lexicon(lang, user_lexicon):
    """Gets a UD lexicon from a languages available lexicons, or the only
    possible lexicon if there's only one"""
    lang_lexicons = YAPUDLEX.lexicons()[lang]
    if user_lexicon and user_lexicon not in lang_lexicons:
        print("Unknown lexicon for languages %s, options are: %s" % (lang, "/".join(lang_lexicons)))
        sys.exit(1)
    if len(lang_lexicons) > 1 and not user_lexicon:
        print("Please specify a lexicon (-o lexicon=<name>), options are: %s" % "/".join(lang_lexicons))
        sys.exit(1)
    if len(lang_lexicons) == 1 and not user_lexicon:
        return lang_lexicons[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dispatcher for CoNLL-UL morphological analysis",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=list_providers_languages())
    parser.add_argument("--nocite", action="store_false", help="Skip citation output")
    parser.add_argument("-p", "--provider", help="Use a given MA provider. If a language has a non-baseline provider, that provider will be the default. If multiple providers exist one must be chosen.")
    parser.add_argument("-o", "--options", help="Optional values to pass on to the providers, as a comma-separated list of <key>=<value> pairs")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress analyzers' output")
    parser.add_argument("lang", help="Language name or code (i.e. en or English)")
    parser.add_argument("input", help="Input File")
    parser.add_argument("output", help="Output File")
    args = parser.parse_args()

    analyzer_cls = None
    if args.lang.lower() in LANG_NAMES:
        args.lang = LANG_TO_CODE[args.lang.lower()]

    if args.lang in LANGUAGES:
        lang_providers = ANALYZERS.get(args.lang)
    else:
        print("The following languages are supported:\n%s" % ", ".join(LANGUAGES))

    provider = analyzer_cls = None
    if args.provider != 'baseline':
        provider, analyzer_cls = get_analyzer(lang_providers, args.provider, args.lang)
    options = defaultdict(None)
    options['quiet'] = args.quiet
    if args.options:
        option_list = options.split(',')
        user_options = {v.split('=') for v in option_list}
        options.update(user_options)
    if provider == 'udlex':
        options['lexicon'] = get_lexicon(args.lang, options.get('lexicon', None))
    if analyzer_cls:
        analyzer = analyzer_cls(args.lang, **options)
    else:
        analyzer = YAPDD(args.lang, **options)
    analyze(analyzer, args.input, args.output, cite=args.nocite)
