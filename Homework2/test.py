import random
from providedcode import dataset
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition

if __name__ == '__main__':

    # load test set in swedish and get 200 random sentences
    swedish_data = dataset.get_swedish_train_corpus().parsed_sents()
    random.seed()
    swedish_subdata = random.sample(swedish_data, 200)

    # load test set in english and get 200 random sentences
    english_data = dataset.get_english_train_corpus().parsed_sents()
    random.seed()
    english_subdata = random.sample(english_data, 200)

    # load test set in danish and get 200 random sentences
    danish_data = dataset.get_danish_train_corpus().parsed_sents()
    random.seed()
    danish_subdata = random.sample(danish_data, 200)

    try:
        print 'training swedish'

        # swedish
        tp = TransitionParser(Transition, FeatureExtractor)
        tp.train(swedish_subdata)
        tp.save('swedish.model')

        testdata = dataset.get_swedish_test_corpus().parsed_sents()
        tp = TransitionParser.load('swedish.model')

        print 'testing swedish'
        parsed = tp.parse(testdata)

        with open('test.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata, parsed)
        print 'Swedish results'
        print "UAS: {} \nLAS: {}".format(*ev.eval())


        # english
        print '\n----------------------\n'
        print 'Training english'
        tpe = TransitionParser(Transition, FeatureExtractor)
        tpe.train(english_subdata)
        tpe.save('english.model')

        print 'testing english'
        testdataE = dataset.get_english_dev_corpus().parsed_sents()
        tpe = TransitionParser.load('english.model')

        parsede = tpe.parse(testdataE)

        eve = DependencyEvaluator(testdataE, parsede)
        print 'English results'
        print "UAS: {} \nLAS: {}".format(*eve.eval())

        # danish
        print '\n----------------------\n'
        print 'Training Danish'
        tpD = TransitionParser(Transition, FeatureExtractor)
        tpD.train(danish_subdata)
        tpD.save('danish.model')

        print 'Testing Danish'
        testdataD = dataset.get_danish_train_corpus().parsed_sents()
        tpD = TransitionParser.load('danish.model')

        parsedD = tpD.parse(testdataD)

        evD = DependencyEvaluator(testdataD, parsedD)
        print 'Danish results'
        print "UAS: {} \nLAS: {}".format(*evD.eval())

        # parsing arbitrary sentences (english):
        # sentence = DependencyGraph.from_sentence('Hi, this is a test')

        # tp = TransitionParser.load('english.model')
        # parsed = tp.parse([sentence])
        # print parsed[0].to_conll(10).encode('utf-8')
    except NotImplementedError:
        print """
        This file is currently broken! We removed the implementation of Transition
        (in transition.py), which tells the transitionparser how to go from one
        Configuration to another Configuration. This is an essential part of the
        arc-eager dependency parsing algorithm, so you should probably fix that :)

        The algorithm is described in great detail here:
            http://aclweb.org/anthology//C/C12/C12-1059.pdf

        We also haven't actually implemented most of the features for for the
        support vector machine (in featureextractor.py), so as you might expect the
        evaluator is going to give you somewhat bad results...

        Your output should look something like this:

            UAS: 0.23023302131
            LAS: 0.125273849831

        Not this:

            Traceback (most recent call last):
                File "test.py", line 41, in <module>
                    ...
                    NotImplementedError: Please implement shift!


        """
