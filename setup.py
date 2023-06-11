from setuptools import setup

with open('readme.md', 'r') as f:
    readme = f.read()

setup(
    name='PoePT',
    version='0.2.4',
    description='Python package for interacting with the Quora POE chatbot',
    author='Saikyo0',
    author_email='mamaexus@gmail.com',
    url='https://github.com/saikyo0/PoePT',
    packages=['poept'],
    install_requires=[
        'selenium',
        'webdriver_manager',
        'SpeechRecognition'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description=readme,
    long_description_content_type='text/markdown'
)
