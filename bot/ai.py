import openai
import database
import traceback

AI_ERROR_MESSAGE = 'An internal error has occured. Please try again in a few moments.'
AI_INVALID_KEY_MESSAGE = 'No valid API key provided. To set an API key, use the "setkey" command in a private channel. You can find your API key at https://beta.openai.com/account/api-keys.'
AI_KEY_CREDIT_ERROR = 'The given open ai key no longer has any credit. You can check your credit and usage by going to https://beta.openai.com/account/usage'
TEST_CASE = 'What is 1+1?'

async def get_ai_response(input_txt: str, api_key:str) -> str:
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        max_tokens=1000,
        prompt=input_txt,
        temperature=0.5
    )

    return response['choices'][0]['text']

async def query_ai(prompt: str, server_id: int) -> str:
    api_key = database.get_ai_key(server_id)
    try:
        ai_response = await get_ai_response(prompt, api_key)
    except openai.error.AuthenticationError:
        ai_response = AI_INVALID_KEY_MESSAGE
    except openai.error.RateLimitError:
        ai_response = AI_KEY_CREDIT_ERROR
    except Exception:
        ai_response = AI_ERROR_MESSAGE
        traceback.print_exc()
    
    return ai_response

async def is_valid_key(key: str) -> bool:
    try:
        await get_ai_response(TEST_CASE, key)
    except:
        return False
    return True