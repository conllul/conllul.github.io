#!/usr/bin/python

from github import Github, GithubException
import base64
import os
import sys
import json
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
        return r.get_file_contents(filename)
    except Exception as e:
        return False


def get_blob_wrapper(r, filename):
    try:
        dir_contents = r.get_dir_contents('/')
        for f in dir_contents:
            if f.name == filename:
                return r.get_git_blob(f.sha)
        print "File %s not found in base of repo %s" % (filename, r.name)
        return False
    except Exception as e:
        print "%s failed to to get blob %s: %s" % (r.name, filename, str(e))
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


def process_treebank(o, conllulorg, r):
    def file_name_render(prefix, split, ma_name=None, directory=None):
        ma_str = ("%s." % ma_name) if ma_name else ""
        dir_str = ("%s/" % directory)  if directory else ""
        file_name = "%s%s-ud-%s.%sconllu" % (dir_str, prefix, split, ma_str)
        return file_name

    file_prefix = UD_TB_LOOKUP.get(r.name[3:], None)
    if not file_prefix:
        return False
    train_file = file_name_render(file_prefix, "train", directory=r.name)
    dev_file = file_name_render(file_prefix, "dev", directory=r.name)
    test_file = file_name_render(file_prefix, "test", directory=r.name)
    splits = [train_file, dev_file, test_file]
    os.mkdir(r.name)
    print "\tGetting treebank files"
    for split in splits:
        repo_file = split.replace("%s/" % r.name, "")
        f_data = get_blob_wrapper(r, repo_file)
        if f_data:
            f = open(split, 'w')
            f.write(base64.b64decode(f_data.content))
            f.close()
        else:
            print "not found, skipping treebank"
            return
    dict_file = "%s/%s.json" % (r.name, file_prefix)
    yap_malearn(r.name, train_file, dict_file)
    print "\tAnalyzing treebank files"
    yap_ma(r.name, dict_file, 'train', train_file, file_name_render(file_prefix, "train", "baseline", directory=r.name))
    yap_ma(r.name, dict_file, 'dev', dev_file, file_name_render(file_prefix, "dev", "baseline", directory=r.name))
    yap_ma(r.name, dict_file, 'test', test_file, file_name_render(file_prefix, "test", "baseline", directory=r.name))
    try:
        conllulorg.get_repo(r.name)
    except Exception as e:
        try:
            conllulorg.create_repo(r.name, private=False, homepage='README.md')
            print "\tCreate repository"
        except Exception as e2:
            print "Failed creating non-existent repo for %s" % r.name
    return True


def make_baseline():
    print 'Getting github handle'
    _, o = get_github(UD_ORG)
    _, conllulo = get_github(UL_ORG)
    for repo in get_ud_repos(o):
        sys.stdout.flush()
        if repo_has_text(repo):
            if repo.name[3:] not in UD_TB_LOOKUP:
                print "Skipping UD repository %s (repo not in lcodes.json)" % (repo.name, )
                continue
            print "Processing UD repository %s" % (repo.name, )
            try:
                if not process_treebank(o, conllulo, repo):
                    print "Failed %s" % repo.name
            except Exception as e:
                print "Failed %s" % repo.name
                print e
        else:
            print "Skipping UD repository %s (found 'Includes text: No')" % (repo.name, )


if __name__ == "__main__":
    make_baseline()
