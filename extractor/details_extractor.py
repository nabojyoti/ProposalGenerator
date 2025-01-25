import json
from pydantic import BaseModel
from openai import OpenAI
client = OpenAI()



class LetterResponse(BaseModel):
    topic: str
    timeline: str
    budget: str


def extract_letter_details(file_content: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract the project timeline and project budget / expenses from the proposal letter."},
            {"role": "user", "content": f"""A proposal letter is given:
Proposal Letter
```
{file_content}
```
Extract the topic of the project from the letter. It shouldn't be more than 1-2 lines.
Extract the detailed timeline of how the project will be executed and the detailed information of how the total budget will be used.
If any of the answers can't be found then return 'Not specified' for it.
"""},
        ],
        response_format=LetterResponse,
    )
    return json.loads(completion.choices[0].message.parsed.json())