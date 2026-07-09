from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from config import API_KEY, PROJECT_ID, URL

credentials = Credentials(
    url=URL,
    api_key=API_KEY
)

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID
)

response = model.generate_text(
    prompt="Say hello in one sentence."
)

print(response)