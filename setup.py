from setuptools import setup, find_packages

setup(
    name='DigitalSignal',  # Replace with your package name
    use_scm_version=True,  # Automatically use version from Git tags
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/caden-cardell/DigitalSignal',  # Replace with your GitHub URL
    author='Caden Cardell',
    author_email='cadencardell@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change to your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package's dependencies here, e.g., 'numpy', 'requests'
    ],
)
