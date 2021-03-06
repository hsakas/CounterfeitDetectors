"""
@author: aswamy
"""

from typing import Tuple

import torch
import torch.nn as nn
from annoy import AnnoyIndex

from searcher.char2vec import sentence_char2vec


class FakeDetector:
    """
    #TODO: Complete the description
    """

    def __init__(self):
        """

        """
        self.tree = None
        self.cos = nn.CosineSimilarity(dim=1, eps=1e-6)
        # self.embedder = EmbedSentence()

    def build(self, brand_names: str, n_tree: int = 100, embedding_size: int = 100):
        """
        #TODO: fill details of param
        :param brand_names:
        :param n_tree:
        :param embedding_size:
        :return:
        """
        brand_names_sentence = sentence_char2vec(brand_names)
        self.tree = AnnoyIndex(embedding_size, 'angular')

        for value, (_, _token) in enumerate(brand_names_sentence.items()):
            self.tree.add_item(value, _token)

        self.tree.build(n_tree)

    def fake_detector(self, text: str, embedding_size: int = 100, detection_range: Tuple = (0.97, 0.99)) -> bool:
        """
        #TODO: fill details of params
        :param text:
        :param embedding_size:
        :param detection_range:
        :return:
        """
        found_match = False
        text_sentence = sentence_char2vec(text)
        for _, (_, _token) in enumerate(text_sentence.items()):
            match = self.tree.get_nns_by_vector(_token, 1)[0]
            sim_score = round(float(self.cos(_token.view(-1, embedding_size),
                                             torch.tensor(self.tree.get_item_vector(match)).view(-1, embedding_size))),
                              2)

            if detection_range[0] <= sim_score <= detection_range[1]:
                found_match = True

            if found_match:
                break

        return found_match
