=====
Gridiron
=====

Gridiron is middleware for front-end grid systems.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. Create a folder called "gridiron" in your project, and add the folder structure "templates/gridiron"

3. Create grid_column.html and grid_row.html and add to this folder.

Grid Row:
<div {%if id %}id="{{id}}"{%endif%} class="mdl-grid {%if classname %}{{classname}}{%endif%}">
    {{content}}
</div>


Grid Column:
<div {%if id %}id="{{id}}"{%endif%} class="mdl-cell {% for col in columns %}mdl-cell--{{col}}-col {% endfor %}{%if classname %}{{classname}}{%endif%}">
    {{content}}
</div>


4. Edit the contents to reflect the grid system you're using. Example for Boostrap:

Grid Row:
<div {%if id %}id="{{id}}"{%endif%} class="row {%if classname %}{{classname}}{%endif%}">
    {{content}}
</div>



Grid Column:
<div {%if id %}id="{{id}}"{%endif%} class="{% for col in columns %}{{col}} {% endfor %}{%if classname %}{{classname}}{%endif%}">
    {{content}}
</div>

5. Usage:
{% load gridiron %}

{% grid_row "extra-class" %}
    {% grid_column "col-sm-12" "col-md-6" "col-lg-4" %}{% endcol %}
{% endrow %}
