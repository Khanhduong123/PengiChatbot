import openai
import os

# Set the API key
openai.api_key = "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"

# Define the function that extracts fields of study from the user input
def extract_fields_of_study(user_input, fields_of_study):
    prompt = f"""
    The following is a list of existing fields of study in FPT University:
    {', '.join(fields_of_study)}.

    Given the input: "{user_input}"

    EXTRACT AND LISTING THE FIELDS OF STUDY THAT THE USER WANT TO KNOW FROM THE INPUT. AND THEN ONLY EXTRACT THE EXACT FIELDS OF STUDY, NOT EXACT FIELDS WHICH USERS INTERESTED IN, DO NOT GENERATE ANYTHING MORE.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    
    extracted_fields = response['choices'][0]['message']['content']
    return extracted_fields.strip()
