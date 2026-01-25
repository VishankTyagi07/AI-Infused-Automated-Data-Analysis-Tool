from ai.prompts import PROMPT_DATASET_SUMMARY
from openai import OpenAI
import json

client = OpenAI()
def generate_dataset_summary(metadata: dict) -> str:
    # Create the prompt by injecting the metadata
    prompt = PROMPT_DATASET_SUMMARY.format(metadata=json.dumps(metadata,indent=2))

    # Call the OpenAI API to generate the summary
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior data analyst. You analyze dataset metadata and produce concise,"
            " structured analytical summaries. Do not hallucinate missing information."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.2,
    )

    # Extract and return the summary from the response
    summary = response.choices[0].message.content
    return summary