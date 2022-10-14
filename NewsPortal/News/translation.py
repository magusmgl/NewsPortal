from .models import Post, Category, Comment
from modeltranslation.translator import register, TranslationOptions

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', )

@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fieds = ('comment_text',)

