from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.interface import IATContentType
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.at import ChosenWidget
from plone.app.widgets.at import ChosenAjaxWidget
from plone.app.widgets.at import BootstrapDatepickerWidget


class ATWidgetsExtender(object):
    """ change any content...
    """
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    adapts(IATContentType)
    layer = IWidgetsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        if 'subject' in schema:
            subject = schema['subject']
            subject_widget = subject.widget
            subject.widget = ChosenWidget(
                label=subject_widget.label,
                description=subject_widget.description,
                js_options={
                    'allow_add_new': True,
                    'no_results_text': 'No results. Press enter to add',
                    'allow_sortable': True
                })
            subject.vocabulary_factory = 'plone.app.vocabularies.Keywords'

        for fieldname in ['contributors', 'creators']:
            if fieldname in schema:
                field = schema[fieldname]
                widget = field.widget
                field.widget = ChosenAjaxWidget(
                    label=widget.label,
                    description=widget.description,
                    ajax_rel_url='widget-user-query'
                )
        if 'customViewFields' in schema:
            field = schema['customViewFields']
            widget = field.widget
            field.widget = ChosenWidget(
                label=widget.label,
                description=widget.description,
                js_options={
                    'allow_sortable': True
                }
            )

        if 'relatedItems' in schema:
            field = schema['relatedItems']
            widget = field.widget
            field.widget = ChosenAjaxWidget(
                label=widget.label,
                description=widget.description,
                ajax_rel_url='widget-catalog-query'
            )

        if 'effectiveDate' in schema:
            field = schema['effectiveDate']
            widget = field.widget
            field.widget = BootstrapDatepickerWidget(
                label=widget.label,
                description=widget.description
            )

        if 'expirationDate' in schema:
            field = schema['expirationDate']
            widget = field.widget
            field.widget = BootstrapDatepickerWidget(
                label=widget.label,
                description=widget.description
            )