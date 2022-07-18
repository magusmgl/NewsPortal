from django import template

register = template.Library()
CENSOR_WORD = ['спецоперации', 'релокации', 'компании', 'россии', 'excel', 'яндекса']


@register.filter(name='censor')
def censor(value: str, censored_words=CENSOR_WORD) -> str:
    for word in map(lambda x: x.lower(), censored_words):
        value = value.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')

    for word in map(lambda x: x.capitalize(), censored_words):
        value = value.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')
    return value
