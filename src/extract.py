# src/extract.py
import os
import base64
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.auth.transport.requests import Request # type: ignore
from googleapiclient.discovery import build # type: ignore
from config_reader import load_config

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_gmail_service():
    cfg = load_config()
    cred_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cfg["GOOGLE"]["credentials_json"]))
    token_path = os.path.abspath(os.path.join(os.path.dirname(__file__), cfg["GOOGLE"]["token_json"]))

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def extract_emails(max_results=20):
    cfg = load_config()
    query = cfg["GOOGLE"].get("gmail_query", "is:unread")
    service = get_gmail_service()

    # Get message IDs
    resp = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    messages = resp.get("messages", [])
    output = []

    for msg in messages:
        msg_id = msg["id"]

        # Get full message
        full = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        payload = full.get("payload", {})
        headers = {h["name"].lower(): h["value"] for h in payload.get("headers", [])}

        # Extract body (simple: only text/plain)
        body = ""
        parts = payload.get("parts", [])

        for p in parts:
            if p.get("mimeType") == "text/plain":
                data = p.get("body", {}).get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        # Extract attachments (simple)
        attachments = []
        for p in parts:
            if p.get("filename"):
                att_id = p["body"].get("attachmentId")
                att = service.users().messages().attachments().get(
                    userId="me", messageId=msg_id, id=att_id
                ).execute()
                file_bytes = base64.urlsafe_b64decode(att["data"])
                attachments.append({
                    "filename": p["filename"],
                    "data_bytes": file_bytes
                })

        output.append({
            "message_id": msg_id,
            "from": headers.get("from"),
            "to": headers.get("to"),
            "subject": headers.get("subject"),
            "body": body,
            "attachments": attachments
        })

    return output


# Quick test if the emails are extracting or not, extract the first one
if __name__ == "__main__":
    emails = extract_emails()
    print("Extracted:", len(emails),'\n')
    print('Here is the first email:')
    if emails:
        print(emails[1])
