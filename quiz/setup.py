from setuptools import setup, find_packages

setup(
    name="leetcode-questions",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask==3.0.2",
        "flask-cors==4.0.0",
        "requests==2.31.0",
        "beautifulsoup4==4.12.3",
        "streamlit==1.32.0",
        "python-dotenv==1.0.1",
        "gunicorn==21.2.0",
        "plotly==5.19.0",
        "pandas==2.2.1",
        "numpy==1.26.4",
        "dash==2.14.2",
        "dash-core-components==2.0.0",
        "dash-html-components==2.0.0",
        "dash-table==5.0.0"
    ],
    python_requires=">=3.12.0",
) 