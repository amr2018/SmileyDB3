from setuptools import setup, find_packages

setup(
    name='SmileDB',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='Your Name',
    author_email='your_email@example.com',
    description='A brief description of SmileDB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/SmileDB',  # Update with your URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
