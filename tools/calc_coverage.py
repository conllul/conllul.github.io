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
    # pprint(lattice_spellouts, width=240)
    # pprint(projected_spellout, width=240)
    result = 1 if projected_spellout in lattice_spellouts else 0
    return result


def conllul_as_lattices(raw_sent):
    lattices = []
    cur_lattice = defaultdict(list)
    cur_lattice_token = ("", "", "")
    cur_lattice_end = -1
    cur_lattice_start = 0
    for line in raw_sent:
        # print "At line %s" % str(line)
        if '-' in line[0]:
            # encountered explicitly multi segment range line
            # print "At new range %s" % str(line)
            if cur_lattice:
                # if a lattice exists, add it
                misc_field = cur_lattice_token[2] if len(cur_lattice_token) > 2 else ""
                # print "Appending existing %s" % str((misc_field, cur_lattice, cur_lattice_token[0]))
                lattices.append((misc_field, cur_lattice, "%s-%s" % (cur_lattice_start, cur_lattice_end)))
            # print "Start new lattice for %s" % line[1]
            cur_lattice = defaultdict(list)
            cur_lattice_token = line
            line_split = line[0].split('-')
            cur_lattice_start = int(line_split[0])
            cur_lattice_end = int(line_split[1])
            continue
        if line[6] == "None":
            line[6] = "_"
        cur_line_start = int(line[0])
        cur_line_end = int(line[1])
        if cur_line_start >= cur_lattice_start and cur_line_start < cur_lattice_end and cur_line_end <= cur_lattice_end:
            # print "Add edge to existing lattice"
            # encountered line from in-progress lattice
            cur_lattice[line[0]].append(line)
            continue
        if cur_lattice_start == cur_line_start:
            # line is a previously un-encountered lattice
            if cur_lattice:
                # if a lattice exists, add it
                misc_field = cur_lattice_token[2] if len(cur_lattice_token) > 2 else ""
                # print "Appending existing %s" % str((misc_field, cur_lattice, "%s-%s" % (cur_lattice_start, cur_lattice_end)))
                lattices.append((misc_field, cur_lattice, "%s-%s" % (cur_lattice_start, cur_lattice_end)))
            # print "Start new lattice for %s" % line[2]
            cur_lattice = defaultdict(list)
            cur_lattice_token = line
            cur_lattice_start = int(line[0])
            cur_lattice_end = int(line[1])
            cur_lattice[line[0]].append(line)
            continue
        if cur_lattice_end == cur_line_start:
            if cur_lattice:
                # if a lattice exists, add it
                misc_field = cur_lattice_token[2] if len(cur_lattice_token) > 2 else ""
                # print "Appending existing %s" % str((misc_field, cur_lattice, "%s-%s" % (cur_lattice_start, cur_lattice_end)))
                lattices.append((misc_field, cur_lattice, "%s-%s" % (cur_lattice_start, cur_lattice_end)))
            # print "Start new lattice for %s" % line[2]
            cur_lattice = defaultdict(list)
            cur_lattice_token = line
            cur_lattice_start = int(line[0])
            cur_lattice_end = int(line[1])
            cur_lattice[line[0]].append(line)
        else:
            # this is an error condition
            # print "Error"
            # sys.exit(1)
            return list()
    if cur_lattice:
        misc_field = cur_lattice_token[2] if len(cur_lattice_token) > 2 else ""
        lattices.append((misc_field, cur_lattice, "%s-%s" % (cur_lattice_start, cur_lattice_end)))
    # print "Returning lattice"
    # pprint(lattices, width=220)
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
        if cur_spellout:
            spellouts.append(cur_spellout)
            cur_spellout = list()
        spellouts.append([line])
        remaining_segments = 0
        cur_spellout = list()
    if cur_spellout:
        spellouts.append(cur_spellout)
    return spellouts


def isoov(lattice):
    if lattice:
        return 'oov' in lattice[0]
    else:
        return False


extractors = [lambda v:[v[1]], lambda v:[v[1], v[3]], lambda v:[v[1], v[3], v[5]]]
# extractors = [lambda v:[v[1], v[3], v[5]]]
def calc_coverage(spellout_reader, lattice_reader, limit=0):
    spellout_file = depread(spellout_reader)
    lattice_file = depread(lattice_reader)
    total = 0
    oovs = 0
    successes = [0, 0, 0]
    oovsuccesses = [0, 0, 0]
    sents = 0
    for spellout_sent, lattice_sent in zip(spellout_file, lattice_file):
        sents += 1
        if limit and sents > limit:
            break
        # print "At sent %d" % sents
        conllu_d = list(conllu_as_spellouts(spellout_sent))
        conllul_d = list(conllul_as_lattices(lattice_sent))
        if len(conllul_d) == 0:
            # print "Skipping"
            total += len(conllu_d)
            continue
        for spellout, lattice in zip(conllu_d, conllul_d):
            total += 1
            oov = isoov(lattice)
            oovs += 1 if oov else 0
            for i, ex in enumerate(extractors):
                result = calc_lattice_coverage(spellout, lattice, ex)
                # print "%s " % result, 
                successes[i] += result
                if oov:
                    oovsuccesses[i] += result
            # print ""
    return successes, total, oovsuccesses, oovs


def main():
    conllu = sys.argv[1]
    conllul = sys.argv[2]
    limit = 0 if len(sys.argv) < 4 else int(sys.argv[3])
    print calc_coverage(open(conllu), bz2.BZ2File(conllul), limit)


if __name__ == "__main__":
    main()
