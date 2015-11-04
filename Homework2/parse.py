from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
import sys


if __name__ == '__main__':

    # Extract model name
    model = None
    filename = None

    # extract params
    for idx, arg in enumerate(sys.argv):
        if idx == 1:
            filename = arg

        if '.model' in arg:
            model = arg

    # Check for model
    if model is None:
        print'Error... Need a model file. Closing parser.'
        sys.exit(0)

    # Check for file
    if not filename:
        print'Error... Need a data file. Closing parser.'
        sys.exit(0)

    try:

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
        parsed = tp.parse(dp_sentences)

        # write parsed to conll file
        with open(filename + '.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        print 'parsing complete'

    except Exception:
        print 'error'
