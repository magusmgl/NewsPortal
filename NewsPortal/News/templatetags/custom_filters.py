from django import template

register = template.Library()

@register.filter()
def censor(text: str, censor_word=['спецоперации', 'релокации']) -> str:
    words = text.strip()
    for i in range(len(words)):
        if words[i] in censor_word or words[i] in map(lambda x: x.title(), censor_word):
            words[i] = "*" * len(words[i])
    return " ".join(words)











    return f'{text}'
