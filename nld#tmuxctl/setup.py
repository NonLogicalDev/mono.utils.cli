import setuptools

with open('requirements.in') as f:
  PYTHON_REQUIRES = f.read()

setuptools.setup(
  name="tmctl",
  version="0.0.1",
  description="A tool to aid in managing tmux",
  packages=setuptools.find_packages(exclude=['tests']),
  python_requires=PYTHON_REQUIRES,
)