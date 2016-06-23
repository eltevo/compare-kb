#!/usr/bin/env python
"""Extend regular notebook server to be aware of multiuser things."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jinja2 import ChoiceLoader, FunctionLoader
from notebook.notebookapp import NotebookApp

page_template = """
{% extends "templates/page.html" %}

{% block header_buttons %}
{{super()}}

<a href='{{stop_link}}'
 class='btn btn-lg btn-danger navbar-btn pull-right'
 style='margin-right: 4px; margin-left: 2px;'
>
STOP</a>
<a href='{{commit_link}}'
 class='btn btn-lg btn-success navbar-btn pull-right'
 style='margin-right: 4px; margin-left: 2px;'
>
COMMIT</a>
<a href='{{push_link}}'
 class='btn btn-lg btn-primary navbar-btn pull-right'
 style='margin-right: 4px; margin-left: 2px;'
>
PUSH</a>
{% endblock %}
"""



class KooplexUserNotebookApp(NotebookApp):

      def patch_templates(self):

        # let us point to some crasy urls with the buttons
        # this illustrates the values of some internal url type strings
        env = self.web_app.settings['jinja2_env']
        env.globals['stop_link'] = 'http://www.google.com/'+self.base_url
        env.globals['commit_link'] = 'http://www.google.com/'+self.connection_url
        env.globals['push_link'] = 'http://www.google.com/'+self.default_url


        # patch jinja env loading to modify page template
        def get_page(name):
            if name == 'page.html':
                return page_template

        orig_loader = env.loader
        env.loader = ChoiceLoader([
            FunctionLoader(get_page),
            orig_loader,
        ])

     
      def init_webapp(self):

          super(KooplexUserNotebookApp,self).init_webapp()
          self.patch_templates()

def main(argv=None):
    return KooplexUserNotebookApp.launch_instance(argv)


if __name__ == "__main__":
    main()
