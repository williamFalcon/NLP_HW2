__author__ = 'waf'
import itertools as it
import re


class FeatureOptimizer():
    """
    This class enumerates all possible combinations of feature subjects (like Stack[0]), and associated
    features to test on that subject.
    It then extracts the relevant information for that test.
    """

    # Each feature is focused around a subject. These are the subject we will focus on.
    # first part of word shows data_source to use. Second part shows index of that datasource
    feature_subjects = ['STK_-1', 'STK_-2', 'STK_-3', 'BUF_0', 'BUF_1', 'BUF_2', 'BUF_3']
    book_tests = ['']

    # Each of these is a feature of that token. They are vanilla because each is accesible via key value
    vanilla_features = ['_WORD_', '_TAG_', '_LEMMA_']

    # Each of these features requires a customized extraction implementation
    advances_features = ['_LDEP_', '_RDEP_', '_FEATS_']

    # combinations of all tests we will run
    tests = []

    active_tests = ['STK_-1_WORD_', 'STK_-1_TAG_', 'STK_-1_LEMMA_', 'STK_-1_LDEP_',
                    'STK_-2_TAG_',
                    'BUF_0_WORD_', 'BUF_0_TAG_', 'BUF_0_LEMMA_', 'BUF_0_LDEP_',
                    'BUF_1_TAG_', 'BUF_1_WORD_',
                    'BUF_2_TAG_'
                    ]

    possible_tests = ['STK_-1_WORD_', 'STK_-1_TAG_', 'STK_-1_LEMMA_', 'STK_-1_LDEP_', 'STK_-1_RDEP_', 'STK_-1_FEATS_',
                      'STK_-2_WORD_', 'STK_-2_TAG_', 'STK_-2_LEMMA_', 'STK_-2_LDEP_', 'STK_-2_RDEP_', 'STK_-2_FEATS_',
                      'STK_-3_WORD_', 'STK_-3_TAG_', 'STK_-3_LEMMA_', 'STK_-3_LDEP_', 'STK_-3_RDEP_', 'STK_-3_FEATS_',
                      'BUF_0_WORD_', 'BUF_0_TAG_', 'BUF_0_LEMMA_', 'BUF_0_LDEP_', 'BUF_0_RDEP_', 'BUF_0_FEATS_',
                      'BUF_1_WORD_', 'BUF_1_TAG_', 'BUF_1_LEMMA_', 'BUF_1_LDEP_', 'BUF_1_RDEP_', 'BUF_1_FEATS_',
                      'BUF_2_WORD_', 'BUF_2_TAG_', 'BUF_2_LEMMA_', 'BUF_2_LDEP_', 'BUF_2_RDEP_', 'BUF_2_FEATS_',
                      'BUF_3_WORD_', 'BUF_3_TAG_', 'BUF_3_LEMMA_', 'BUF_3_LDEP_', 'BUF_3_RDEP_', 'BUF_3_FEATS_'
                      ]


    def __init__(self):
        self.build_feature_tests()

    def build_feature_tests(self):

        self.tests = self.active_tests
        #tests = self.build_linear_combinations()
        # run each test individually, then
        #combinations = self.powerset(tests)

        #print combinations

    def powerset(self, items):
        results = []
        for pair in it.combinations(items, 2):
            results.append(pair)

        return results

    def build_linear_combinations(self):
        """
        Builds all permutations of features we will run
        :return:
        """
        tests = []
        for subj in self.feature_subjects:
            all_features = self.vanilla_features + self.advances_features
            for feat in all_features:
                test = subj + feat
                tests.append(test)
        return tests

    def insert_features_for_test(self, test, tokens, buff, stack, arcs, result):
        """
        Adds relevant feature for the given test
        """
        data_source_id, index, feature = self.params_from_test(test)

        # pick where the item will come from
        actual_source = stack if data_source_id == 'STK' else buff

        # extract that index
        min_size = abs(index)
        if len(actual_source)-1 >= min_size:
            ds_index = actual_source[index]
            token = tokens[ds_index]

            # vanilla feature = something we can find through key value lookup
            modded_feat = '_' + feature + '_'
            if modded_feat in self.vanilla_features:
                if self._check_informative(modded_feat):
                    lower = feature.lower()
                    if token[lower] is not None:
                        mod_test_name = self.svm_friendly_stack_test_name(test, index) if data_source_id == 'STK' else test
                        mod_test_name = re.sub(r"WORD", "FORM", mod_test_name)
                        result.append(mod_test_name + token[lower])
            else:
                self.handle_advance_feature(token, ds_index, feature, test, arcs, result, index, data_source_id)

    def handle_advance_feature(self, token, token_index, feature, test, arcs, result, index, data_source_id):
        """
        Inserts relevant feature for unique test
        """
        # add LDEP feature
        if feature == 'LDEP':
            dep_left_most, dep_right_most = self.find_left_right_dependencies(token_index, arcs)
            if self._check_informative(dep_left_most):
                mod_test_name = self.svm_friendly_stack_test_name(test, index) if data_source_id == 'STK' else test
                result.append(mod_test_name + dep_left_most)

        # add RDEP feature
        if feature == 'RDEP':
            dep_left_most, dep_right_most = self.find_left_right_dependencies(token_index, arcs)
            if self._check_informative(dep_right_most):
                mod_test_name = self.svm_friendly_stack_test_name(test, index) if data_source_id == 'STK' else test
                result.append(mod_test_name + dep_right_most)

        # add feats for each subject
        if feature == 'FEATS':
            if 'feats' in token and self._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    mod_test_name = self.svm_friendly_stack_test_name(test, index) if data_source_id == 'STK' else test
                    result.append(test + mod_test_name)

    def svm_friendly_stack_test_name(self, test, original_index):
        new_index = abs(original_index + 1)
        new_test = re.sub(r"-?[0-9]+", str(new_index), test)
        return new_test

    def find_left_right_dependencies(self, idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    def _check_informative(self, feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """
        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    def params_from_test(self, test):
        """
        Breaks down instructions for the test
        :param test:
        :return:
        """
        local = test[0:-1]
        data_source, index, feature = local.split('_')

        return data_source, int(index), feature