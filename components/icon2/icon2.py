from django_components import component


@component.register("icon2")
class Icon(component.Component):
    template_name = "template.html"
