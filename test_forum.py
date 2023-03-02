import utils 
import json

# def test_1():
#     assert False
#     pass

def test_forum():
    with open('sample.json') as f:
        for line in f:
            # print(line)
            x = json.loads(line)
            assert x !=None
            n = utils.nombre_messages(x['content'])
            # assert n ==  x['content']['comments_count']+1
            assert False

def test_factorielle():
    n = utils.factorielle(1)
    assert n == 1
    n = utils.factorielle(2)
    assert n == 2
    n = utils.factorielle(3)
    assert n == 6
    n = utils.factorielle(4)
    assert n == 24
    n = utils.factorielle(10)
    assert n == 3628800
    