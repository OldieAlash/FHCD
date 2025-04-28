import twm, ruler

text = twm.Text(input())
changes = 1
while changes > 0:
    changes = 0
    for word_i in range(len(text.words)):
        if text.words[word_i].is_homonymous and (prop := ruler.RuleProcessor.process_rules(text, word_i)):
            text.words[word_i].props = {prop[0].POS: prop}
            text.words[word_i].is_homonymous = False
            changes += 1

for word in text.words:
    print(word.props)