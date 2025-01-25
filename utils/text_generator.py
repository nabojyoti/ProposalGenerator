from typing import List
from datetime import date
from openai import OpenAI
client = OpenAI()



def text_completion(query: str, records: List):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who can give answer of the user's query based on the given context."},
            {
                "role": "user",
                "content": f"""The user's query is given as follows:
Query
```
{query}
```

The context is given as follows:
Context
```
{records}
```

Answer the user's query based on the given context. If the answer isn't found in the given context then return 'Not specified'.
Return only the answer. Don't return any additional text.
"""
            }
        ]
    )
    return completion.choices[0].message.content




def generate_letter(prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who can write proposal letters for NGOs from a given topic and some other details related to NGO and the current project."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


def generate_timeline(project_title: str, total_timeline: str, records: List):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is an expert to create timeline of projects."},
            {
                "role": "user",
                "content": f"""
Project Title
```
{project_title}
```

Deadline of the project:
```
{total_timeline}
```

Current date:
```
{date.today()}
```

Some available details of timeline of the previous projects:
```
{records}
```

Take your time and think step by step to create the detailed timeline of the project. 
Make sure that the timeline is as descriptive as possible. Return the timeline pointwise. Exaplain each point of the timeline in detail.
Return the generated timeline only and don't return any additional text.
"""
            }
        ]
    )
    return completion.choices[0].message.content


def generate_budget(project_title: str, total_budget: str, records: List):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is an expert to create timeline of projects."},
            {
                "role": "user",
                "content": f"""
Project Title / Topic
```
{project_title}
```

Total budget of the project:
```
{total_budget}
```

Some available details of budget of the previous projects:
```
{records}
```

Take your time and think step by step to create the detailed budget of the project. 
Make sure that the budget is as descriptive as possible. Return the budget pointwise. Explain each points of the budget in detail.
Return the generated budget only and don't return any additional text.
"""
            }
        ]
    )
    return completion.choices[0].message.content