import pymorphy2
import string

morph = pymorphy2.MorphAnalyzer()

class Word:
    def __init__(self, word:str, index: int):
        #в self.props хранятся возможные морф св-ва, отсортированные по ч.р: ключ-ч.р., значение-список возможных наборов св-в
        self.props = dict()
        self.word = word
        self.index = index

        for morph_var in morph.parse(word):
            self.props.setdefault(morph_var.tag.POS, []).append((morph_var.tag, morph_var.normal_form))

        self.is_homonymous = len(self.props.keys()) > 1


class Text:
    def __init__(self, text:str):
        # сперва убираем пунктуацию (потом можно научиться обрабатывать текст, сохраняя пунктуацию, понадобится для правил
        text_tmp = ''.join(filter(lambda x: x not in string.punctuation, text)).lower().split()
        self.words = [Word(text_tmp[i], i) for i in range(len(text_tmp))]
