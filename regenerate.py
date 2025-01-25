from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
client = OpenAI()


def regenerate_letter(proposal_letter: str, prompt: str):
    """
    Modify a proposal letter based on the given prompt.

    Args:
        proposal_letter (str): The original proposal letter.
        prompt (str): Instructions for modification.

    Returns:
        str: The modified proposal letter.

    Raises:
        Exception: If there is an error during the generation process.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant who can modify letters based on the user's prompt."
                },
                {
                    "role": "user",
                    "content": f"""A proposal letter is given as input. Modify it according to the user's prompt.
Proposal Letter
```
{proposal_letter}
```

User's Prompt
```
{prompt}
```

Modify it accordingly. Return the modified letter. Don't return any additional text.
"""
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating letter: {str(e)}")
