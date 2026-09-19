from setuptools import setup, find_packages

setup(
    name="instaagent",
    version="2.0.0",
    description="Autonomous Instagram Specialist Agent with Leno OS compatibility",
    author="arunkumarpatil24j2007-cmd",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.5.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "full": [
            "google-genai>=0.1.1",
            "pillow>=10.0.0",
        ]
    },
)
