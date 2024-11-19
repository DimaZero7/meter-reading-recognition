from django.utils.translation import gettext_lazy as _


class SearchHelpTextMixin:
    @property
    def search_help_text(self):
        fields = ", ".join(self.search_fields)
        help_text = _("search fields: {fields}").format(fields=fields)
        return help_text
