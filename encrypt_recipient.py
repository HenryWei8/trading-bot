from cryptography.fernet import Fernet
key = Fernet.generate_key()
print("STORE THIS AS YOUR SECRETS_KEY:", key.decode())
f = Fernet(key)
encrypted = f.encrypt(b"henryweihw@gmail.com")
print("YOUR ENCRYPTED_RECIPIENTS:", encrypted.decode())
#key = PihHVFK7rzYDT-T5wrW_jElSCXhGFnGmq88b2Om7_hI=
#Recipient = gAAAAABodCYgyy_W7SiEIt0AiA87-Fyuqd2Xo3fg6q4hBdGLiiLbQtVjGu_0m_fnBvvyr3fWFGHmszzGuD-VaGD0ReMSsarIkGEC0mHPOEEpE6HO1lH4YEI=