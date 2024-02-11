from setuptools import setup, find_packages

setup(
    name="opentelemetry-instrumentation-discordpy",
    version="0.1.1",
    author="Cookie",
    author_email="cookie@idegrity.com",
    description="OpenTelemetry instrumentation for discord.py bots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Idegrity/opentelemetry-instrumentation-discordpy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.9",
    install_requires=[
        "opentelemetry-api>=1.0.0",
        "opentelemetry-sdk>=1.0.0",
        "opentelemetry-instrumentation>=0.13b0",
        "discord.py>=1.7.3",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "pytest-asyncio", "flake8", "mypy"],
    },
)
