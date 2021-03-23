from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(
            modules.LinkList(
                "Redes Sociales",
                children=[
                    {
                        'title': 'Twitter',
                        'url': 'https://bit.ly/3fAINsK',
                        'external': True,
                    },
                    {
                        'title': 'Facebook',
                        'url': 'https://bit.ly/3dD0mGy',
                        'external': True,
                    },
                    {
                        'title': 'Youtube',
                        'url': 'https://bit.ly/3ewUEXl',
                        'external': True,
                    },
                ],
                column=2,
                order=0
            )
        )

        self.children.append(
            modules.LinkList(
                "Orden de Predicadores",
                children=[
                    {
                        'title': 'Twitter',
                        'url': 'https://twitter.com/dominicos_es',
                        'external': True,
                    },
                    {
                        'title': 'Página Oficial',
                        'url': 'https://dominicos.es',
                        'external': True,
                    }
                ],
                column=2,
                order=0
            )
        )

        self.children.append(
            modules.AppList(
                'Aplicación',
                exclude=None,
                column=0,
                order=0
            )
        )

        self.children.append(
            modules.RecentActions(
                'Acciones Recientes',
                5,
                column=0,
                order=0
            )
        )