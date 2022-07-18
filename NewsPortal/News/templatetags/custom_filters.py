from django import template
import pymorphy2

register = template.Library()

@register.filter(name='censor')
def censor(text: str, censor_word=['спецоперации', 'релокации', 'компания', 'Россия']) -> str:
    words = text.split()
    for i in range(len(words)):
        if normalized_word(words[i].lower()) in censor_word:
            words[i] = "*" * len(words[i])
    return " ".join(words)

def normalized_word(word:str):
    word.strip()
    morph = pymorphy2.MorphAnalyzer()
    return morph.parse(word)[0].normal_form
