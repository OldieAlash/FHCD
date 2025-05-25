import twm, ruler


class TextProcessor:
    # обрабатывает и хранит текст, может применять контекстные правила
    @staticmethod
    def contextual_disambiguation(text: twm.Text):
        disambiguated = True
        while disambiguated:
            disambiguated = False
            for word_i in range(len(text.words)):
                if text.words[word_i].is_homonymous and (prop := ruler.RuleProcessor.process_rules(text, word_i)):
                    # text.words[word_i].props = {prop[0].POS: [prop]}
                    text.words[word_i].props = {twm.homonymy_groups[prop[0].POS]: [prop]}
                    text.words[word_i].is_homonymous = False
                    disambiguated = True

    @staticmethod
    def process_text(text: str):
        text = twm.Text(text)
        TextProcessor.contextual_disambiguation(text)
        return text
