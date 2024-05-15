from openai import OpenAI
import time

# init client and connect to localhost server
client = OpenAI(
    api_key="3d252ff13a770cbbb99ae41f41785b11",
    base_url="http://localhost:8000/v1" # change the default port if needed
)

# call API
start = time.time()
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a useful AI assistant.",
        },

		{
			"role": "user",
			"content":"hello, how are you doing today?",
		}
    ],
    #model="mistral-7b-instruct-v0.1.Q4_0.gguf",
	#model="Meta-Llama-3-8B-Instruct.Q5_K_M.gguf",
	model="Meta-Llama-3-8B-Instruct-exl2-4_25",
	seed=0,
	temperature=0.0
)

print(response.usage.completion_tokens/(time.time()-start))
print(response.choices[0].message.content)