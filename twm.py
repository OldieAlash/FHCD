import pymorphy2
import string

morph = pymorphy2.MorphAnalyzer()

'''СЛОВАРЬ ОМОНИМИЧНЫХ СИТУАЦИЙ ВВЕДЁН ДЛЯ РЕАЛИЗАЦИИ ОПИСАННЫХ В ИСТОЧНИКАХ ПРАВИЛ. ОНИ РАБОТАЮТ С ТОЧНОСТЬЮ ДО ГРУПП,
ПРИШЛОСЬ ПЕРЕЙТИ В ЭТУ НОТАЦИЮ'''

homonymy_groups = {"NOUN" : "N", "ADJF" : "A", "ADJS" : "ABR", "COMP" : "COMP", "VERB": "VF", "INFN": "VINF",
"PRTF": "A", "PRTS": "ABR", "GRND": "DV", "NUMR": "NNUM", "ADVB": "D", "NPRO": "N", "PRED": "PRED", "PREP": "P",
"CONJ": "CONJ", "PRCL": "CH", "INTJ": "MJD"}

class Word:
    def __init__(self, word:str, index: int, prev_lst_char):
        self.index = index
        '''сохраняем правый знак препинания от прошлого слова, если он есть
        в json нет None, поэтому неопределенный знак - '' '''
        self.l_punct = prev_lst_char if prev_lst_char in string.punctuation else ''
        '''если после разбиения текста по пробелам слово заканчивается знаком препинания,
        отсекаем его и записываем в отдельное поле'''
        self.r_punct, self.word = (word[-1], word[:-1]) if word[-1] in string.punctuation else ('', word)
        ''' в self.props хранятся возможные морф св-ва, отсортированные по ч.р: ключ-ч.р.,
        значение-список возможных наборов св-в'''
        self.props = dict()

        for morph_var in morph.parse(self.word):
            # self.props.setdefault(morph_var.tag.POS, []).append((morph_var.tag, morph_var.normal_form))
            self.props.setdefault(homonymy_groups[morph_var.tag.POS], []).append((morph_var.tag, morph_var.normal_form))
        self.is_homonymous = len(self.props.keys()) > 1


class Text:
    def __init__(self, text:str):
        '''сперва убираем пунктуацию (потом можно научиться обрабатывать текст,
        сохраняя пунктуацию, понадобится для правил'''
        #text_tmp = ''.join(filter(lambda x: x not in string.punctuation, text)).lower().split()
        #self.words = [Word(text_tmp[i], i, text_tmp[i-1][-1] if i > 0 else None) for i in range(len(text_tmp))]
        text_tmp = text.lower().split()
        '''при обработке, где нет слева знака препинания, считаем что этот символ - пустой '' '''
        self.words = [Word(text_tmp[i], i, text_tmp[i-1][-1] if i > 0 else '') for i in range(len(text_tmp))]
