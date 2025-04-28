import json
import os
from twm import Text


class RuleProcessor:
    # в директории проекта должна быть папка rules, где хранятся правила
    directory_path = os.path.dirname(os.path.abspath(__file__))
    rules_path = os.path.join(directory_path, "rules")
    #правила распределены по частям речи, так их и загружаем в словарь с правилами
    pos_rules = dict()
    for file in os.scandir(rules_path):
        if file.name.endswith('.json'):
            with open(os.path.join(rules_path, file.name), 'r') as rule:
                pos_rules[file.name[:-5]] = json.load(rule)


    @staticmethod
    def find(text: Text, word_index: int, l_border: int, r_border: int, props) -> bool:
        # здесь пока будем считать что первым в props всегда будет передаваться ч.р.
        for i in range(max(word_index - l_border, 0), min(word_index + r_border + 1, len(text.words))):
            # нам не нужно смотреть изучаемое слово и не интересны слова неподходящей ч.р.
            if i == word_index or props[0] not in text.words[i].props.keys(): continue
            # если есть слово подходящей ч.р., мы перебираем варианты морф. свойств этого слова в качестве этой ч.р.
            for word_prop in text.words[i].props[props[0]]:
                # смотрим искомые св-ва, пропуская первое (ч.р.)
                for prop in props[1:]:
                    # если св-во не совпало, сразу пропускаем слово
                    if prop not in word_prop[0]: break
                # если доработал цикл, значит все данные св-ва совпали, значит нашли слово
                else:
                    return True
        # False если слово не нашли
        return False

    @staticmethod
    def process_rules(text: Text, word_i: int):
        # перебирает все возможные для слова наборы морф. св-в
        # перебирает правила для возможной ч.р. переданного слова и возвращает подошедшие морф. свойства слова
        # если хотя бы одно правило выполнилось, иначе возвращает None

        for pos in text.words[word_i].props.keys():
            for prop in text.words[word_i].props[pos]:
                for rule in RuleProcessor.pos_rules[pos]:
                    for sub_rule in rule:
                        rule_command = getattr(RuleProcessor, sub_rule[0])
                        rule_props = [getattr(prop[0], rule_prop[2:]) if rule_prop.startswith('x_') else rule_prop for rule_prop in sub_rule[1]["props"]]
                        if rule_command(text, word_i, sub_rule[1]["l_border"], sub_rule[1]["r_border"], rule_props):
                         return prop
        return None
