# Makefile for managing the Flask server with Conda

# Define the Conda environment name
CONDA_ENV = env

# Define the script to run
SERVER = Server/server.py

# Define the requirements file
REQUIREMENTS = requirements.txt

# Target to create a Conda environment and install dependencies
env:
	@conda env create -f environment.yml --prefix $(CONDA_ENV)/ || echo "Environment already exists. Use 'make install-requirements' to update."

# Target to clean up __pycache__ and other generated files
clean:
	@find . -type d -name "__pycache__" -exec rm -r {} + || true
	@find . -type f -name "*.pyc" -exec rm -f {} + || true
	@rm -rf $(CONDA_ENV)/

# Target to install requirements (if no requirements file is used, remove this target)
install-requirements:
	@conda run --prefix $(CONDA_ENV) --no-capture-output pip install -r $(REQUIREMENTS)

# Target to run the server
run_server: env
	@conda run --prefix $(CONDA_ENV) --no-capture-output python $(SERVER)

# Default target
all: run_server
