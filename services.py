from django.apps import apps

def get_response(prompt, messages=None, temperature=0):
    chatbot_model = apps.get_app_config('chatbot').model

    if messages == None:
        messages = []
    
    messages.append({'role': 'user', 'parts': [prompt]})
    
    # Set up the model
    generation_config = {
      "temperature": temperature,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }
    
    # Generate content based on user prompt
    response = chatbot_model.generate_content(
                contents=messages,
                generation_config=generation_config,
            )
    response_dict = {
        'role': response.candidates[0].content.role,
        'parts': [response.candidates[0].content.parts[0].text]
    }
    messages.append(response_dict)
    
    return messages