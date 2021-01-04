from setuptools import setup, find_packages

install_requires = [
    'jsonschema==3.2.0',
]

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='azure-arm2schema',
    version="0.1.0",
    description="Convert ARM Parameters to JSON Schema",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True, 
    install_requires=install_requires,
    zip_safe=False,
    author='Stephane RAULT',
    author_email="stephane.rault@radicalspam.org",
    python_requires='>=3.8',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'arm2schema = arm2schema.core:main',
        ],
    }    
)
