# client cert

This refers to client certificate credentials, which can be used to authenticate a device using a digital certificate.

from OpenSSL import crypto

# Generate private key
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

# Create CSR
req = crypto.X509Req()
req.get_subject().CN = 'ibshono.com'
req.set_pubkey(key)
req.sign(key, 'sha256')

# Print CSR and private key
print(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())
print(crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode())

# Obtain signed certificate from CA
# Send the CSR to the CA and follow their instructions for obtaining a signed certificate

{
    "type": "client-cert",
    "auth-id": "<auth_id>",
    "cert": "<base64 encoded client certificate>",
    "key": "<base64 encoded private key>"
}
# Public key
 
  Generating SSH Key Pair:

Open a terminal on your device or SSH into your device if it is a remote system.
  
Enter the following command to generate an SSH key pair: ssh-keygen -t rsa
  
You will be prompted to enter a file name to save the key pair. Press Enter to accept the default file name and location, or enter a new file name if you prefer.
  
You will then be prompted to enter a passphrase to encrypt the private key. You can choose to enter a passphrase or leave it blank for an unencrypted key.
  
The key pair will be generated and saved in the specified file location. By default, the public key file will have a .pub file extension.
  
# Creating Public Key Credentials:

To view the public key, enter the following command: cat ~/.ssh/id_rsa.pub
  
This will display the public key in the terminal. Copy the public key.
  
Use the following JSON format to create device credentials with the "public-key" authentication mechanism in Eclipse Hono:

{
  "type": "public-key",
  "auth-id": "<auth_id>",
  "public-key": "<base64 encoded public key>"
}

Replace <auth_id> with a unique identifier for the device, and <base64 encoded public key> with the public key you copied in the previous step.
Security Reminder:

Keep the private key file secure, as anyone who has access to the private key will be able to authenticate as the device.
  
# plain
"plain": This refers to user password credentials, which can be used to authenticate a device using a username and password.

{
    "type": "plain",
    "auth-id": "<auth_id>",
    "secrets": [
        {
            "pwd-plain": "<password>"
        }
    ]
}

# hmac
"hmac"(keyed-Hash Message Authentication Code): This refers to HMAC credentials, which can be used to authenticate a device using a shared secret key.

{
    "type": "hmac",
    "auth-id": "<auth_id>",
    "algorithm": "<hash algorithm>",
    "secrets": [
        {
            "key": "<base64 encoded shared secret key>"
        }
    ]
}

[
    {
        "type": "hashed-password",
        "auth-id": "glucometer",
        "secrets": [
            {
                "pwd-hash": "LI97LTW1UMQfmrEhtdy/IxDxuTDRgbTY7k/9NCANuCA=",
                "salt": "c2FsdHZhbHVl",
                "hash-function": "sha-512"
            }
        ]
    }
]
  
# oauth client credentials
  
"oauth-client-credentials": This refers to OAuth client credentials, which can be used to authenticate a device using the OAuth 2.0 client credentials grant type.

{
    "type": "oauth-client-credentials",
    "auth-id": "<auth_id>",
    "client-id": "<OAuth client ID>",
    "client-secret": "<OAuth client secret>",
    "grant-type": "<OAuth grant type>"
}

  

These are some of the types of credentials that can be used for device onboarding in Eclipse Hono.
  

Eclipse Hono provides a pluggable authentication and authorization framework, which allows developers to implement custom authentication and authorization mechanisms as needed.
  
  
 Therefore, it is possible to have additional credential types beyond the five built-in types (client-cert, public-key, plain, hmac, and oauth-client-credentials) if they are implemented by the developer.
 
  
  However, these five types are the ones that are provided out of the box with Hono.
