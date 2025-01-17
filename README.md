# HaloPSA Ticket Recalculation Script

This Python script is designed to automate the process of recalculating billing for tickets in the HaloPSA. It allows for processing all tickets within a specified date range, optionally filtering by customer ID and starting from a specific ticket ID.

## Configuration

Before running the script, you need to configure it with your HaloPSA app client ID and secret, API URL, Auth URL, Tenant, and the start and end dates for the ticket processing range. You can also specify a customer ID to limit the processing to a single customer, or leave it blank to process tickets for all customers. Additionally, you can set a ticket ID as a starting point or leave it as `None` to process all tickets.

### Parameters

- `client_id`: Your HaloPSA app client ID.
- `secret`: Your HaloPSA app secret.
- `api_url`: The base URL for the HaloPSA API.
- `auth_url`: The URL for HaloPSA authentication.
- `tenant`: Your HaloPSA tenant identifier.
- `start_date`: The start date for the ticket processing range (YYYY-MM-DD).
- `end_date`: The end date for the ticket processing range (YYYY-MM-DD).
- `customer_id`: The customer ID to filter tickets by (leave blank for all customers).
- `start_from_ticket_id`: The ticket ID to start processing from (leave as `None` for all tickets).

## Usage

1. Ensure you have Python 3 installed on your system.
2. Install the `requests` library using pip:
