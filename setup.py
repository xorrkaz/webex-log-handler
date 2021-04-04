from setuptools import setup, find_packages

setup(
    name="webex_handler",
    version="1.0.0",
    description="A python logging handler that logs to Webex incoming webhooks",
    url="https://gitlab.systems.cll.cloud/jclarke/webex-log-handler",
    author="Joe Clarke",
    author_email="jclarke@cisco.com",
    license="MIT",
    setup_requires=["wheel"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["requests"],
    zip_safe=False,
    keywords=["Elemental"],
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
)
