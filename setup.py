# setup.py

from setuptools import setup

setup(
    name="jaculus-library-manager",  # Tool name
    version="0.2.0",  # Initial version
    py_modules=["jlm"],  # Specify the main Python file (no subfolders)
    entry_points={
        'console_scripts': [
            'jlm=jlm:main',  # Point to the `main` function in `jlm.py`
        ],
    },
    install_requires=["requests>=2.20.0"],  # Add any dependencies if required
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple library manager for Jaculus",
    url="https://github.com/yourusername/jaculus-library-manager",  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    
)
