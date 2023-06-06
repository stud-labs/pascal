import pymorphy3
from razdel import tokenize
import operator
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

    g = norms(inputfd)
    l = []
    while True:
        while len(l)<n:
            try:
                l.append(next(g))
            except StopIteration:
                yield l
                return
        yield l
        l.pop(0)


def fs(ab):
    a,b=ab
    return a+b

def pp(s1,s2):
    return map(fs, zip(s1,s2))

def assess(inputfd, kwsl, n=4):
    first = True
    s = [0]*len(kwsl)

    for seq in splittext(inputfd, n):
        if len(seq) < n:
            if first:
                s = assessseq(seq, kwsl)
                return list(s)
            else:
                return list(s)

        s = pp(assessseq(seq, kwsl), s)
        first = False
    return list(s)

def assessseq(seq, kwsl):
    return [assesskw(seq, kw) for kw in kwsl]

def assesskw(seq, kw, sp=""):
    assert(len(kw)>0)
    if len(kw) == 1:
        k = kw[0]
        s = 0
        for w in seq:
            if w==k:
                s += 1
        return s
    elif len(kw)>len(seq):
        return 0
    else:
        u=seq[:-1]
        a=seq[-1]
        v=kw[:-1]
        b=kw[-1]
        vb=kw
        if a==b:
            s1=assesskw(u,v, sp+"^^")
        else:
            s1=0
        s = assesskw(u,kw, sp+"vv", )
        s+=s1
        return s



# ---- USER space ---------------------

keywordset = ["информационная система",
              "трёхзвенная архитектура",
              "клиентское приложение"]

def prepkeywords(kwsl):
    kw = []
    for s in kwsl:
        kw.append(list(norms(io.StringIO(s))))
    return kw

def main():
    fn = "ex1.txt"
    kws = prepkeywords(keywordset)
    with open(fn) as i:
        s = assess(i, kws, 4)
        print(s)
    printnorms(fn)

def printnorms(fn):
    with open("out-"+fn, "w") as o:
        with open(fn) as i:
            for w in norms(i):
                o.write(w+" ")

def test101001():
    s="один ноль один ноль ноль один"
    kws=["один ноль один"]
    kws=prepkeywords(kws)
    with io.StringIO(s) as i:
        s = assess(i, kws, 6)
        print(s)

if __name__ == '__main__':
    main()
    # test101001()
