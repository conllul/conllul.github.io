#!/usr/bin/python

from github import Github, GithubException
import base64
import os
import sys
import json
import operator
import subprocess

UD_ORG = 'universaldependencies'
UL_ORG = 'conllul'

UD_TB_LOOKUP = json.load(open('lcodes.json'))

def get_github(orgname):
    githubkey = map(lambda l:l.strip(), open('.githubconllulkey').readlines())[0]
    g = Github(githubkey)
    return g, g.get_organization(orgname)


def get_ud_repos(udorg):
    for udrepo in udorg.get_repos():
        if udrepo.name.startswith('UD_'):
            yield udrepo


def get_file_wrapper(r, filename=None):
    try:
        if not filename:
            filename = "README.md"
        return r.get_file_contents(filename, ref='dev')
    except Exception as e:
        return False


def get_blob_wrapper(r, filename):
    try:
        dir_contents = r.get_dir_contents('/', ref='dev')
        for f in dir_contents:
            if f.name == filename:
                return r.get_git_blob(f.sha)
        print "File %s not found in base of repo %s" % (filename, r.name)
        return False
    except Exception as e:
        print "%s failed to to get blob %s: %s" % (r.name, filename, str(e))
        return False


def compare_master_dev(r, filename):
    try:
        repo_file = filename.split('/')[1]
        print("\t\tGetting %s from %s ref %s" % (repo_file, r.name, 'master'))
        master = r.get_contents(repo_file, ref='master')
        print("\t\tGetting %s from %s ref %s" % (repo_file, r.name, 'dev'))
        dev = r.get_contents(repo_file, ref='dev')
        return master.sha == dev.sha
    except Exception as e:
        print("\t\tException caught comparing master/dev for repo %s: %s" % (r.name, str(e)))
        return False


def repo_has_text(r):
    readme = get_file_wrapper(r, "README.md")
    if not readme:
        readme = get_file_wrapper(r, "README.txt")

    if not readme:
        return False

    if readme.encoding == "base64":
        text = base64.b64decode(readme.content)
        lines = text.split('\n')
        for line in lines:
            if line == 'Includes text: No':
                return False

    return True


def yap_malearn(out_dir, train, dd):
    print "\tTraining data-driven"
    logfile = open("%s/malearn.log" % out_dir, 'w')
    subprocess.call(['./yap', 'malearn', '-conllu', train, '-out', dd], stderr=logfile)
    logfile.close()


def yap_ma(out_dir, dd, filetype, filename, lattice):
    logfile = open("%s/%s-ma.log" % (out_dir,filetype), 'w')
    subprocess.call(['./yap', 'ma', '-dict', dd, '-conllu', filename, '-format', 'ud', '-out', lattice], stderr=logfile)
    logfile.close()


def process_treebank(o, conllulorg, r, file_prefix):
    def file_name_render(prefix, split, ma_name=None, directory=None):
        ma_str = ("%s." % ma_name) if ma_name else ""
        dir_str = ("%s/" % directory)  if directory else ""
        file_name = "%s%s-ud-%s.%sconllu" % (dir_str, prefix, split, ma_str)
        return file_name

    ul_repo = r.name.replace('UD_','UL_')
    train_file = file_name_render(file_prefix, "train", directory=ul_repo)
    dev_file = file_name_render(file_prefix, "dev", directory=ul_repo)
    test_file = file_name_render(file_prefix, "test", directory=ul_repo)
    splits = [train_file, dev_file, test_file]
    if not os.path.exists(ul_repo):
        print "\tCreating directory %s" % ul_repo
        os.mkdir(ul_repo)
    print "\tGetting treebank files"
    for split in splits:
        repo_file = split.replace("%s/" % ul_repo, "")
        f_data = get_blob_wrapper(r, repo_file)
        if f_data:
            f = open(split, 'w')
            f.write(base64.b64decode(f_data.content))
            f.close()
        else:
            print "not found, skipping treebank"
            return
    dict_file = "%s-dd/%s.json" % (ul_repo, file_prefix)
    yap_malearn(ul_repo, train_file, dict_file)
    print "\tAnalyzing treebank files"
    yap_ma(ul_repo, dict_file, 'train', train_file, file_name_render(file_prefix, "train", "baseline", directory=ul_repo) + 'l')
    yap_ma(ul_repo, dict_file, 'dev', dev_file, file_name_render(file_prefix, "dev", "baseline", directory=ul_repo) + 'l')
    yap_ma(ul_repo, dict_file, 'test', test_file, file_name_render(file_prefix, "test", "baseline", directory=ul_repo) + 'l')
    try:
        conllulorg.get_repo(ul_repo)
    except Exception as e:
        try:
            conllulorg.create_repo(ul_repo, private=False)
            print "\tCreate repository %s" % ul_repo
        except Exception as e2:
            print "Failed creating non-existent repo %s for %s" % (ul_repo, r.name)
    return True


def deduce_lcode(repo):
    dir_contents = repo.get_dir_contents('/')
    for f in dir_contents:
        if f.name.endswith('.conllu'):
            repo_name = f.name
            repo_split = repo_name.split('-')
            return repo_split[0]
    return False

def make_baseline():
    print 'Getting github handle'
    _, o = get_github(UD_ORG)
    _, conllulo = get_github(UL_ORG)
    for repo in get_ud_repos(o):
        sys.stdout.flush()
        if repo_has_text(repo):
            # if os.path.exists(repo.name.replace('UD_', 'UL_')):
            #     print "Skipping already created UD repository %s" % (repo.name, )
            #     continue
            lcode = UD_TB_LOOKUP.get(repo.name[3:], None) 
            if not lcode:
                lcode = deduce_lcode(repo)
                if not lcode:
                    print "Skipping UD repository %s (repo not in lcodes.json and no conllu file found)" % (repo.name, )
                    continue
            print "Processing UD repository %s" % (repo.name, )
            try:
                if not process_treebank(o, conllulo, repo, lcode):
                    print "Failed %s" % repo.name
            except Exception as e:
                print "Failed %s" % repo.name
                print e
        else:
            print "Skipping UD repository %s (found 'Includes text: No')" % (repo.name, )


if __name__ == "__main__":
    make_baseline()
