from setuptools import setup, find_packages


setup(
    name="scicalc",
    version="0.1.0",
    description="Simple scientific calculator",
    author="Juan Luis Cano Rodríguez",
    author_email="juanlu001@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'scicalc=scicalc.__main__:main'
        ]
    }
)
