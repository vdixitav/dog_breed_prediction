from setuptools import find_packages, setup

setup(
    name = "app",
    version= '0.0.0',
    author="Dixitha",
    packages= find_packages(),
    #install_requires = ["pip install -r requirements.txt"]
    install_requires = ["Keras","opencv_python","numpy","streamlit"]
)