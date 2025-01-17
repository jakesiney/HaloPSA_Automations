import requests
import json
import time

""" Configuration - Enter HaloPSA app client id and secret, API URL, Auth URL, Tenant, Start and End dates. 
Enter a Customer ID or leave blank to do process all customers. A ticket ID can be used as a starting point or leave as None to process all tickets. """
client_id = ""
secret = ""
api_url = "https://YOURDOMAIN.halopsa.com/api"
auth_url = "https://YOURDOMAIN.halopsa.com/auth"
tenant = ""
start_date = "2024-02-01T00:00:00.00" # yyyy-mm-dd
end_date = "2024-02-28T00:00:00.00" # yyyy-mm-dd
customer_id = ""
start_from_ticket_id = None


# Construct URLs
tickets_all_url = f"{api_url}/tickets?startdate={start_date}&enddate={end_date}&ticketidonly=true&client_id={customer_id}"
actions_base_url = f"{api_url}/Actions"
actions_url = f"{api_url}/Actions?excludesys=true"
tenant_param = f"tenant={tenant}" if tenant else ""
token_endpoint = f"{auth_url}/token?{tenant_param}"
print(f"API URL: {api_url}")
print(f"AUTH URL: {auth_url}")


def get_token(token_endpoint, client_id, secret):
    """
    Retrieves an access token from the specified token endpoint using client credentials.

    Args:
        token_endpoint (str): The URL of the token endpoint.
        client_id (str): The client ID for authentication.
        secret (str): The client secret for authentication.

    Returns:
        str: The access token retrieved from the token endpoint.
    """
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
    response_data = response.json()
    print("New token retrieved")
    return response_data['access_token']

def get_tickets(token, tickets_all_url):
    """
    Retrieves tickets from the specified URL using the provided token.

    Args:
        token (str): The authorization token.
        tickets_all_url (str): The URL to retrieve the tickets from.

    Returns:
        dict: A dictionary containing the JSON response from the API.

    """
    headers = {
        "Authorization": f"Bearer {token}",
        "halo-app-name": "halo-web-application"
    }
    response = requests.get(tickets_all_url, headers=headers)
    return response.json()

def process_tickets(token, tickets_data, start_from_ticket_id, token_endpoint, client_id, secret):
    """
    Process tickets and recalculate billing for actions with time entered.

    Args:
        token (str): The access token for authentication.
        tickets_data (dict): The data containing the tickets.
        start_from_ticket_id (int): The ticket ID to start processing from.
        token_endpoint (str): The endpoint to get the access token.
        client_id (str): The client ID for authentication.
        secret (str): The secret key for authentication.

    Returns:
        None
    """
    token = get_token(token_endpoint, client_id, secret)  # Ensure the token is refreshed at the start

    # Sort tickets by ID in ascending order so that we can skip tickets with IDs less than start_from_ticket_id
    tickets = sorted(tickets_data['tickets'], key=lambda x: x['id'])

    for ticket in tickets:
        current_ticket_id = int(ticket['id'])
        
        if start_from_ticket_id is not None and current_ticket_id < start_from_ticket_id:
            continue  # Skip tickets with IDs less than start_from_ticket_id

        # Refresh token to avoid expiration
        token = get_token(token_endpoint, client_id, secret)

        action_get_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "halo-app-name": "halo-web-application"
        }

        one_action_url = f"{actions_url}&ticket_id={ticket['id']}"
        response_action_get = requests.get(one_action_url, headers=action_get_headers)
        actions_data = response_action_get.json()

        for action in actions_data['actions']:
            if action.get('timetaken', 0) > 0:
                action_post_headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "halo-app-name": "halo-web-application"
                }

                body_action_post = json.dumps([{
                    "id": action['id'],
                    "ticket_id": ticket['id'],
                    "recalculate_billing": True
                }])

                response_action_recalc = requests.post(actions_base_url, headers=action_post_headers, data=body_action_post)
                post_response_data = response_action_recalc.json()
                print(f"Ticket ID = {ticket['id']} Action ID = {post_response_data['id']} - recalculated (for Client = {ticket['client_name']})")
                time.sleep(1)
            else:
                print(f"Ticket ID = {ticket['id']} Action ID = {action['id']} - not recalculated (for Client = {ticket['client_name']}) as no time entered")

def main():
    token = get_token(token_endpoint, client_id, secret)
    tickets_data = get_tickets(token, tickets_all_url)
    process_tickets(token, tickets_data, start_from_ticket_id, token_endpoint, client_id, secret)

if __name__ == "__main__":
    main()
