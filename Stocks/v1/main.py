from kiteconnect import KiteConnect

api_key = "4e6s7q03hj8ji7lr"
request_token = "Vb9Xm1mpgtljfgKQ0fwRhrF0eZczYrHW"


kite = KiteConnect(api_key=api_key)

# Generate session and get access token
session = kite.generate_session(request_token, api_secret)
access_token = session["access_token"]

# Set the access token for subsequent API calls
kite.set_access_token(access_token)

# Now you can make API calls
profile = kite.profile()
print(profile)

