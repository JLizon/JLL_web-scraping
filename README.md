# Tesla Revenue Scraper

A simple web scraper that extracts Tesla's revenue data from Macrotrends.

## Features

- Extracts revenue data for Tesla from the Macrotrends website.
- Handles  403 Forbidden errors by retrying the request with a custom User-Agent header.

## Requirements

- Python  3
- `requests`
- `beautifulsoup4`
- `pandas`

## Installation

To set up the project, you will need Python  3. It is recommended to create a virtual environment. You can install the required packages using pip:


## Usage

1. Import the necessary libraries:


2. Define the URL for Tesla's revenue chart:


3. Retrieve the HTML content of the page:


4. If a  403 Forbidden error is encountered, use a custom User-Agent header to retry the request:

