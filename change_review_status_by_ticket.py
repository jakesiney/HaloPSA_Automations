import requests
import json
from decouple import config

client_id = config('CLIENT_ID')
secret = config('SECRET')
api_url = "https://synergy.halopsa.com/api"
auth_url = "https://synergy.halopsa.com/auth"
tenant = "synergy"

ticket_id = 361718  # Set the ticket ID here

token_endpoint = f"{auth_url}/token?tenant={tenant}"
actions_base_url = f"{api_url}/Actions"
actions_url = f"{api_url}/Actions?excludesys=true&ticket_id={ticket_id}"


def get_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "halo-app-name": "halo-web-application"
    }
    body = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": secret,
        "scope": "all"
    }
    response = requests.post(token_endpoint, headers=headers, data=body)
    return response.json()['access_token']


def main():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "halo-app-name": "halo-web-application"
    }

    actions_data = requests.get(actions_url, headers=headers).json()
    actions = actions_data['actions']
    print(f"Found {len(actions)} actions for Ticket ID = {ticket_id}")

    for action in actions:
        if action.get('actreviewed') is not True:
            print(f"  Action ID = {action['id']} - not reviewed, skipping")
            continue

        print(f"  Action ID = {action['id']} - setting actreviewed to false...")
        body = json.dumps([{"id": action['id'], "ticket_id": ticket_id, "actreviewed": False}])
        response = requests.post(actions_base_url, headers=headers, data=body)
        try:
            print(f"  Action ID = {response.json()['id']} - done")
        except json.JSONDecodeError:
            print(f"  Action ID = {action['id']} - FAILED (Status: {response.status_code}) - {response.text}")


if __name__ == "__main__":
    main()
