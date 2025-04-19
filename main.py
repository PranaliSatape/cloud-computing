# main.py

from cryptography.fernet import Fernet
import dropbox

print("Starting the script...")  # Debug statement

# ======= 1. KEY MANAGEMENT =======

def generate_key():
    print("Generating key...")  # Debug statement
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    print("Loading key...")  # Debug statement
    return open("secret.key", "rb").read()

# ======= 2. ENCRYPTION / DECRYPTION =======

def encrypt_note(data, key):
    print("Encrypting note...")  # Debug statement
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_note(data, key):
    print("Decrypting note...")  # Debug statement
    f = Fernet(key)
    return f.decrypt(data).decode()

# ======= 3. DROPBOX UPLOAD / DOWNLOAD =======

ACCESS_TOKEN = "sl.u.AFpE96DfsHdj82jfqRplny0mV6WjrdheJKdte2XCAC3Z3EUvftLRQcKaWoFiXknaimkHxSERqR3tJZonjEDOuqetQOEZz18ld4m8rwLuPjr9d4dXVE1Xhru2rhZ3eDmZXpmN-yegW5ZOCpzJB8hLKCBkNBKUwwbvsiyVI6A5v2i7NB860e6ZfNUXoTixtowjcDL_MmRA18kp0O1IrchOoSOMZMEDSDlo9cIEwsFDnARzXtCpVvyHfh8wCx2p-biUoUcvHHV7OhsGMjozGk9K84PbE8irEKcq-YuUvd-ZiOcmHG1Lu0R_5gLxZn2ZgEhCxDHSzW__7qSYuBQu8sge_J6q_3pdDL58ySc-n3e3VAOPPZUSTrw16qarKgW-DV2CTBwBn8bc16gqv8rDjNCpcduwMs_FcnKRmsaA7wVsGrAv_Fe9OsDVCBCVqYEZIP4H1sLDObEs6Tn7tN6LgtaHuCyxk2Ikm8wlKc6cXJx6muVV-FSkfm_S2yk7K0AJdBzcAjzfUS6GEjv9fQVJctzA-KhhCZ2mXkDiyF6rDe0StIscegQDQlAHWKVakfdm_CDh331fSEMGdm50ZK-wgXrmP7HMM24NiEP4u2brDkRh8a81zMzY_Amb9eWpsc8Lo0Y833ZgPv4CbyzrKcAYHLbZnjjfeCmMJBW7nLfQeZmaJx8cCwrwvadqYryZckiNcPSLSQAouMhSVC8rm72GMlS4A1EJ4BJkCzUXcqMkhuuzRenKAqUMtaAL-IxhGfi7Gg-lkQUTy2ssoEYzWIydpP0JFMqJnNDv-ZkrZPooBjnDyoLjczCTwFXtDbKI_J7lLPGIaR-OS6-dYiVoKw81mSSV1gR8bB7ASHLxNTjM-Z8LB-eff8-ztJsil4RTH2nd1Xi1iBXqs6-KMeoPrlP6DF7hp5G16k0tXzHEfe1ucQFFFUvWssy0F0h6gw9IL2qlMbEkoVccyTq1wr0vFakZupt03kW4mNxko59x1BtzYZUYWNug0qKNNbmeSbZvulzlzI4Gch5890lNRL3XG---g8RK1ea9NA54LXxnpT1mDgIqKV4Kqoya6LHd5lDbX42GdivFv91Mnutuj0TAnsmhJkLhidlvGdj9YoGpJd9kKomzogMORlLUGKaeE4uLpMcIMCJ-I5jtuSH1JlPMhvn3GO-8Bz70vW5I2yXhZ9xWSttKz3KXMQMoZQWIKNvCoqc2Srzbvn57y5iPwSdgFiKgRrqriktQvH9yMSpmjrKYgQK8hKGRXXeSvQbMgHLjKVV99mWORGzsJDZN_xe7biZMheRiMqoheOgx1Hgskyk88AXorbKyOy7r0-K3TaiMe7SncZhMugs1IPkAbbymtcIOrwcfHgTBcfTrqRRZAQkltjN-K6pwaf-HOaLKqAKaFuWTgtBAtonJhfbcSweANivWVLzgCIUAE1Dwi8bZalf0dasBwqtq-g"
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def upload_to_dropbox(local_file, dropbox_path):
    print(f"Uploading {local_file} to Dropbox...")  # Debug statement
    with open(local_file, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
    print(f"✅ Uploaded to Dropbox: {dropbox_path}")

def download_from_dropbox(dropbox_path, local_file):
    print(f"Downloading {dropbox_path} from Dropbox...")  # Debug statement
    metadata, res = dbx.files_download(dropbox_path)
    with open(local_file, 'wb') as f:
        f.write(res.content)
    print(f"✅ Downloaded from Dropbox: {dropbox_path} ➜ {local_file}")

# ======= 4. MAIN FLOW =======

if __name__ == "__main__":
    print("Script is running...")  # Debug statement

    # Generate encryption key (only once, comment it out later)
    generate_key()

    # Load the encryption key
    key = load_key()

    # Get note input
    note = input("📝 Enter your note: ")

    # Encrypt the note
    encrypted_note = encrypt_note(note, key)

    # Save encrypted note to file
    with open("encrypted_note.txt", "wb") as f:
        f.write(encrypted_note)
    print("🔐 Note encrypted and saved locally.")

    # Upload to Dropbox
    upload_to_dropbox("encrypted_note.txt", "/encrypted_note.txt")

    # Download it back (for test)
    download_from_dropbox("/encrypted_note.txt", "downloaded_note.txt")

    # Decrypt downloaded note
    with open("downloaded_note.txt", "rb") as f:
        downloaded_encrypted_data = f.read()

    decrypted_note = decrypt_note(downloaded_encrypted_data, key)
    print(f"🔓 Decrypted note: {decrypted_note}")
