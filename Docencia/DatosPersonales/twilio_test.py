from twilio.rest import Client
 
# Find these values at https://twilio.com/user/account
account_sid = "AC97c38c7a979b98db0414eab5bcb8821e"
auth_token = "7a27a3852a6db5ff07218adcf99b01d9"
client = Client(account_sid, auth_token)
my_number = "+12074050121"
to = "+5353861204"

message = client.messages.create(
            body='Holaaaaaaa, twilio test',
            from_=my_number,
            to=to
        )
message.send()