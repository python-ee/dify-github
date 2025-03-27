import requests
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider


class GithubProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            if "access_tokens" not in credentials or not credentials.get("access_tokens"):
                raise ToolProviderCredentialValidationError("Github API Access Tokens is required.")
            if "api_version" not in credentials or not credentials.get("api_version"):
                api_version = "2022-11-28"
            else:
                api_version = credentials.get("api_version")
            if "api_url" not in credentials or not credentials.get("api_url"):
                api_url = "https://api.github.com"
            else:
                api_url = credentials.get("api_url")
            try:
                headers = {
                    "Content-Type": "application/vnd.github+json",
                    "Authorization": f"Bearer {credentials.get('access_tokens')}",
                    "X-GitHub-Api-Version": api_version,
                }
                response = requests.get(
                    url="{api_url}/search/users?q={account}".format(api_url=api_url, account="charli117"), headers=headers
                )
                if response.status_code != 200:
                    raise ToolProviderCredentialValidationError(response.json().get("message"))
            except Exception as e:
                raise ToolProviderCredentialValidationError("Github API Key and Api Version is invalid. {}".format(e))
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
