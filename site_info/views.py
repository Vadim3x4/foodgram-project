from django.views.generic.base import TemplateView


class AboutPage(TemplateView):
    template_name = 'about_page.html'


class TechPage(TemplateView):
    template_name = 'tech_page.html'