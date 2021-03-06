# built-in module
import os
import pickle
from nltk.corpus import stopwords
from nltk import tokenize

# 3rd-party module
from tqdm import tqdm

class BaseTokenizer:
    def __init__(self, config):
        # padding token
        self.pad_token = '[pad]'
        self.pad_token_id = 0

        # others
        self.token_to_id = {}
        self.id_to_token = {}
        self.config = config

        self.token_to_id[self.pad_token] = self.pad_token_id
        self.id_to_token[self.pad_token_id] = self.pad_token

    def tokenize(self, sentences, task_ids):
        # nltk TweetTokenizer for stance
        tweet_tokenizer = tokenize.TweetTokenizer()

        # nltk WordPunctTokenizer for NLI
        punct_tokenizer = tokenize.WordPunctTokenizer()

        all_sentence = []
        for sentence, task_id in zip(sentences, task_ids):
            if task_id == 0:  # stance
                tokenize_sent = tweet_tokenizer.tokenize(sentence)
            elif task_id == 1:  # NLI
                tokenize_sent = punct_tokenizer.tokenize(sentence)

            all_sentence.append(tokenize_sent)

        return all_sentence

    def detokenize(self, sentences):
        return [' '.join(sentence) for sentence in sentences]

    def build_vocabulary(self, sentences, task_ids):
        # tokenize
        sentences = self.tokenize(sentences, task_ids)

        # get all tokens
        all_tokens = set()
        for sent in sentences:
            all_tokens |= set(sent)
        all_tokens = sorted(list(all_tokens))

        # build vocabulary
        for idx in range(len(all_tokens)):
            self.token_to_id[all_tokens[idx]] = idx+1  # start from 1, 0 for padding token
            self.id_to_token[idx+1] = all_tokens[idx]

    def convert_tokens_to_ids(self, sentences):
        result = []

        for sentence in sentences:
            ids = []
            for token in sentence:
                if token in self.token_to_id:
                    ids.append(self.token_to_id[token])
                else:
                    ids.append(self.pad_token_id)
            result.append(ids)

        return result

    def convert_ids_to_tokens(self, sentences):
        result = []

        for sentence in sentences:
            tokens = []
            for idx in sentence:
                if idx in self.id_to_token:
                    tokens.append(self.id_to_token[idx])
                else:
                    raise ValueError(f'idx {idx} not in the dictionary')
            result.append(tokens)

        return result

    def encode(self, sentences, task_ids):
        # convert tokens to ids
        sentences = self.convert_tokens_to_ids(
            self.tokenize(sentences, task_ids))

        # get max length of sentence
        max_stance_len = max([len(sent) for sent, task in zip(sentences, task_ids)
                              if task == 0])
        max_seq_len = (self.config.max_seq_len
                       if self.config.max_seq_len > max_stance_len
                       else max_stance_len)

        # cut off or padding
        task_sentences, shared_sentences = [], []
        for task_sent, shared_sent, task_id in zip(sentences, sentences, task_ids):
            # cutoff sentence
            task_sent = task_sent[:max_seq_len]
            shared_sent = shared_sent[:max_seq_len]

            # padding for each task sentence
            if task_id == 0:  # stance
                task_pad_count = max_stance_len - len(task_sent)
            elif task_id == 1:  # NLI
                task_pad_count = max_seq_len - len(task_sent)

            task_sent.extend([self.pad_token_id] * task_pad_count)

            # padding for shared sentence
            shared_pad_count = max_seq_len - len(shared_sent)
            shared_sent.extend([self.pad_token_id] * shared_pad_count)

            task_sentences.append(task_sent)
            shared_sentences.append(shared_sent)

        return task_sentences, shared_sentences

    def decode(self, sentences):
        sentences = self.detokenize(self.convert_ids_to_tokens(sentences))

        return sentences

    def load(self, file_path=None):
        if file_path is None or type(file_path) != str:
            raise ValueError('argument `file_path` should be a string')
        elif not os.path.exists(file_path):
            raise FileNotFoundError('file {} does not exist'.format(file_path))

        with open(file_path, 'rb') as f:
            tokenizer = pickle.load(f)
            self.token_to_id = tokenizer.token_to_id
            self.id_to_token = tokenizer.id_to_token

    def save(self, file_path=None):
        if file_path is None or type(file_path) != str:
            raise ValueError('argument `file_path` should be a string')
        else:
            with open(file_path, 'wb') as f:
                pickle.dump(self, f)