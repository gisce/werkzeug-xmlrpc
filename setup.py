# -*- coding: utf-8 -*-
"""Setup per la llibreria de Werkzeug-XMLRPC"""
import os
import shutil
import unittest
from distutils.command.clean import clean as _clean
from distutils.core import Command
from setuptools import setup, find_packages

from werkzeug_xmlrpc import __version__

PACKAGES_DATA = {}


class Clean(_clean):
    """Eliminem el directory build i els bindings creats."""
    def run(self):
        """Comença la tasca de neteja."""
        _clean.run(self)
        if os.path.exists(self.build_base):
            print "Cleaning %s dir" % self.build_base
            shutil.rmtree(self.build_base)


setup(name='werkzeug_xmlrpc',
      description='Llibreria de switching',
      author='GISCE Enginyeria',
      author_email='devel@gisce.net',
      url='http://www.gisce.net',
      version=__version__,
      license='MIT',
      long_description='''Long description''',
      provides=['werkzeug_xmlrpc'],
      install_requires=['werkzeug'],
      tests_require=['expects'],
      packages=find_packages(),
      package_data=PACKAGES_DATA,
      scripts=[],
      cmdclass={'clean': Clean},
      test_suite='tests',
)
