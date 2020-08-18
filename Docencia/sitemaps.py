from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class Dynamic(Sitemap):
    priority = 1.0
    changefreq = 'daily'


    def items(self):
        return ['index', 'admision_dashboard']

    def location(self, item):
        return reverse(item)