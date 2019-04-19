import os
import json


class Questionnaire(object):

    MAX_QUESTIONNAIRE_SCORE = 100
    META_FILE_NAME = 'default.meta.json'

    def __init__(self, pre, post):
        self.pre = pre
        self.post = post

    def _get_meta_file_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meta', self.META_FILE_NAME)

    def _calculate_pre_score(self):
        pass

    def _calculate_post_score(self):
        pass

    def _calculate_symptom_scores(self, questionnaire):
        pass


class SSQ(Questionnaire):
    META_FILE_NAME = 'ssq.meta.json'

    def score(self):
        pre_NS, pre_OS, pre_DS, pre_TS = self._calculate_pre_score()
        post_NS, post_OS, post_DS, post_TS = self._calculate_post_score()
        return [pre_NS, pre_OS, pre_DS, pre_TS, post_NS, post_OS, post_DS, post_TS]

    def _calculate_pre_score(self):
        N, O, D = self._calculate_symptom_scores(self.pre)
        return self._calculate_ssq_scores(N=N, O=O, D=D)

    def _calculate_post_score(self):
        N, O, D = self._calculate_symptom_scores(self.post)
        return self._calculate_ssq_scores(N=N, O=O, D=D)

    def _calculate_symptom_scores(self, questionnaire):
        N = 0.0
        O = 0.0
        D = 0.0
        with open(self._get_meta_file_path()) as meta_file:
            meta = json.load(meta_file)
            for s in meta['symptoms']:
                if s['weight']['N'] == 1:
                    N = N + (questionnaire[s['symptom']])
                if s['weight']['O'] == 1:
                    O = O + (questionnaire[s['symptom']])
                if s['weight']['D'] == 1:
                    D = D + (questionnaire[s['symptom']])
        print('N - %s, O - %s, D - %s' % (N, D, O))
        return [N, O, D]

    def _calculate_ssq_scores(self, N, O, D):
        with open(self._get_meta_file_path()) as meta_file:
            meta = json.load(meta_file)
            NS = N * meta['conversion_multipliers']['N']
            OS = O * meta['conversion_multipliers']['O']
            DS = D * meta['conversion_multipliers']['D']
            TS = (N + O + D) * meta['conversion_multipliers']['TS']
        print('NS - %s, OS - %s, DS - %s, TS - %s' % (NS, DS, OS, TS))
        return [NS, OS, DS, TS]
