import httpx
from openai import OpenAI


def get_client() -> OpenAI:
    return OpenAI(
        api_key="learner013",
        base_url="https://keygateway.arshnivlabs.com/v1",
        http_client=httpx.Client(verify=False),
    )
