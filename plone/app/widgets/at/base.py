from lxml import etree
from Products.Archetypes.Widget import TypesWidget


class PatternsWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': "patterns_widgets",
        'input_type': 'input',
        'pattern': '',
        'pattern_options': {},
        'pattern_extra_options': {},
    })

    def view(self, context, field, request):
        return field.getAccessor(context)()

    def edit(self, context, field, request):
        value = field.getAccessor(context)()
        if value is None:
            value = ''

        if hasattr(self, 'formatAccessor'):
            value = self.formatAccessor(value)

        el = etree.Element(self.input_type)
        el.attrib['name'] = field.getName()

        if self.input_type == 'input':
            el.attrib['type'] = 'text'
            el.attrib['value'] = value
        elif self.input_type == 'textarea':
            el.text = value

        if self.pattern:
            el.attrib['data-pattern'] = self.pattern
            for option_name, options_value in self.pattern_options.items():
                attrib_name = 'data-%s-%s' % (self.pattern, option_name)
                if options_value.startswith('!'):
                    options_value = getattr(self, options_value[1:])
                    if callable(options_value):
                        options_value = options_value(context, request, field)

                el.attrib[attrib_name] = options_value
            for pattern_name in self.pattern_extra_options.keys():
                for option_name, options_value in \
                        self.pattern_extra_options[pattern_name].items():
                    attrib_name = 'data-%s-%s' % (pattern_name, option_name)
                    el.attrib[attrib_name] = options_value

        return etree.tostring(el)