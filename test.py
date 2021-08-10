from cryptography.fernet import Fernet

message = "hello geeks"

key = Fernet.generate_key()
fernet = Fernet(key)
encMessage = fernet.encrypt(message.encode())
print("original string: ", message)
print("encrypted string: ", encMessage)
decMessage = fernet.decrypt(encMessage).decode()
print("decrypted string: ", decMessage)

# convert bytes to strings
string_encMessage = encMessage.decode("utf-8")
print("convert string encrypted: ",string_encMessage)

# decrypted string

print(fernet.decrypt(string_encMessage.encode()).decode())
