from setuptools import setup, find_packages

setup(
    name="sol-env",
    description="sol-env allows you to switch between environments in Solidity and other languages",
    url="https://github.com/hacker-DOM/sol-env/",
    author="Dominik Teiml <@hacker-dom>",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    license="MIT",
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": [
            "sol-env = sol_env.__main__:main",
        ]
    },
)