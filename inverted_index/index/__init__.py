import operator, math, queue, threading, pickle

from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords as stopwords_from_nltk

# stopwords from nltk
# {‘ourselves’, ‘hers’, ‘between’, ‘yourself’, ‘but’, ‘again’, ‘there’, ‘about’, ‘once’, ‘during’, ‘out’, ‘very’, ‘having’, ‘with’, ‘they’, ‘own’, ‘an’, ‘be’, ‘some’, ‘for’, ‘do’, ‘its’, ‘yours’, ‘such’, ‘into’, ‘of’, ‘most’, ‘itself’, ‘other’, ‘off’, ‘is’, ‘s’, ‘am’, ‘or’, ‘who’, ‘as’, ‘from’, ‘him’, ‘each’, ‘the’, ‘themselves’, ‘until’, ‘below’, ‘are’, ‘we’, ‘these’, ‘your’, ‘his’, ‘through’, ‘don’, ‘nor’, ‘me’, ‘were’, ‘her’, ‘more’, ‘himself’, ‘this’, ‘down’, ‘should’, ‘our’, ‘their’, ‘while’, ‘above’, ‘both’, ‘up’, ‘to’, ‘ours’, ‘had’, ‘she’, ‘all’, ‘no’, ‘when’, ‘at’, ‘any’, ‘before’, ‘them’, ‘same’, ‘and’, ‘been’, ‘have’, ‘in’, ‘will’, ‘on’, ‘does’, ‘yourselves’, ‘then’, ‘that’, ‘because’, ‘what’, ‘over’, ‘why’, ‘so’, ‘can’, ‘did’, ‘not’, ‘now’, ‘under’, ‘he’, ‘you’, ‘herself’, ‘has’, ‘just’, ‘where’, ‘too’, ‘only’, ‘myself’, ‘which’, ‘those’, ‘i’, ‘after’, ‘few’, ‘whom’, ‘t’, ‘being’, ‘if’, ‘theirs’, ‘my’, ‘against’, ‘a’, ‘by’, ‘doing’, ‘it’, ‘how’, ‘further’, ‘was’, ‘here’, ‘than’}


class Index:

    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = stopwords_from_nltk.words()
    stemmer = PorterStemmer()

    def __init__(self):
        self._thread_lock = threading.Lock()
        self._doc_set = set()
        self._index_dict = {}
        self._index_queue = queue.Queue()

    def print(self, content):
        print(content)

    @staticmethod # A static method doesn't receive any reference argument whether it is called by an instance of a class or by the class itself
    def clean(content):
        tokens = Index.tokenizer.tokenize(content)
        tokens = [Index.stemmer.stem(i) for i in tokens if i not in Index.stop_words]
        return tokens

    def index(self, document_id, content):
        tokens = Index.clean(content) # remove ? ! . , and stopwords
        token_set = set(tokens)
        for token in token_set:
            token_count = tokens.count(token)
            self._update_inverted_index(token, document_id, token_count)
        self._doc_set.add(document_id)
        return

    def _update_inverted_index(self, token, document, count):
        if token not in self._index_dict:
            with self._thread_lock:
                self._index_dict[token] = {
                    'count': count,
                    'frequency': {document: count}
                }
        else:
            with self._thread_lock:
                self._index_dict[token]['frequency'][document] = count
                self._index_dict[token]['count'] += count

    def get_documents_containing_word(self, token, count=None, text_=True):
        token = Index.clean(token)
        if len(token) == 0:
            return []
        token = token[0]
        docs = self._index_dict.get(token, {'frequency': {}})['frequency']
        #self.print(self._index_dict)
        sorted_docs = sorted(docs.items(), key=operator.itemgetter(1), reverse=False)
        doc_list = list(sorted_docs)
        return_doc_list = []
        for doc in doc_list:
            return_doc_list.append(doc + (self._text_from_file(doc[0]), ))

        if text_:
            return return_doc_list if count is None else return_doc_list[:count]
        else:
            return doc_list if count is None else doc_list[:count]


    def _text_from_file(self, path):
        with open(path) as f:
            return f.read()

    def bulk_index(self, doc_list, threads):
        for txt_item in doc_list:
            self.print('%s was added to queue' % txt_item[0])
            self._index_queue.put(txt_item)
        thread_list = []
        #self.print(threads)
        for i in range(threads):
            th = threading.Thread(target=self._index_worker)
            th.start()
            thread_list.append(th)
        for th in thread_list:
            th.join()

    def _index_worker(self):
        while True:
            try:
                doc_id, content = self._index_queue.get(timeout=0.1)
            except:
                return
            self.index(doc_id, content)
            self.print('%s docs left to process -  %s was indexed' % (self._index_queue.qsize(), doc_id))
