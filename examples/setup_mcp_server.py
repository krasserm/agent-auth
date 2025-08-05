
import json
import os
import webbrowser

from composio_client import Composio


def list_tools(client: Composio, toolkit: str):
    tools = client.tools.list(toolkit_slug=toolkit)
    for item in tools.items:
        print(item.slug)


def setup_googlecalendar(client: Composio, user_id: str):
    # -------------------------------------
    #  Create auth config
    # -------------------------------------
    auth_scopes = [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ]

    response = client.auth_configs.create(
        toolkit={"slug": "googlecalendar"},
        auth_config={
            "name": "calendar-example", 
            "type": "use_composio_managed_auth",
            "authScheme": "OAUTH2",
            "credentials": {
                "scopes": ",".join(auth_scopes)
            }
        },
    )
    auth_config_id = response.auth_config.id

    # -------------------------------------
    #  Create connected account
    # -------------------------------------
    response = client.connected_accounts.create(
        auth_config={"id": auth_config_id},
        connection={"user_id": user_id},
    )

    # -------------------------------------
    #  Open browser to initiate OAuth flow
    #  (doesn't wait for completion)
    # -------------------------------------
    webbrowser.open(response.connection_data.val.redirect_url)

    # -------------------------------------
    #  Create MCP server
    # -------------------------------------
    result = client.mcp.create(
        auth_config_ids=[auth_config_id],
        name="calendar-server",
        allowed_tools=["GOOGLECALENDAR_FIND_EVENT"],
        managed_auth_via_composio=False,
    )

    # -------------------------------------
    #  Return user-specific MCP server URL
    # -------------------------------------

    # API responds with legacy transport=sse query param which can be removed to 
    # get a streamable http MCP server. Replace with user_id query param instead.
    return result.mcp_url.replace("transport=sse", f"user_id={user_id}")


def setup_gmail(client: Composio, user_id: str):
    # -------------------------------------
    #  Create auth config
    # -------------------------------------
    response = client.auth_configs.create(
        toolkit={"slug": "gmail"},
        auth_config={
            "name": "gmail-example", 
            "type": "use_composio_managed_auth",
            "authScheme": "OAUTH2",
        },
    )
    auth_config_id = response.auth_config.id

    # -------------------------------------
    #  Create connected account
    # -------------------------------------
    response = client.connected_accounts.create(
        auth_config={"id": auth_config_id},
        connection={"user_id": user_id},
    )

    # -------------------------------------
    #  Open browser to initiate OAuth flow
    #  (doesn't wait for completion)
    # -------------------------------------
    webbrowser.open(response.connection_data.val.redirect_url)

    # -------------------------------------
    #  Create MCP server
    # -------------------------------------
    result = client.mcp.create(
        auth_config_ids=[auth_config_id],
        name="gmail-server",
        allowed_tools=[
            "GMAIL_FETCH_EMAILS",
            "GMAIL_GET_ATTACHMENT",
            "GMAIL_CREATE_EMAIL_DRAFT",
            "GMAIL_DELETE_DRAFT",
            "GMAIL_LIST_DRAFTS",
        ],
        managed_auth_via_composio=False,
    )

    # -------------------------------------
    #  Return user-specific MCP server URL
    # -------------------------------------
    return result.mcp_url.replace("transport=sse", f"user_id={user_id}")


def main():
    client = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))    
    user_id = "martin"
        
    gcal_mcp_url = setup_googlecalendar(client, user_id)
    print(f"URL of Google Calendar MCP server: {gcal_mcp_url}")

    gmail_mcp_url = setup_gmail(client, user_id)
    print(f"URL of Gmail MCP server: {gmail_mcp_url}")
    
    # Write URLs to JSON file
    mcp_urls = {
        "gcal": gcal_mcp_url,
        "gmail": gmail_mcp_url
    }
    
    with open("examples/mcp_server_urls.json", "w") as f:
        json.dump(mcp_urls, f, indent=2)

    print("MCP server URLs saved to examples/mcp_server_urls.json")


if __name__ == "__main__":
    main()
