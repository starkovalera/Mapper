from setuptools import setup

setup(name='pipeline',
      version='0.1',
      description='Pipeline to read RSS feed to Django model',
      url='https://github.com/starkovalera/Pipeline',
      author='starkovalera',
      packages=['pipeline', 'pipeline.reader', 'pipeline.mapper', 'pipeline.writer'],
      install_requires=[
          'feedparser',
          'pytest',
      ],
      zip_safe=False)
