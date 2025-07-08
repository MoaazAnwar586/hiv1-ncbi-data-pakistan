# HIV-1 NCBI Metadata Retrieval (Pakistan)

This repository contains a Python script that retrieves metadata and sequence data for HIV-1 (pol gene) sequences from the NCBI Nucleotide database, specifically filtered for sequences originating from Pakistan.

## Features

- Queries NCBI for HIV-1 pol gene sequences from Pakistan (2015 onwards)
- Downloads FASTA sequences
- Extracts metadata including accession number, collection date, country, and sequence length
- Saves metadata to CSV and Excel files
- Optionally emails the results as attachments

## Requirements

Install the required Python packages using:

```bash
pip install -r requirements.txt

