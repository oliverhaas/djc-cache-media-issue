from django_components import component


@component.register("icon")
class Icon(component.Component):
    template_name = "template.html"
