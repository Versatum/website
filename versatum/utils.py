# coding: UTF-8


import os

from django import forms
from django.conf import settings
from django.shortcuts import render
from django.forms.utils import ErrorList
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.template.loader import get_template
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _



CHARS_ALLOWED = r'1234567890ABCDEFGHIJKLMNOPQRSTUVXWYZabcdefghijklmnopqrstuvxwyz'


def rename_image(instance, filename):
    return os.path.join(
        str(instance.__class__.__name__).lower(),
        '{0}.{1}'.format(
            get_random_string(length=16, allowed_chars=CHARS_ALLOWED),
            filename.split('.')[-1],
        )
    )


def enviar_email_html(para, assunto, template, dados, request,
    de=settings.DEFAULT_FROM_EMAIL, debug=False):

    if not isinstance(para, (list, tuple)):
        para = (para,)

    message = get_template(template).render(
        request=request, context=dados)
    msg = EmailMessage(assunto, message, to=para, from_email=de)
    msg.content_subtype = 'html'

    if not debug:
        msg.send()

    return message


class HandleError(object):
    info = {
        400: {
            'status': 400,
            'titulo': _(u'Invalid requisition'),
            'mensagem': _(u"Ops! The requested page is invalid..."),
        },
        403: {
            'status': 403,
            'titulo': _(u'Denied page'),
            'mensagem': _(u'Ops! Denied page access...'),
        },
        404: {
            'status': 404,
            'titulo': _(u'Page not found'),
            'mensagem': _(u"Ops! The page requested is not found..."),
        },
        500: {
            'status': 500,
            'titulo': _(u'Internal error'),
            'mensagem': _(u'Ops!An internal error occurred... '),
        }
    }

    template = "error.html"

    def __init__(self, status_code, template=None, dados=None, mensagem=None):
        self.status_code = status_code
        self.dados = dados or self.info.get(self.status_code)
        if template:
            self.template = template
        if mensagem:
            self.dados['mensagem'] = mensagem

    def __call__(self, request):
        return render(
            request=request,
            template_name=self.template,
            status=self.status_code,
            context=self.dados)
            #context_instance=render(request))


class ErrorListCSS(ErrorList):
    def __str__(self):
        return self.as_div()

    def as_ul(self):
        return self.as_div()

    def as_div(self):
        if not self:
            return ''
        return u'<div class="alert alert-danger">%s</div>' % u'\n'.join(
            [u'<p> %s </p>' % e for e in self]
        )


class BaseBootstrapForm(forms.BaseForm):
    error_css_class = 'has-error'
    required_css_class = 'form-group'

    def __init__(self, *args, **kwargs):
        args = list(args)

        if len(args) >= 6:
            args[5] = ErrorListCSS
        else:
            kwargs = {'error_class': ErrorListCSS}
            kwargs.update(kwargs)

        super(BaseBootstrapForm, self).__init__(
            *args, **kwargs
        )

        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs.setdefault('class', "form-control")
                if field.help_text:
                    field.widget.attrs.setdefault('title', field.help_text)

                if field.required:
                    field.widget.attrs.setdefault(
                        'placeholder',  _(u'Required field'))

    def __unicode__(self):
        return self.as_div()

    def __str__(self):
        return self.as_div()

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            # Escape and cache in local variable.
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors])
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    has_errors = ''

                    if bf_errors or (self.errors and '__all__' in self.errors):
                        has_errors = self.error_css_class

                    html_class_attr = u'class="%s %s"' % (css_classes, has_errors)

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % str(bf_errors))

                if bf.label:
                    label = conditional_escape(bf.label)
                    #label = bf.label_tag(label) or ''
                    label = u'<label class="control-label" for="id_%s"> %s </label>' % (
                        label.lower(), label
                    )
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': bf_errors,
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors': '',
                        'label': '',
                        'field': '',
                        'help_text': '',
                        'html_class_attr': html_class_attr,
                        'css_classes': '',
                        'field_name': '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))

    def as_div(self):
        return self._html_output(
            normal_row=u'''<div %(html_class_attr)s>
                        %(label)s
                        %(errors)s
                        %(field)s
                        %(help_text)s
                   </div>''',
            error_row=u'''<p> %s </p>''',
            row_ender=u'</div>',
            help_text_html=u'<p class="help-block">%s</p>',
            errors_on_separate_row=False)
