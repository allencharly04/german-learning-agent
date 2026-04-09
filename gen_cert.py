from OpenSSL import crypto

print("Generating SSL certificate...")

k = crypto.PKey()
k.generate_key(crypto.TYPE_RSA, 2048)

cert = crypto.X509()
cert.get_subject().CN = "192.168.0.35"
cert.set_serial_number(1)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, "sha256")

open("cert.pem", "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
open("key.pem", "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

print("Done! cert.pem and key.pem created.")
print("Now run: python launch.py")
print("Then open on your phone: https://192.168.0.35:8764")
