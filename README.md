# Installation Guide for DarkGPT Project

![Descripción de la imagen](https://i.imgur.com/bYW6pai.jpg)

DarkGPT is an artificial intelligence assistant based on GPT-4-200K designed to perform queries on leaked databases. This guide will help you set up and run the project on your local environment.

## Prerequisites

Before starting, make sure you have Python installed on your system. This project has been tested with Python 3.8 and higher versions.

## Environment Setup

1.**Clone the Repository**

   First, you need to clone the GitHub repository to your local machine. You can do this by executing the following command in your terminal:

  git clone <https://github.com/luijait/DarkGPT.git>
  cd DarkGPT

1.**Configure Environment Variables**

   You will need to set up some environment variables for the script to work correctly. Copy the `.env.example` file to a new file named `.env`:

   DEHASHED_API_KEY="your_dehashed_api_key_here"

2. **Create a virtual environment**

   It is recommended to use a virtual environment to manage dependencies safely:

   python3 -m venv .venv
   source .venv/bin/activate

   When the venv is active, the shell prompt will usually change to show the environment name, for example:

   (.venv) user@machine ~/DarkGPT$

3. **Install dependencies**

   Install the required Python packages inside the active virtual environment:

   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   If you want to run tests, install the dev dependencies too:

   python3 -m pip install -e .[dev]

   Then run tests with:

   python3 -m pytest tests/test_import.py

4. **Run the project**

   With the virtual environment active, start the CLI:

   python3 main.py

   ## Or run via module

   python3 -m darkgpt.main

5. **Runtime check**

   Verify the package imports successfully before starting the app:

   python3 -c "import darkgpt; print('darkgpt import OK')"

6. **Run tests**

   Execute the import test with pytest:

   python3 -m pytest tests/test_import.py

7. **Package install option**

   Install the package in editable mode to use the entry point directly:

   python3 -m pip install -e .

7.**Deactivate the virtual environment**

   When you are finished working with the project, deactivate the active environment with:

   deactivate
