#!/usr/bin/python

import bz2
import sys
from collections import defaultdict


def get_projected(spellout, func):
    return tuple([tuple(func(segment)) for segment in spellout])


def get_all_paths(graph, start=0, path=None):
    if path:
        path.append(start)
    else:
        path = [start]
    if start not in graph:
        return []
    paths = list()
    for node in graph[start]:
        if node not in path:
            new_paths = get_all_paths(graph, node, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


def get_spellouts(lattice, func):
    spellouts = get_all_paths(lattice[1])
    return spellouts


def get_spellout_set(lattice, func):
    all_spellouts = get_spellouts(lattice)
    return set([get_projected(s, func) for s in all_spellouts])


def calc_lattice_coverage(spellout, lattice, extraction_func):
    lattice_spellouts = get_spellout_set(lattice, extraction_func)
    projected_spellout = get_projected(spellout, extraction_func)
    return 1 if projected_spellout in lattice_spellouts else 0


def conllul_as_lattices(raw_sent):
    lattices = []
    cur_lattice = defaultdict(list)
    cur_lattice_token = ""
    for line in raw_sent:
        if '-' in line[0]:
            if cur_lattice:
                lattices.append((cur_lattice_token[2], cur_lattice))
            cur_lattice = defaultdict(list)
            cur_lattice_token = line
            continue
        cur_lattice[line[0]].append(line)
    return lattices


def conllu_as_spellouts(raw_sent):
    spellouts = []
    cur_spellout = list()
    remaining_segments = 0
    for line in raw_sents:
        if '-' in line[0]:
            if remaining_segments:
                print 'Error: found new multi-seg token with remaining segments from previous'
                sys.exit(0)
            segments = line[0].split('-')
            remaining_segments = int(segments[1]) - int(segments[0])
            cur_spellout = list()
            continue
        if remaining_segments:
            cur_spellouts.append(line)
            remaining_segments -= 1
            continue
        spellouts.append([line])
    return spellouts


def isoov(lattice):
    return 'oov' in lattice[0][2]


def calc_coverage(spellout_reader, lattice_reader):
    spellout_file = depread(spellout_reader)
    lattice_file = depread(lattice_reader)
    total = 0
    oovs = 0
    successes = [0, 0, 0]
    oovsuccesses = [0, 0, 0]
    for spellout_sent, lattice_sent in zip(spellout_file, lattice_file):
        for spellout, lattice in zip(conllu_as_spellouts(spellout_sent),
                                     conllul_as_lattices(lattice_sent)):
            total += 1
            oov = isoov(lattice)
            oovs += if oov else 0
            for i, ex in enumerate(extractors):
                result = calc_lattice_coverage(spellout, lattice, get_seg)
                successes[i] += result
                if oov:
                    oovsuccesses[i] += result
    return successes, total, oovsuccesses, oovs


def main():
    conllu = sys.argv[1]
    conllul = sys.argv[2]
    extractor_name = sys.argv[3]
    extractor = EXTRACTOR_LOOKUP[extractor_name]
    print calc_coverage(bz2.BZ2File(conllu), bz2.BZ2File(conllul))


if __name__ == "__main__":
    main()
