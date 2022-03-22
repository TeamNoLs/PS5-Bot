import smtplib, ssl

# Global Vars
# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = 'whatisthebestway27@gmail.com'  # Enter your address
# receiver_email = "taj8zg@virginia.edu"  # Enter receiver address
# password = "Infussy1@1"

class email_bot:
    def __init__(self):
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = 'whatisthebestway27@gmail.com'  # Enter your address
        self.receiver_email = "taj8zg@virginia.edu"  # Enter receiver address
        self.password = "Infussy1@1"

    def run(self, store="Should've input a store (doofus)"):
        self.store = store
        self.message = f"""\
            {store} PS5 yuhhhhhhhhhhh.
            
            Happy Christmas
            
            This message is sent from Python(dork)."""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.message)



# Result: It works but message gets sent to spam unless the reciever marks the account
#         I'm cool with that for a free solution.
#         I need to remove the personal info, but this was just testing and its a 
#         throwaway email so I really couldn't care less.