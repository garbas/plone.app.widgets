# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from mock import Mock
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.widgets.browser.vocabulary import VocabularyView
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.testing import ExampleVocabulary
from plone.app.widgets.testing import PLONEAPPWIDGETS_DX_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.autoform.interfaces import WIDGETS_KEY
from plone.dexterity.fti import DexterityFTI
from plone.testing.zca import UNIT_TESTING
from z3c.form.interfaces import IFieldWidget, IFormLayer
from z3c.form.widget import FieldWidget
from z3c.form.util import getSpecification
from zope import schema
from zope.component import provideUtility
from zope.component import provideAdapter
from zope.component.globalregistry import base
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.globalrequest import setRequest
from zope.schema import Date
from zope.schema import Datetime
from zope.schema import List
from zope.schema import Choice
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema import Set

import json

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


class BaseWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = TextLine(__name__='textlinefield')

    def test_widget_pattern_notimplemented(self):
        from plone.app.widgets.dx import BaseWidget
        from plone.app.widgets.utils import NotImplemented

        widget = BaseWidget(self.request)
        widget.field = self.field

        self.assertRaises(
            NotImplemented,
            widget._base_args)

        widget.pattern = 'example'

        self.assertEqual(
            {
                'pattern': 'example',
                'pattern_options': {}
            },
            widget._base_args())

    def test_widget_base_notimplemented(self):
        from plone.app.widgets.dx import BaseWidget
        from plone.app.widgets.base import InputWidget
        from plone.app.widgets.utils import NotImplemented

        widget = BaseWidget(self.request)
        widget.field = self.field
        widget.pattern = 'example'

        self.assertRaises(
            NotImplemented,
            widget.render)

        widget._base = InputWidget

        self.assertEqual(
            '<input class="pat-example" type="text"/>',
            widget.render())


class DateWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DateWidget

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Date(__name__='datefield')
        self.widget = DateWidget(self.request)
        self.widget.field = self.field
        self.widget.pattern_options = {'date': {'firstDay': 0}}

    def test_widget(self):
        self.assertEqual(
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': None,
                'pattern_options': {
                    'date': {
                        'firstDay': 0,
                        'min': [1914, 1, 1],
                        'max': [2034, 1, 1],
                        'clear': u'Clear',
                        'format': 'mmmm d, yyyy',
                        'monthsFull': [u'January', u'February', u'March',
                                       u'April', u'May', u'June', u'July',
                                       u'August', u'September', u'October',
                                       u'November', u'December'],
                        'weekdaysShort': [u'Sun', u'Mon', u'Tue', u'Wed',
                                          u'Thu', u'Fri', u'Sat'],
                        'weekdaysFull': [u'Sunday', u'Monday', u'Tuesday',
                                         u'Wednesday', u'Thursday', u'Friday',
                                         u'Saturday'],
                        'today': u'Today',
                        'selectYears': 200,
                        'placeholder': u'Enter date...',
                        'monthsShort': [u'Jan', u'Feb', u'Mar', u'Apr', u'May',
                                        u'Jun', u'Jul', u'Aug', u'Sep', u'Oct',
                                        u'Nov', u'Dec']
                    },
                    'time': False
                }
            },
            self.widget._base_args(),
        )

    def test_data_converter(self):
        from plone.app.widgets.dx import DateWidgetConverter
        converter = DateWidgetConverter(self.field, self.widget)

        self.assertEqual(
            converter.field.missing_value,
            converter.toFieldValue(''),
        )

        self.assertEqual(
            date(2000, 10, 30),
            converter.toFieldValue('2000-10-30'),
        )

        self.assertEqual(
            date(21, 10, 30),
            converter.toFieldValue('21-10-30'),
        )

        self.assertEqual(
            '',
            converter.toWidgetValue(converter.field.missing_value),
        )

        self.assertEqual(
            '2000-10-30',
            converter.toWidgetValue(date(2000, 10, 30)),
        )

        self.assertEqual(
            '21-10-30',
            converter.toWidgetValue(date(21, 10, 30)),
        )


class DatetimeWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DatetimeWidget

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Datetime(__name__='datetimefield')
        self.widget = DatetimeWidget(self.request)
        self.widget.pattern_options = {'date': {'firstDay': 0}}

    def test_widget(self):
        self.assertEqual(
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': None,
                'pattern_options': {
                    'date': {
                        'firstDay': 0,
                        'min': [1914, 1, 1],
                        'max': [2034, 1, 1],
                        'clear': u'Clear',
                        'format': 'mmmm d, yyyy',
                        'monthsFull': [u'January', u'February', u'March',
                                       u'April', u'May', u'June', u'July',
                                       u'August', u'September', u'October',
                                       u'November', u'December'],
                        'weekdaysShort': [u'Sun', u'Mon', u'Tue', u'Wed',
                                          u'Thu', u'Fri', u'Sat'],
                        'weekdaysFull': [u'Sunday', u'Monday', u'Tuesday',
                                         u'Wednesday', u'Thursday', u'Friday',
                                         u'Saturday'],
                        'today': u'Today',
                        'selectYears': 200,
                        'placeholder': u'Enter date...',
                        'monthsShort': [u'Jan', u'Feb', u'Mar', u'Apr', u'May',
                                        u'Jun', u'Jul', u'Aug', u'Sep', u'Oct',
                                        u'Nov', u'Dec']
                    },
                    'time': {
                        'placeholder': u'Enter time...',
                        'today': u'Today',
                        'format': 'h:i a'
                    }
                }
            },
            self.widget._base_args(),
        )

    def test_data_converter(self):
        from plone.app.widgets.dx import DatetimeWidgetConverter
        converter = DatetimeWidgetConverter(self.field, self.widget)

        self.assertEqual(
            converter.toFieldValue(''),
            converter.field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('2000-10-30 15:40'),
            datetime(2000, 10, 30, 15, 40),
        )

        self.assertEqual(
            converter.toFieldValue('21-10-30 15:40'),
            datetime(21, 10, 30, 15, 40),
        )

        self.assertEqual(
            converter.toWidgetValue(converter.field.missing_value),
            '',
        )

        self.assertEqual(
            converter.toWidgetValue(datetime(2000, 10, 30, 15, 40)),
            '2000-10-30 15:40',
        )

        self.assertEqual(
            converter.toWidgetValue(datetime(21, 10, 30, 15, 40)),
            '21-10-30 15:40',
        )

    def test_data_converter_timezone(self):
        from plone.app.widgets.dx import DatetimeWidgetConverter
        context = Mock()

        # Test for previously set datetime, without tzinfo and no timezone on
        # context.
        # Should not apply a timezone to the field value.
        dt = datetime(2013, 11, 13, 10, 20)
        setattr(context, self.field.getName(), dt)
        self.widget.context = context
        converter = DatetimeWidgetConverter(self.field, self.widget)
        self.assertEqual(
            converter.toFieldValue('2013-11-13 10:20'),
            datetime(2013, 11, 13, 10, 20),
        )

        # Test for previously set datetime, with tzinfo but no timezone on
        # context.
        # Should apply UTZ zone to field value, to be able to be compared with
        # the timezone aware datetime from the context.
        import pytz
        nl = pytz.timezone('Europe/Amsterdam')
        dt = nl.localize(datetime(2013, 11, 13, 10, 20))
        setattr(context, self.field.getName(), dt)
        context.timezone = None
        self.widget.context = context
        converter = DatetimeWidgetConverter(self.field, self.widget)
        self.assertEqual(
            converter.toFieldValue('2013-11-13 10:20'),
            pytz.utc.localize(datetime(2013, 11, 13, 10, 20)),
        )

        # Test for previously set datetime, with tzinfo and timezone one
        # context.
        # Should apply the zone based on "timezone" value to field value, to be
        # able to be CORRECTLY compared with the timezone aware datetime from
        # the context.
        nl = pytz.timezone('Europe/Amsterdam')
        dt = nl.localize(datetime(2013, 11, 13, 10, 20))
        setattr(context, self.field.getName(), dt)
        context.timezone = "Europe/Amsterdam"
        self.widget.context = context
        converter = DatetimeWidgetConverter(self.field, self.widget)
        self.assertEqual(
            converter.toFieldValue('2013-11-13 10:20'),
            nl.localize(datetime(2013, 11, 13, 10, 20)),
        )

        # cleanup
        self.widget.context = None


class SelectWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        alsoProvides(self.request, IFormLayer)

        # ITerms Adapters are needed for data converter
        from z3c.form import term
        import zope.component
        zope.component.provideAdapter(term.CollectionTerms)
        zope.component.provideAdapter(term.CollectionTermsVocabulary)
        zope.component.provideAdapter(term.CollectionTermsSource)

    def tearDown(self):
        from z3c.form import term
        base.unregisterAdapter(term.CollectionTerms)
        base.unregisterAdapter(term.CollectionTermsVocabulary)
        base.unregisterAdapter(term.CollectionTermsSource)

    def test_widget(self):
        from plone.app.widgets.dx import SelectWidget
        widget = SelectWidget(self.request)
        widget.field = Choice(
            __name__='selectfield',
            values=['one', 'two', 'three']
        )
        widget.terms = widget.field.vocabulary
        self.assertEqual(
            {
                'multiple': False,
                'name': None,
                'pattern_options': {},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

        widget.multiple = True
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {'separator': ';', 'multiple': True},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

        widget.value = 'one'
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {'separator': ';', 'multiple': True},
                'pattern': 'select2',
                'value': ('one'),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

    def test_widget_list_orderable(self):
        from plone.app.widgets.dx import SelectWidget
        widget = SelectWidget(self.request)
        widget.separator = '.'
        widget.field = List(
            __name__='selectfield',
            value_type=Choice(values=['one', 'two', 'three'])
        )
        widget.terms = widget.field.value_type.vocabulary
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {'orderable': True, 'multiple': True,
                                    'separator': '.'},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

    def test_widget_tuple_orderable(self):
        from plone.app.widgets.dx import SelectWidget
        widget = SelectWidget(self.request)
        widget.field = Tuple(
            __name__='selectfield',
            value_type=Choice(values=['one', 'two', 'three'])
        )
        widget.terms = widget.field.value_type.vocabulary
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {'orderable': True, 'multiple': True,
                                    'separator': ';'},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

    def test_widget_set_not_orderable(self):
        from plone.app.widgets.dx import SelectWidget
        widget = SelectWidget(self.request)
        # A set is not orderable
        widget.field = Set(
            __name__='selectfield',
            value_type=Choice(values=['one', 'two', 'three'])
        )
        widget.terms = widget.field.value_type.vocabulary
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {'multiple': True, 'separator': ';'},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

    def test_widget_extract(self):
        from plone.app.widgets.dx import SelectWidget
        widget = SelectWidget(self.request)
        widget.field = Choice(
            __name__='selectfield',
            values=['one', 'two', 'three']
        )
        widget.name = 'selectfield'
        self.request.form['selectfield'] = 'one'
        self.assertEquals(widget.extract(), ('one',))
        widget.multiple = True
        self.request.form['selectfield'] = 'one;two'
        self.assertEquals(widget.extract(), ('one;two', ))

    def test_data_converter_list(self):
        from plone.app.widgets.dx import SelectWidget
        from plone.app.widgets.dx import SelectWidgetConverter

        field = List(__name__='listfield',
                     value_type=Choice(__name__='selectfield',
                                       values=['one', 'two', 'three']))
        widget = SelectWidget(self.request)
        widget.field = field
        widget.multiple = True
        converter = SelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue(''),
            field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('one;two;three'),
            ['one', 'two', 'three'],
        )

        self.assertEqual(
            converter.toWidgetValue([]),
            [],
        )

        widget.separator = ','
        self.assertEqual(
            converter.toFieldValue('one,two,three'),
            ['one', 'two', 'three'],
        )
        self.assertRaises(
            LookupError,
            converter.toFieldValue, 'one;two;three'
        )

        self.assertEqual(
            converter.toWidgetValue(['one', 'two', 'three']),
            ['one', 'two', 'three']
        )

    def test_data_converter_tuple(self):
        from plone.app.widgets.dx import SelectWidget
        from plone.app.widgets.dx import SelectWidgetConverter

        field = Tuple(__name__='tuplefield',
                      value_type=Choice(__name__='selectfield',
                                        values=['one', 'two', 'three']))
        widget = SelectWidget(self.request)
        widget.field = field
        widget.multiple = True
        converter = SelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue(''),
            field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('one;two;three'),
            ('one', 'two', 'three'),
        )

        self.assertEqual(
            converter.toWidgetValue(tuple()),
            [],
        )

        self.assertEqual(
            converter.toWidgetValue(('one', 'two', 'three')),
            ['one', 'two', 'three'],
        )

    def test_data_converter_handles_empty_value(self):
        from plone.app.widgets.dx import SelectWidget
        from plone.app.widgets.dx import SelectWidgetConverter

        field = Tuple(__name__='tuplefield',
                      value_type=Choice(__name__='selectfield',
                                        values=['one', 'two', 'three']))
        widget = SelectWidget(self.request)
        widget.field = field
        widget.multiple = True
        converter = SelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue((u'',)),
            field.missing_value,
        )


class AjaxSelectWidgetTests(unittest.TestCase):

    layer = UNIT_TESTING
    maxDiff = None

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        provideUtility(ExampleVocabulary(), name=u'example')

    def test_widget(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        widget = AjaxSelectWidget(self.request)
        widget.update()
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {'separator': ';'},
            },
            widget._base_args()
        )

        widget.vocabulary = 'example'
        self.assertEqual(
            widget._base_args(),
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {
                    'vocabularyUrl': '/@@getVocabulary?name=example',
                    'separator': ';'
                },
            }
        )

        widget.value = 'three;two'
        self.assertEqual(
            widget._base_args(),
            {
                'name': None,
                'value': 'three;two',
                'pattern': 'select2',
                'pattern_options': {
                    'vocabularyUrl': '/@@getVocabulary?name=example',
                    'initialValues': {'three': u'Three', 'two': u'Two'},
                    'separator': ';'
                },
            }
        )

    def test_widget_list_orderable(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        widget = AjaxSelectWidget(self.request)
        widget.field = List(__name__='selectfield')
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {'orderable': True, 'separator': ';'},
            },
            widget._base_args(),
        )

    def test_widget_tuple_orderable(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        widget = AjaxSelectWidget(self.request)
        widget.field = Tuple(__name__='selectfield')
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {'orderable': True, 'separator': ';'},
            },
            widget._base_args(),
        )

    def test_widget_set_not_orderable(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        widget = AjaxSelectWidget(self.request)
        # A set is not orderable
        widget.field = Set(__name__='selectfield')
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {'separator': ';'},
            },
            widget._base_args(),
        )

    def test_widget_addform_url_on_addform(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        widget = AjaxSelectWidget(self.request)
        form = Mock()
        from zope.interface import directlyProvides
        from z3c.form.interfaces import IAddForm
        directlyProvides(form, IAddForm)
        form.request = {'URL': 'http://addform_url'}
        widget.form = form
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {'separator': ';'},
            },
            widget._base_args(),
        )
        widget.vocabulary = 'vocabulary1'
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'select2',
                'pattern_options': {
                    'separator': ';',
                    'vocabularyUrl':
                    'http://addform_url/@@getVocabulary?name=vocabulary1'}

            },
            widget._base_args(),
        )

    def test_data_converter_list(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        from plone.app.widgets.dx import AjaxSelectWidgetConverter

        field = List(__name__='listfield', value_type=TextLine())
        widget = AjaxSelectWidget(self.request)
        widget.field = field
        converter = AjaxSelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue(''),
            field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('123;456;789'),
            ['123', '456', '789'],
        )

        self.assertEqual(
            converter.toWidgetValue([]),
            None,
        )

        self.assertEqual(
            converter.toWidgetValue(['123', '456', '789']),
            '123;456;789',
        )

    def test_data_converter_tuple(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        from plone.app.widgets.dx import AjaxSelectWidgetConverter

        field = Tuple(__name__='tuplefield', value_type=TextLine())
        widget = AjaxSelectWidget(self.request)
        widget.field = field
        converter = AjaxSelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue(''),
            field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('123;456;789'),
            ('123', '456', '789'),
        )

        self.assertEqual(
            converter.toWidgetValue(tuple()),
            None,
        )

        self.assertEqual(
            converter.toWidgetValue(('123', '456', '789')),
            '123;456;789',
        )


class QueryStringWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

    def test_widget(self):
        from plone.app.widgets.dx import QueryStringWidget
        widget = QueryStringWidget(self.request)
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'querystring',
                'pattern_options': {
                    'indexOptionsUrl': '/@@qsOptions',
                    'previewCountURL': '/@@querybuildernumberofresults',
                    'previewURL': '/@@querybuilder_html_results',
                },
            },
            widget._base_args()
        )


class RelatedItemsWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

    def test_widget(self):
        from plone.app.widgets.dx import RelatedItemsWidget
        context = Mock(absolute_url=lambda: 'fake_url')
        context.portal_properties.site_properties\
            .getProperty.return_value = ['SomeType']
        widget = RelatedItemsWidget(self.request)
        widget.context = context
        widget.update()
        self.assertEqual(
            {
                'name': None,
                'value': u'',
                'pattern': 'relateditems',
                'pattern_options': {
                    'folderTypes': ['SomeType'],
                    'separator': ';',
                    'vocabularyUrl': '/@@getVocabulary?name='
                                     'plone.app.vocabularies.Catalog',
                },
            },
            widget._base_args()
        )


def add_mock_fti(portal):
    # Fake DX Type
    fti = DexterityFTI('dx_mock')
    portal.portal_types._setObject('dx_mock', fti)
    fti.klass = 'plone.dexterity.content.Item'
    fti.schema = 'plone.app.widgets.tests.test_dx.IMockSchema'
    fti.filter_content_types = False
    fti.behaviors = ('plone.app.dexterity.behaviors.metadata.IBasic',)


def _custom_field_widget(field, request):
    from plone.app.widgets.dx import AjaxSelectWidget
    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = 'plone.app.vocabularies.PortalTypes'
    return widget


def _enable_custom_widget(field):
    provideAdapter(_custom_field_widget, adapts=
                   (getSpecification(field), IWidgetsLayer),
                   provides=IFieldWidget)


def _disable_custom_widget(field):
        base.unregisterAdapter(
            required=(getSpecification(field), IWidgetsLayer,),
            provided=IFieldWidget)


class IMockSchema(Interface):
    allowed_field = schema.Choice(
        vocabulary='plone.app.vocabularies.PortalTypes')
    disallowed_field = schema.Choice(
        vocabulary='plone.app.vocabularies.PortalTypes')
    default_field = schema.Choice(
        vocabulary='plone.app.vocabularies.PortalTypes')
    custom_widget_field = schema.TextLine()
    adapted_widget_field = schema.TextLine()

IMockSchema.setTaggedValue(WRITE_PERMISSIONS_KEY, {
    'allowed_field': u'zope2.View',
    'disallowed_field': u'zope2.ViewManagementScreens',
    'custom_widget_field': u'zope2.View',
    'adapted_widget_field': u'zope2.View',
    })
IMockSchema.setTaggedValue(WIDGETS_KEY, {
    'custom_widget_field': _custom_field_widget,
    })


class DexterityVocabularyPermissionTests(unittest.TestCase):

    layer = PLONEAPPWIDGETS_DX_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)
        self.portal = self.layer['portal']

        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        add_mock_fti(self.portal)
        self.portal.invokeFactory('dx_mock', 'test_dx')

        self.portal.test_dx.manage_permission('View',
                                              ('Anonymous',),
                                              acquire=False)
        self.portal.test_dx.manage_permission('View management screens',
                                              (),
                                              acquire=False)
        self.portal.test_dx.manage_permission('Modify portal content',
                                              ('Editor', 'Manager',
                                               'Site Adiminstrator'),
                                              acquire=False)

    def test_vocabulary_field_allowed(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'allowed_field',
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))

    def test_vocabulary_field_wrong_vocabulary_disallowed(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.Fake',
            'field': 'allowed_field',
        })
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def test_vocabulary_field_disallowed(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'disallowed_field',
        })
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def test_vocabulary_field_default_permission(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'default_field',
        })
        # If the field is does not have a security declaration, the
        # default edit permission is tested (Modify portal content)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

        setRoles(self.portal, TEST_USER_ID, ['Editor'])
        # Now access should be allowed, but the vocabulary does not exist
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))

    def test_vocabulary_field_default_permission_wrong_vocab(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.Fake',
            'field': 'default_field',
        })
        setRoles(self.portal, TEST_USER_ID, ['Editor'])
        # Now access should be allowed, but the vocabulary does not exist
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def test_vocabulary_missing_field(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'missing_field',
        })
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        with self.assertRaises(AttributeError):
            view()

    def test_vocabulary_on_widget(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'custom_widget_field',
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))
        self.request.form['name'] = 'plone.app.vocabularies.Fake'
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def test_vocabulary_on_adapted_widget(self):
        _enable_custom_widget(IMockSchema['adapted_widget_field'])
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'adapted_widget_field',
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))

        self.request.form['name'] = 'plone.app.vocabularies.Fake'
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')
        _disable_custom_widget(IMockSchema['adapted_widget_field'])
