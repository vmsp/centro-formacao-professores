from crispy_forms import layout, utils
from django.utils import html as html_utils


class RadioWithOther(layout.LayoutObject):
    template = 'visprof/layout/radio_with_other.html'

    def __init__(self, field, other_field, *args, other_attrs=None, **kwargs):
        self.field = field
        self.other_field = other_field
        self.other_attrs = other_attrs or {}

        self.other_attrs.update({
            k.replace('_', '-'): html_utils.conditional_escape(v)
            for k, v in self.other_attrs.items()
        })

        if not hasattr(self, 'attrs'):
            self.attrs = {}
        else:
            self.attrs = self.attrs.copy()

        if 'css_class' in kwargs:
            if 'class' in self.attrs:
                self.attrs['class'] += ' %s' % kwargs.pop('css_class')
            else:
                self.attrs['class'] = kwargs.pop('css_class')

        self.wrapper_class = kwargs.pop('wrapper_class', None)
        self.template = kwargs.pop('template', self.template)

        self.attrs.update({
            k.replace('_', '-'): html_utils.conditional_escape(v)
            for k, v in kwargs.items()
        })

    def render(self,
               form,
               form_style,
               context,
               template_pack=layout.TEMPLATE_PACK,
               extra_context=None,
               **kwargs):
        # pylint: disable=too-many-arguments
        if extra_context is None:
            extra_context = {}
        if hasattr(self, 'wrapper_class'):
            extra_context['wrapper_class'] = self.wrapper_class

        extra_context['other_field'] = utils.render_field(
            self.other_field,
            form,
            form_style,
            context,
            attrs=self.other_attrs,
            template_pack=template_pack)

        return utils.render_field(self.field,
                                  form,
                                  form_style,
                                  context,
                                  self.template,
                                  attrs=self.attrs,
                                  template_pack=template_pack,
                                  extra_context=extra_context)
