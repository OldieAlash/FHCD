import json, os

import twm
from twm import Text


class RuleProcessor:
    '''в директории проекта должна быть папка rules, где хранятся правила'''
    directory_path = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(directory_path, "rules")
    '''правила распределены по частям речи, так их и загружаем в словарь с правилами'''
    pos_rules = dict()
    for file in os.scandir(rules_path):
        if file.name.endswith('.json'):
            with open(os.path.join(rules_path, file.name), 'r', encoding='utf-8') as rule:
                pos_rules[file.name[:-5]] = json.load(rule)


    @staticmethod
    def find(text: Text, word_i: int, l_border: int, r_border: int, props) -> bool:
        # ТУТ У МН ЧИСЛА ПРИЛАГАТЕЛЬНЫХ НЕТ РОДА ПОЭТОМУ ГРАМЕМА ПЕРЕДАЕТСЯ NONE
        # НУЖНО ИЛИ ПРОВЕРЯТЬ НА NONE ИЛИ ИГНОРИРОВАТЬ
        '''в props должны приходить искомые морф св-ва, первым св-вом - ч.р.
        если св-во начинается с x_, то оно совпадает с таким же у изучаемого слова'''
        # props = [getattr(text.words[word_i], prop[2:]) if prop.startswith('x_') else prop for prop in props]
        for i in range(max(word_i - l_border, 0), min(word_i + r_border + 1, len(text.words))):
            '''нам не нужно смотреть изучаемое слово и не интересны слова неподходящей ч.р.'''
            if i == word_i or props[0] not in text.words[i].props.keys(): continue
            # if i == word_i or twm.homonymy_groups[props[0]] not in text.words[i].props.keys(): continue
            '''если есть слово подходящей ч.р.,
            мы перебираем варианты морф. свойств этого слова в качестве этой ч.р.'''
            for word_prop in text.words[i].props[props[0]]:
            # for word_prop in text.words[i].props[twm.homonymy_groups[props[0]]]:
                '''смотрим искомые св-ва, пропуская первое (ч.р.)'''
                for prop in props[1:]:
                    '''если св-во не совпало, сразу пропускаем слово'''
                    if prop and prop not in word_prop[0]: break
                    '''если доработал цикл, значит все данные св-ва совпали, значит нашли слово'''
                else: return True
        '''False если слово не нашли'''
        return False

    @staticmethod
    def find_w(text: Text, word_i: int, l_border: int, r_border: int, props) -> bool:
        '''считаем, что в props лежат искомые слова'''
        for i in range(max(word_i - l_border, 0), min(word_i + r_border + 1, len(text.words))):
            if i == word_i: continue
            if text.words[i].word in props:
                return True
        '''Если дошли до конца цикла, то нужных слов не нашлось'''
        return False

    @staticmethod
    def n_find(text: Text, word_i: int, l_border: int, r_border: int, props) -> bool:
        '''неэлегантная проверка отсутствия слова с заданными морф. свойствами'''
        return not RuleProcessor.find(text, word_i, l_border, r_border, props)

    @staticmethod
    def n_find_w(text: Text, word_i: int, l_border: int, r_border: int, props) -> bool:
        '''неэлегантная проверка отсутствия заданных слов'''
        return not RuleProcessor.find_w(text, word_i, l_border, r_border, props)

    @staticmethod
    def find_punct(text: Text, word_i: int, l_border: int, r_border: int, props) -> bool:
        '''считаем, что в props лежат искомые знаки пунктуации'''
        '''тут не учитываются случаи когда исследуемое слово слишном близко к краям
        потом добавлю обработку таких случаев'''
        if word_i - l_border >= 0 and word_i + r_border < len(text.words):
            return text.words[word_i - l_border].l_punct == props[0] and text.words[word_i + r_border].r_punct == props[1]
        return False

    @staticmethod
    def process_rules(text: Text, word_i: int):
        ''' перебирает все возможные для слова наборы морф. св-в
        перебирает правила для возможной ч.р. переданного слова и возвращает подошедшие морф. свойства слова
        если хотя бы одно правило выполнилось, иначе возвращает None'''

        for pos in text.words[word_i].props.keys():
            for prop in text.words[word_i].props[pos]:
                for rule in RuleProcessor.pos_rules.get(pos, []):
                    for sub_rule in rule:
                        rule_command = getattr(RuleProcessor, sub_rule[0])
                        '''в props для find могут быть искомые морф св-ва
                                если св-во начинается с x_, то оно совпадает с таким же у изучаемого слова'''
                        rule_props = [getattr(prop[0], rule_prop[2:]) if rule_prop.startswith('x_') else rule_prop for rule_prop in sub_rule[1]["props"]]
                        '''пока что подправила предполгают, что они выполняются вместе последовательно
                        если выполнились все, то морф св-ва подходят и правило выполнилось
                        если какое-то подправило не выполнилось, считаем что правило не выполнилось целиком
                        и переходим к следующему'''
                        if not rule_command(text, word_i, sub_rule[1]["l_border"], sub_rule[1]["r_border"], rule_props):
                            break
                    else:
                        return prop
        return None
