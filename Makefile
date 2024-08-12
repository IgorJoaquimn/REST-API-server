# Makefile for managing the Flask server with Conda and running the client

# Define the Conda environment name
CONDA_ENV = env

# Define the script to run the server
SERVER = Server/server.py

# Define the client script
CLIENT = Client/client.py

# Define default values for client arguments
CLIENT_IP ?= 127.0.0.1
CLIENT_PORT ?= 5000
CLIENT_ANALYSIS ?= 1
CLIENT_OUTPUT ?= output.csv

# Define the requirements file
REQUIREMENTS = requirements.txt

# Define the environment YAML file
ENV_YAML = environment.yml

# Target to create a Conda environment and install dependencies
env:
	@conda env create -f $(ENV_YAML) --prefix $(CONDA_ENV) || echo "Environment already exists. Use 'make install-requirements' to update."

# Target to clean up __pycache__ and other generated files
clean:
	@find . -type d -name "__pycache__" -exec rm -r {} + || true
	@find . -type f -name "*.pyc" -exec rm -f {} + || true
	@rm -rf $(CONDA_ENV)/

# Target to install requirements
install-requirements:
	@conda run --prefix $(CONDA_ENV) --no-capture-output pip install -r $(REQUIREMENTS)

# Target to run the server
run_server: env
	@conda run --prefix $(CONDA_ENV) --no-capture-output python $(SERVER)

# Target to run the client with specified arguments
run_client: env
	@conda run --prefix $(CONDA_ENV) --no-capture-output python $(CLIENT) $(CLIENT_IP) $(CLIENT_PORT) $(CLIENT_ANALYSIS) $(CLIENT_OUTPUT)

# Default target
all: run_server
