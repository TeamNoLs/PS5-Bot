import smtplib, ssl

# Global Vars
password = "Infussy1@1"
email = 'whatisthebestway27@gmail.com'
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = 'whatisthebestway27@gmail.com'  # Enter your address
receiver_email = "taj8zg@virginia.edu"  # Enter receiver address
password = "Infussy1@1"

class email_bot:
    def __init__(self, store):
        self.store = store
        self.message = f"""\
            {store} PS5 yuhhhhhhhhhhh.
            
            Happy Christmas
            
            This message is sent from Python(dork)."""

    def run(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, self.message)