# ProposalGenerator

ProposalGenerator is an automated system designed to generate detailed proposal letters for NGOs. It leverages various document processing and natural language generation techniques to create comprehensive and customized proposals based on provided project descriptions and NGO details.

## Features

- **Document Reading**: Supports reading from text, PDF, and HTML files.
- **Text Splitting**: Utilizes recursive character text splitting for efficient document processing.
- **Vector Database Integration**: Stores and retrieves documents using ChromaDB.
- **Proposal Generation**: Automatically generates proposal letters based on project descriptions and NGO details.
- **Letter Regeneration**: Allows modification of generated letters based on user prompts.


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/nabojyoti/ProposalGenerator.git
    cd ProposalGenerator
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables in the [.env](http://_vscodecontentref_/12) file:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

### Register NGO Details

To register NGO details and proposal letters in the vector database, run the following command:

```sh
python register.py
```

## Generate Proposal Letters
To generate proposal letters based on the registered NGO details and project descriptions, run:

```sh
python generate_proposal.py
```

## Regenerate Proposal Letters
To modify a generated proposal letter based on user prompts, run:

```sh
python regenerate_proposal.py
```

# Configuration
The configuration files are located in the configs directory:

- `generate_configs.json`: Configuration for generating proposal letters.
- `register_configs.json`: Configuration for registering NGO details and proposal letters.