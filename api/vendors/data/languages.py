from django.utils.translation import gettext_lazy as _

LIST_OF_LANGUAGES = (
   ('en', _('English')),
   ('fr', _('France')),
   ('de', _('Germany')),
   ('ru', _('Russian')),
)
LIST_OF_LANGUAGE_CODES = [lang[0] for lang in LIST_OF_LANGUAGES]