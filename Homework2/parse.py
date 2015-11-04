from providedcode.transitionparser import TransitionParser
from svmfeatureoptimizer import FeatureOptimizer
from  providedcode.dependencygraph import  DependencyGraph
import sys

if __name__ == '__main__':

    # Extract model name
    model = 'english.model'
    for arg in sys.argv:
        if '.model' in arg:
            model = arg

    filename = 'englishfile'

    # Check for model
    if model is None:
        print'Error... Need a model file. Closing parser.'
        sys.exit(0)

    # Check for file
    if not filename:
        print'Error... Need a data file. Closing parser.'
        sys.exit(0)

    try:
        # load feature optimizer
        feature_optimizer = FeatureOptimizer()

        # load sentences
        with open(filename) as fle:
            sentences = fle.readlines()

        dp_sentences = []
        for s in sentences:
            dp = DependencyGraph.from_sentence(s)
            dp_sentences.append(dp)

        # load the model
        tp = TransitionParser.load(model)

        # parse sentences
        print 'parsing sentences'
        parsed = tp.parse(dp_sentences, feature_optimizer)

        # write parsed to conll file
        with open(filename + '.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        print 'parsing complete'

    except NotImplementedError:
        print 'error'
