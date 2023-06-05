import pymorphy3
from razdel import tokenize
import io

# DAWG

morph = pymorphy3.MorphAnalyzer(lang="ru")

def norm(w):
    morps = morph.parse(w)
    bf = morps[0]
    tag = bf.tag
    # https://github.com/no-plagiarism/pymorphy3/blob/master/docs/user/grammemes.rst
    for gr in ["NOUN", "VERB", "ADJF", "ADJS"]:
        if gr in tag:
            return bf.normal_form
            # return (gr, bf.normal_form)
    return None


def words(inputfd):
    for l in inputfd.readlines():
        ws = tokenize(l)
        l=[a.text for a in ws]
        yield from l


def norms(inputfd):
    for w in words(inputfd):
        n = norm(w)
        if n:
            yield n


def splittext(inputfd, n):


def assess(inputfd, kwsl, n=4):
    for seq in splittext(inputfd, n):
        assessseq(seq, kwsl)


# ---- USER space ---------------------

keywordset = ["информационная система",
              "трехзвенная архитектура",
              "клиентское приложение"]

def prepkeywords(kwsl):
    kw = []
    for s in kwsl:
        kw.append(list(norms(io.StringIO(s))))
    return kw

def main():
    print(prepkeywords(keywordset))
    quit()
    with open("./ex1.txt") as i:
        for w in norms(i):
            print(w, end=" ")


if __name__ == '__main__':
    main()
