from typing import Any
from utils.formatter import create_uuid
from reader.text_reader import read_text
from reader.pdf_reader import read_pdf
from reader.html_reader import read_html
from vector_datbase.chroma_db import ChromaDB
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from utils.text_generator import generate_timeline, generate_budget, generate_letter, text_completion
from downloader.file_download import html_downloader


# Generate proposal letter
def write_letter(configs: dict[str, Any]):
    # Read and embed project description
    docs = []
    for file_path in configs['project_docs']:
        if file_path.endswith('.pdf'):
            data = read_pdf(file_path)
        elif file_path.endswith('.txt'):
            data = read_text(file_path)
        elif file_path.endswith('.html'):
            filename = html_downloader(file_path)
            if filename is None:
                continue
            data = read_html(filename)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        docs.extend(data)
    desc_db = InMemoryVectorStore(OpenAIEmbeddings())
    desc_db.add_documents(documents=docs)
    # Initialize other databases
    index_name = str(create_uuid(configs['name']))
    ngo_details_db = ChromaDB(collection_name=index_name + '_details')
    letters_db = ChromaDB(collection_name=index_name + '_letters')
    meta_db = ChromaDB(collection_name=index_name + '_meta')
    # Topic of the letter
    rec = desc_db.similarity_search("What is the objective of the project?", top_k=5) + \
        desc_db.similarity_search("What is the goal of the project?", top_k=5) + \
        desc_db.similarity_search("What is the title of the project?", top_k=5)
    rec = list({x.id: x.page_content for x in rec}.values())
    topic = text_completion("what is the objective of the project?", rec)
    # Given timeline of the project
    rec = desc_db.similarity_search("What is the given timeline of the project?", top_k=5) + \
        desc_db.similarity_search("What is the deadline of the project?", top_k=5)
    rec = list({x.id: x.page_content for x in rec}.values())
    timeline = text_completion("what is the given timeline / deadline of the project?", rec)
    # Given budget of the project
    rec = desc_db.similarity_search("What is the given budget of the project?", top_k=5) + \
        desc_db.similarity_search("What is the total budget of the project?", top_k=5) + \
        desc_db.similarity_search("What is the total expenses provided for the project?", top_k=5)
    rec = list({x.id: x.page_content for x in rec}.values())
    budget = text_completion("what is the given budget of the project?", rec)
    # NGO name
    rec = ngo_details_db.query("What is name of the NGO?", top_k=5) + \
        ngo_details_db.query("What is name of the organization?", top_k=5)
    rec = list({x.id: x.page_content for x in rec}.values())
    ngo_name = text_completion("what is the name of the NGO?", rec)
    # Objective of the NGO
    rec = ngo_details_db.query("What is the objective of the NGO?", top_k=10) + \
        ngo_details_db.query("What is the goal of the NGO?", top_k=10)
    rec = list({x.id: x.page_content for x in rec}.values())
    ngo_objective = text_completion("what is the objective of the NGO?", rec)
    # Details of the NGO
    rec = ngo_details_db.query("Describe all the details of the NGO?", top_k=10) + \
        ngo_details_db.query("Describe all the properties of the NGO?", top_k=10) + \
        ngo_details_db.query("When the NGO was founded?", top_k=5) + \
        ngo_details_db.query("How many members are there in the NGO?", top_k=10) + \
        ngo_details_db.query("What is the unique about the NGO?", top_k=10)
    rec = list({x.id: x.page_content for x in rec}.values())
    ngo_desc = text_completion("Give me a detailed summary of all the details of the NGO. Make it as descriptive as possible.", rec)

    # Prvious projects
    rec = ngo_details_db.query("What are the previous projects of the NGO?", top_k=20) + \
        ngo_details_db.query("What are the projects completd by the NGO?", top_k=20)
    rec = list({x.id: x.page_content for x in rec}.values())
    previous_projects = text_completion("what are the previous projects of the NGO?", rec)
    # Fetch similar projects, timeline and budget from the previous letter
    rec = meta_db.query(topic, top_k=3)
    similar_projects = [x.page_content for x in rec]
    sample_timline = [x.metadata['timeline'] for x in rec]
    sample_budget = [x.metadata['budget'] for x in rec]
    # Build the timeline for the project
    project_timeline = generate_timeline(topic, timeline, sample_timline)

    # Build the budget for the project
    project_budget = generate_budget(topic, budget, sample_budget)
    # Generate the letter
    prompt = f"""Write a proposal letter for a NGO using the following information:
NGO Name: {ngo_name}
NGO Objective: {ngo_objective}
NGO Details: {ngo_desc}
Previous Projects: {previous_projects}
Similar Projects: {similar_projects}


Project Topic for the current Proposal Letter: {topic}
Project Deadline for the Current Proposal Letter: {timeline}
Project Budget for the Current Proposal Letter: {budget}

Also, attach the timeline and budget of the project created by the NGO:
Timeline of the project: {project_timeline}
Budget of the project: {project_budget}

Take your time and think step by step to write the proposal letter.
Make sure to add the following sections:
1. Description of the NGO
2. Why the NGO is best choice for the project
3. Timeline of the project
4. Budget of the project
Accoeding to you add some more sections in the letter which are needed for a proposal letter.

The proposal letter should be as descriptive as possible. It should be also as long as possible.
Try not to excude any provided details. Include as many details as possible in the letter from the given context.
Project time and budget created by the NGO shouldn't be updated and should be included as it's provided in the letter.
Return only the letter. Don't return any additional text.
"""
    letter = generate_letter(prompt)
    print(letter)
    with open('assets/timeline.txt', 'w') as file:
        file.write(project_timeline)
    with open('assets/budget.txt', 'w') as file:
        file.write(project_budget)
    with open('assets/letter.txt', 'w') as file:
        file.write(letter)
    return letter
