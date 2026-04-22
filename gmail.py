import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from tools.claude import TicketResolver
from business_logic.data_logic import Data_Logic
import time

class GmailAIResponder:
    def __init__(self, email_user, email_pass):
        self.user = email_user
        self.password = email_pass
        self.imap_url = 'imap.gmail.com'
        self.smtp_url = 'smtp.gmail.com'

    def get_ai_response(self, original_content):
        return Data_Logic().search_results(original_content)
       
    def process_emails(self, target_domain="@fareye.com"):
        try:
            # 1. Connect to Inbox
            mail = imaplib.IMAP4_SSL(self.imap_url)
            mail.login(self.user, self.password)
            mail.select('inbox')

            # Search for unread emails
            status, data = mail.search(None, 'UNSEEN')
            
            for num in data[0].split():
                status, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        sender = msg['from']
                        subject = msg['subject']

                        
                        if target_domain in sender.lower():
                            print(f"Match found! From: {sender}")
                            
                           
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                            else:
                                body = msg.get_payload(decode=True).decode()

                            
                            ai_reply = self.get_ai_response(body)
                            self.send_reply(sender, subject, ai_reply)
            
            mail.logout()

        except Exception as e:
            print(f"Error: {e}")

    def send_reply(self, to_email, subject, content):
        msg = MIMEText(content)
        msg['Subject'] = f"Re: {subject}"
        msg['From'] = self.user
        msg['To'] = to_email

        with smtplib.SMTP_SSL(self.smtp_url, 465) as server:
            server.login(self.user, self.password)
            server.sendmail(self.user, to_email, msg.as_string())
            print(f"AI response sent to {to_email}")


EMAIL_ID = "aisupportengine@gmail.com"
APP_PASSWORD = "bjoctuvdvrcsfrma" # The 16-character code from Google


bot = GmailAIResponder(EMAIL_ID, APP_PASSWORD)

print("Bot is starting... Press Ctrl+C to stop.")


while True:
    print("Checking for new emails from @fareye.com...")
    bot.process_emails(target_domain="@fareye.com")
    
    
    time.sleep(60)