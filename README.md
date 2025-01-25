# ProposalGenerator

ProposalGenerator is an automated system designed to generate detailed proposal letters for NGOs. It leverages various document processing and natural language generation techniques to create comprehensive and customized proposals based on provided project descriptions and NGO details.

## Features

- **Document Reading**: Supports reading from text, PDF, and HTML files.
- **Text Splitting**: Utilizes recursive character text splitting for efficient document processing.
- **Vector Database Integration**: Stores and retrieves documents using ChromaDB.
- **Proposal Generation**: Automatically generates proposal letters based on project descriptions and NGO details.
- **Letter Regeneration**: Allows modification of generated letters based on user prompts.

## Project Structure
```
ProposalGenerator/
├── assets/
│   ├── budget.txt
│   ├── green_horizon_details_1.txt
│   ├── letter.txt
│   ├── project_description.txt
│   ├── proposal_letter_1.txt
│   ├── proposal_letter_2.txt
│   ├── proposal_letter_3.txt
│   ├── proposal_letter_4.txt
│   └── timeline.txt
├── configs/
│   ├── generate_configs.json
│   └── register_configs.json
├── downloader/
│   ├── __init__.py
│   └── downloader.py
├── extractor/
│   ├── __init__.py
│   └── extractor.py
├── reader/
│   ├── __init__.py
│   ├── html_reader.py
│   ├── pdf_reader.py
│   └── text_reader.py
├── text_splitters/
│   ├── __init__.py
│   └── text_splitter.py
├── utils/
│   ├── __init__.py
│   ├── formatter.py
│   └── text_generator.py
├── vector_database/
│   ├── __init__.py
│   ├── chroma_db.py
│   └── pinecone_db.py
├── .env
├── generate.py
├── main.py
├── README.md
├── regenerate.py
├── register.py
└── requirements.txt
```
## Tech Stack

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
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