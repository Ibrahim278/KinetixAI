import os
import openai
import config

openai.api_key = os.getenv("OPENAI_API_KEY", config.OPENAI_API_KEY)
def openAI(query):
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            prompt=query,
            temperature=0.5,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if 'choices' in response:
            if len(response['choices']) > 0:
                answer = response['choices'][0]['text']
            else:
                answer = 'Sorry! The AI could not understand what you are looking for'
        else:
            answer = 'Sorry! The AI could not understand what you are looking for'
        '''print(answer)'''
        return answer


