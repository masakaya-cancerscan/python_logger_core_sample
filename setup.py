# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cs', 'cs.core.logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-logger-core-sample',
    'version': '0.1.14',
    'description': '',
    'long_description': 'None',
    'author': 'Masashi.Kayahara',
    'author_email': 'masashi.kayahara@arc-connects.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}

setup(**setup_kwargs)