from abc import ABC,abstractmethod
from pandas import DataFrame
from data import ShortAnswerInstance
from typing import List
import re
import textdistance as td
import pandas as pd
import sys

TARGET_DELIMS_PATTERN = re.compile('|'.join(map(re.escape, ["•", "ODER", " / "])))
MEASURES = [
    td.algorithms.edit_based.NeedlemanWunsch(),
    td.algorithms.edit_based.SmithWaterman(),
    td.algorithms.sequence_based.LCSSeq(),
    td.algorithms.sequence_based.LCSStr(),
    td.algorithms.simple.Length(),
    td.algorithms.phonetic.Editex(),
    td.algorithms.phonetic.MRA(),
    td.algorithms.token_based.Overlap(),
    td.algorithms.token_based.Cosine()
]
simCache = {}



class FeatureGroupExtractor(ABC):
    @abstractmethod
    def extract(self, instances: List[ShortAnswerInstance]) -> DataFrame:
        return DataFrame()


class SIMGroupExtractor(FeatureGroupExtractor):

    def extract(self, instances: List[ShortAnswerInstance]) -> DataFrame:
        # extract student and target answers from ShortAnswerInstances
        st_tgt_answers = [(x.answer, x.itemTargets[0]) for x in
                          instances]  # TODO: what to do if there are several target sentences?
        ids = [x.taskId + '_' + x.itemId + '_' + x.learnerId for x in
               instances]  # TODO: add answer ID? taskId_itemId_learnerId ?
        # TODO: there are no learner IDs in the test file

        d = pd.DataFrame([self.similarity_features(r, t, MEASURES) for r, t in st_tgt_answers],
                         columns=[type(i).__name__ for i in MEASURES])
        d['ID'] = ids

        d.to_csv("testing/sim_test.tsv", sep='\t', encoding='utf8', index=False)
        print("Saved sim features to testing/sim_test.tsv")

        return d

    def extract_sim_per_instance(self):
        pass

    def get_target_alternatives(self, targetstr):
        return TARGET_DELIMS_PATTERN.split(targetstr)

    def sim_lookup_str(self, response, a, m):
        return response + "  " + a + " | " + type(m).__name__

    def similarity_features(self, response, target, measures):
        target = str(target)
        response = str(response)
        resultScores = []
        alternatives = self.get_target_alternatives(target)

        for m in measures:
            max_sim = -1.0
            for a in alternatives:
                a = str(a)
                try:
                    lookup = self.sim_lookup_str(response, a, m)
                    simCache.setdefault(lookup, m.normalized_similarity(response, a))
                    sim = simCache[lookup]
                    if sim > max_sim:
                        max_sim = sim
                except:
                    # this should only happen for German answers and phonetic distance measures
                    print("Error with measure", m, "on strings '", response, "' and '", a, "'", file=sys.stderr)

            resultScores.append(max_sim)

        return resultScores


class BOWGroupExtractor(FeatureGroupExtractor):
    def extract(self, instances: List[ShortAnswerInstance]) -> DataFrame:
        # add implementation
        """
        Copied over from isaac-data-analysis
        bag = train_bag(" ".join(datafr[columns_to_be_used['studentAnswer']]), 500)
        d = pd.DataFrame(bow_features(bag, datafr), columns=bag)
        d['ID'] = datafr['ID']"""
        pass

    # train on all instances passed?
    def train_bag(self, text, n=500):
        words = [w for w in text.lower().split(" ") if w]
        word_counts = {}
        for w in words:
            if w not in word_counts:
                word_counts[w] = 0.0
            word_counts[w] += 1.0

        sorted_words = sorted(word_counts.keys(), key=lambda x: word_counts[x], reverse=True)
        return sorted_words[:n]

    def bag_representation(self,bag, text):
        text = set(map(lambda w: w.lower(), text.split()))
        return [float(w in text) for w in
                bag]  # todo: CREATES AN INCORRECT REPRESENTATION because .lower() was not used!!!

    def bow_features(self, bag, instances):
        return [self.bag_representation(bag, x) for x in instances["value.raw"]] # TODO: change "value.raw"

    # TODO: is this method still needed?
    def bag_count_representation(self, bag, text):
        return [float(len(re.findall(w, text))) for w in bag]






