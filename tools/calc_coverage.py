#!/usr/bin/python

import bz2
import sys
from collections import defaultdict
from depio import depread
from pprint import pprint


def get_projected(spellout, func):
    return tuple([tuple(func(segment)) for segment in spellout])


def get_all_paths(graph, node="0", path=None):
    if not path:
        path = list()
    out_edges = graph.get(node)
    if not out_edges:
        return [path]
    paths = list()
    for edge in out_edges:
        add_this_to_path = path + [edge]
        new_paths = get_all_paths(graph, edge[1], add_this_to_path)
        for new_path in new_paths:
            paths.append(new_path)
    return paths


def get_spellouts(lattice):
    lattice_range = lattice[2]
    start, end = lattice_range.split('-')
    spellouts = get_all_paths(lattice[1], start)
    return spellouts


def get_spellout_set(lattice, func):
    all_spellouts = get_spellouts(lattice)
    retval = set([get_projected([seg[1:] for seg in s], func) for s in all_spellouts])
    return retval


def calc_lattice_coverage(spellout, lattice, extraction_func):
    lattice_spellouts = get_spellout_set(lattice, extraction_func)
    projected_spellout = get_projected(spellout, extraction_func)
    result = 1 if projected_spellout in lattice_spellouts else 0
    return result


def conllul_as_lattices(raw_sent):
    lattices = []
    cur_lattice = defaultdict(list)
    cur_lattice_token = ""
    for line in raw_sent:
        if '-' in line[0]:
            if cur_lattice:
                lattices.append((cur_lattice_token[2], cur_lattice, cur_lattice_token[0]))
            cur_lattice = defaultdict(list)
            cur_lattice_token = line
            continue
        cur_lattice[line[0]].append(line)
    if cur_lattice:
        lattices.append((cur_lattice_token[2], cur_lattice, cur_lattice_token[0]))
    return lattices


def conllu_as_spellouts(raw_sent):
    spellouts = []
    cur_spellout = list()
    remaining_segments = 0
    for line in raw_sent:
        if '-' in line[0]:
            if remaining_segments:
                print 'Error: found new multi-seg token with remaining segments from previous'
                sys.exit(0)
            if cur_spellout:
                spellouts.append(cur_spellout)
            segments = line[0].split('-')
            remaining_segments = int(segments[1]) - int(segments[0]) + 1
            cur_spellout = list()
            continue
        if remaining_segments:
            cur_spellout.append(line)
            remaining_segments -= 1
            continue
        spellouts.append([line])
    if cur_spellout:
        spellouts.append(cur_spellout)
    return spellouts


def isoov(lattice):
    return 'oov' in lattice[0]


extractors = [lambda v:[v[1]], lambda v:[v[1], v[3]], lambda v:[v[1], v[3], v[5]]]
def calc_coverage(spellout_reader, lattice_reader):
    spellout_file = depread(spellout_reader)
    lattice_file = depread(lattice_reader)
    total = 0
    oovs = 0
    successes = [0, 0, 0]
    oovsuccesses = [0, 0, 0]
    for spellout_sent, lattice_sent in zip(spellout_file, lattice_file):
        cur_lat = 0
        conllu_d = list(conllu_as_spellouts(spellout_sent))
        conllul_d = list(conllul_as_lattices(lattice_sent))
        for spellout, lattice in zip(conllu_d, conllul_d):
            cur_lat += 1
            total += 1
            oov = isoov(lattice)
            oovs += 1 if oov else 0
            for i, ex in enumerate(extractors):
                result = calc_lattice_coverage(spellout, lattice, ex)
                successes[i] += result
                if oov:
                    oovsuccesses[i] += result
    return successes, total, oovsuccesses, oovs


def main():
    conllu = sys.argv[1]
    conllul = sys.argv[2]
    print calc_coverage(open(conllu), bz2.BZ2File(conllul))


if __name__ == "__main__":
    main()
