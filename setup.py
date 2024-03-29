from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'girder>=3.0.0a1'
]

setup(
    author='Curtis Lisle',
    author_email='clisle@knowledgevis.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description='Girder v3 adaptation of NCIAuth',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='girder-plugin, nciauth_girder3',
    name='nciauth_girder3',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/knowledgevis/NCIAuth-girder3',
    version='0.1.0',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'nciauth_girder3 = nciauth_girder3:GirderPlugin'
        ]
    }
)
