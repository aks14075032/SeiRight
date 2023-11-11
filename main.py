import requests


def check_compliance(policy_url: str, webpage_url: str, api_url: str) -> None:
    """
    Perform a compliance check by making an HTTP POST request to the specified API.

    Parameters:
    - policy_url (str): The URL of the compliance policy.
    - webpage_url (str): The URL of the webpage to check for compliance.
    - api_url (str): The URL of the API endpoint.

    Returns:
    None
    """
    try:
        # Create a JSON payload with policy_url and webpage_url
        data = {
            "policy_url": policy_url,
            "webpage_url": webpage_url
        }

        # Define headers if needed
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_KEY"  # Include any necessary authorization headers
        }

        # Make an HTTP POST request to the API with headers
        response = requests.post(api_url, json=data, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the response JSON
        result = response.json()

        # Check for non-compliant results
        if "non_compliant_result" in result:
            non_compliant_results = result["non_compliant_result"]
            print(non_compliant_results)
        else:
            print("No non-compliant results found.")

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")


if __name__ == "__main__":
    # Define the URLs for the policy and webpage you want to check
    policy_url = "https://stripe.com/docs/treasury/marketing-treasury"
    webpage_url = "https://www.joinguava.com/"

    # Define the API endpoint URL
    api_url = "http://127.0.0.1:5000/check_compliance"  # Replace with your server's URL

    # Perform the compliance check
    check_compliance(policy_url, webpage_url, api_url)
