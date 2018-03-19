from github import Github, GithubException
import base64

UD_ORG = 'universaldependencies'
UL_ORG = 'conllul'

def get_github():
    githubkey = map(lambda l:l.strip(), open('.githubconllulkey').readlines())[0]
    return Github(githubkey)


def get_ud_repos(g):
    udorg = g.get_organization(UD_ORG)
    for udrepo in udorg.get_repos():
        if udrepo.name.startswith('UD_'):
            yield udrepo


def get_file_wrapper(r, filename):
    try:
        return r.get_file_contents("README.md")
    except Exception as e:
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


def process_treebank(r):
    # get train/dev/test files
    # run yap malearn
    # run yap ma on dev and test in ud mode (filenames with dd)
    # get_or_create conllul repository
    # add train/test/dev conllul files to repository
    # add base README


def make_baseline():
    print 'Getting github handle'
    g = get_github()
    for repo in get_ud_repos(g):
        if repo_has_text(repo):
            print "Processing UD repository %s" % (repo.name, )
        else:
            print "Skipping UD repository %s (found 'Includes text: No')" % (repo.name, )


if __name__ == "__main__":
    make_baseline()
