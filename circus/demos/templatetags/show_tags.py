from django import template

from ..models import Rating


def do_if_rated(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError('%s tag takes two arguments ' % bits[0])
    nodelist_true = parser.parse(('else', 'endif_rated'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_rated', ))
        parser.delete_first_token()
    else:
        nodelist_false = template.Nodelist()
    return IfRatedNode(bits[1], bits[2], nodelist_true, nodelist_false)


class IfRatedNode(template.Node):

    def __init__(self, user, show, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.user = template.Variable(user)
        self.show = template.Variable(show)

    def render(self, context):
        try:
            user = self.user.resolve(context)
            show = self.show.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if Rating.objects.filter(user__pk=user.id, show__pk=show.id):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

register = template.Library()
register.tag('if_rated', do_if_rated)
