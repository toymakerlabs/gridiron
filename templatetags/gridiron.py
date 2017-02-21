from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
#http://stackoverflow.com/questions/35054230/django-did-you-forget-to-register-or-load-this-tag
#http://stackoverflow.com/questions/22733510/django-custom-templatetag-which-is-preferred-rendering-a-template-or-populating
#http://stackoverflow.com/questions/6816907/django-custom-template-tag-passing-variable-number-of-arguments
#http://stackoverflow.com/questions/3085382/python-how-can-i-strip-first-and-last-double-quotes


register = template.Library()

"""
RIP quotes.
"""
def dequote(s):
    if s == '' or s == None:
        return s

    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]


"""
Take token bits and return two lists, one for positional arguments and one
for keyword args. Optionally include kw params to check against.
"""
def parse_tag_arguments(parser,bits,required=False,params_accepted=None):
    kwargs = {}
    positional_args = []
    #lifted this from parse_bits in template.library
    for bit in bits:
        # First we try to extract a potential kwarg from the bit
        print (bit)
        #if not quotes, we're looking at a vararg

        kwarg = template.base.token_kwargs([bit], parser)
        if kwarg:
            # The kwarg was successfully extracted
            param, value = kwarg.popitem()
            if not params_accepted==None:
                if param not in params_accepted:
                    # An unexpected keyword argument was supplied
                    raise template.exceptions.TemplateSyntaxError(
                        "received unexpected keyword argument '%s'" %
                        (param))
                elif param in kwargs:
                    # The keyword argument has already been supplied once
                    raise template.exceptions.TemplateSyntaxError(
                        "received multiple values for keyword argument '%s'" %
                        (param))
                else:
                    # All good, record the keyword argument
                    kwargs[str(param)] = value.var
        else:
            if kwargs:
                raise template.exceptions.TemplateSyntaxError(
                    "received some positional argument(s) after some "
                    "keyword argument(s)")
            else:
                positional_args.append(parser.compile_filter(bit).var)

    if required and len(positional_args) <1:
        raise template.exceptions.TemplateSyntaxError(
            "must include at least one responsive column value")
    return positional_args,kwargs




@register.tag(name='grid_row')
def do_grid_row(parser, token):
    nodelist = parser.parse(('endrow',))
    parser.delete_first_token()
    bits = token.split_contents()[1:]
    p_args, kwargs = parse_tag_arguments(parser,bits,False,['id','classname'])

    return GridRowNode(nodelist,*p_args,**kwargs)

class GridRowNode(template.Node):
    def __init__(self, nodelist, *args,**kwargs):
        self.nodelist = nodelist
        self.id = kwargs.get('id','')
        self.classname = kwargs.get('classname','')


    def render(self, context):
        try:
            self.classname = self.classname.resolve(context)
        except AttributeError:
            pass
        output = self.nodelist.render(context)
        #something = '<div class="mdl-grid">%s</div>' % (output)
        return render_to_string('gridiron/grid_row.html',{'content': output,'id':self.id,'classname':self.classname})
        #return mark_safe(something)





@register.tag(name='grid_column')
def do_grid_column(parser, token):
    nodelist = parser.parse(('endcol',))
    parser.delete_first_token()
    bits = token.split_contents()[1:]
    p_args, kwargs = parse_tag_arguments(parser,bits,True,['id','classname'])

    return GridColumnNode(nodelist,*p_args,**kwargs)

class GridColumnNode(template.Node):
    def __init__(self, nodelist, *args,**kwargs):
        self.nodelist = nodelist
        self.columns = []
        self.id = kwargs.get('id','')
        self.classname = kwargs.get('classname','')
        #import pdb;pdb.set_trace()
        for col in args:
            self.columns.append(col.var)

    def render(self, context):
        output = self.nodelist.render(context)
        #something = '<div class="mdl-grid">%s</div>' % (output)
        return render_to_string('gridiron/grid_column.html',{'content': output,'columns':self.columns,'id':self.id,'classname':self.classname})
        #return mark_safe(something)









# @register.tag(name='upper')
# def do_upper(parser, token):
#     nodelist = parser.parse(('endupper',))
#     parser.delete_first_token()
#     return UpperNode(nodelist)
#
# class UpperNode(template.Node):
#     def __init__(self, nodelist):
#         self.nodelist = nodelist
#     def render(self, context):
#         output = self.nodelist.render(context)
#         return output.upper()
    #     something = '<h1>%s</h1><p>%s</p>' % (title, content)
    # return mark_safe(something)
