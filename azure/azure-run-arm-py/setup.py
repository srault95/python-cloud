from setuptools import setup, find_packages

install_requires = [
    'python-dotenv==0.15.0',
    'azure-mgmt-resource==15.0.0',
    'azure-identity==1.5.0',
    'msrestazure==0.6.4'
]

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='azure-run-arm-py',
    version="0.1.0",
    description="Run ARM Template with Python",
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
)
