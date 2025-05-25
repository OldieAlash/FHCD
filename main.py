import twm, ruler
from textual_disambiguator import TextProcessor

#Демонстрация работы

#Просто считали текст и привели к формату twm.Text
txt = input()
text = twm.Text(txt)
for word in text.words:
    print(word.props)

print('А теперь снимем неоднозначности:')

#Засунули необработанный текст в обработчик текста, в том числе снимающий неоднозначности
text = TextProcessor.process_text(txt)
for word in text.words:
    print(word.props)