from Bio import Entrez, SeqIO
import pandas as pd
import time
import smtplib
from email.message import EmailMessage

Entrez.email = "your_personal_email@gmail.com"

# Use your improved query
query = '(("Human immunodeficiency virus 1"[Organism] OR hiv 1[All Fields]) AND pol gene[All Fields] AND pakistan[All Fields]) AND (is_nuccore[filter] AND ("900"[SLEN] : "3000"[SLEN]) AND ("2015/01/01"[PDAT] : "3000/12/31"[PDAT]))'

handle = Entrez.esearch(db="nucleotide", term=query, retmax=500)
record = Entrez.read(handle)
handle.close()
ids = record["IdList"]

print(f"Found {len(ids)} records.")

if not ids:
    print("No records found for the given query. Exiting.")
    exit()

with Entrez.efetch(db="nucleotide", id=ids, rettype="fasta", retmode="text") as handle:
    fasta_data = handle.read()

with open("hiv1_pol_pakistan.fasta", "w") as fasta_file:
    fasta_file.write(fasta_data)

metadata = []
for i in range(0, len(ids), 50):
    batch_ids = ids[i:i+50]
    with Entrez.efetch(db="nucleotide", id=batch_ids, rettype="gb", retmode="text") as handle:
        records = SeqIO.parse(handle, "gb")
        for record in records:
            accession = record.id
            length = len(record.seq)
            country = ""
            collection_date = ""
            for feature in record.features:
                if feature.type == "source":
                    qualifiers = feature.qualifiers
                    country = qualifiers.get("country", [""])[0]
                    collection_date = qualifiers.get("collection_date", [""])[0]
            metadata.append({
                "Accession": accession,
                "Collection Date": collection_date,
                "Country": country,
                "Sequence Length": length
            })
    time.sleep(1)

df = pd.DataFrame(metadata)
df.to_csv("hiv1_pol_metadata.csv", index=False)
df.to_excel("hiv1_pol_metadata.xlsx", index=False)

print("Data retrieval complete.")

# ----------- Email the files -----------
sender_email = "your_personal_email@gmail.com"
receiver_email = "your_personal_email@gmail.com"
app_password = "xxxxxxxxxxxxxxxxxxxx"  # <-- Replace with your Gmail App Password

subject = "HIV-1 pol FASTA and Metadata Files"
body = "Attached are the FASTA and metadata files you requested."

msg = EmailMessage()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.set_content(body)

files = ["hiv1_pol_pakistan.fasta", "hiv1_pol_metadata.csv", "hiv1_pol_metadata.xlsx"]
for file in files:
    with open(file, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)

print("Email sent with attachments.")
