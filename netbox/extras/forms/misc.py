from django import forms
from django.utils.translation import gettext_lazy as _

__all__ = (
    'RenderMarkdownForm',
)


class RenderMarkdownForm(forms.Form):
    """
    Provides basic validation for markup to be rendered.
    """
    text = forms.CharField(
        label=_('Text'),
        required=False,
        max_length=5000,
        error_messages={'max_length': _('Markdown previews are limited to 5,000 characters.')},
    )
