import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = \
['cs', 'cs.core.logger']

package_data = \
{'': ['*']}

setuptools.setup(
    name='python_logger_core_sample',
    version='0.0.2',
    packages=packages,
    package_date= package_data,
    url='https://github.com/masakaya/python_logger_core_sample',
    license='MIT',
    author='Masashi Kayahara',
    author_email='masashi.kayahara@arc-connects.com',
    description='',
    python_requires=">=3.7",
)
