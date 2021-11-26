"""The setuptools setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# Define your dependencies here
requirements = []
setup_requirements = []

setup(
    author="MaisTODOS",
    author_email='devs@maistodos.com.br',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: Portuguese',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='chalice_utils',
    name='chalice_utils',
    packages=find_packages(include=['chalice_utils', 'chalice_utils.*']),
    setup_requires=setup_requirements,
    url='https://gitlab.com/guilherme.tavares/chalice_utils',
    version='0.0.1',
    zip_safe=False,
)
