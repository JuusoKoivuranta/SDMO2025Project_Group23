
import lmstudio as lms
import sys, io
import pandas as pd
import os
import csv

from pydriller import Repository
DEVS = set()
for commit in Repository("https://github.com/dspsir/SMP-FFmpeg").traverse_commits():
    DEVS.add((commit.author.name, commit.author.email))
    DEVS.add((commit.committer.name, commit.committer.email))

DEVS = sorted(DEVS)

with open(os.path.join("project1devs", "devs.csv"), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerow(["name", "email"])
    writer.writerows(DEVS)


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the CSV file
csv_data = pd.read_csv("project1devs/devs.csv")

# Process in chunks to avoid context overflow
chunk_size = 500
all_duplicates = []

print(f"Processing {len(csv_data)} developers in chunks of {chunk_size}...")

with lms.Client() as client:
    for i in range(0, len(csv_data), chunk_size):
        chunk = csv_data.iloc[i:i+chunk_size]
        chunk_content = chunk.to_string(index=False)
        
        print(f"\nProcessing chunk {i//chunk_size + 1}/{(len(csv_data)-1)//chunk_size + 1}...")
        
        prompt = f"""Find ALL duplicate developer pairs in this data (same person, different accounts):

{chunk_content}

Look for: identical names with different emails, similar names, same email patterns, name variations.
Output CSV format: name_1,email_1,name_2,email_2,reason
Include all combinations. Prioritize recall over precision.
Just output CSV - no analysis."""

        result = client.llm.model("openai/gpt-oss-20b").respond(prompt)
        response = str(result)
        
        # Extract CSV lines
        lines = response.split('\n')
        found_header = False
        
        for line in lines:
            line = line.strip()
            
            if 'name_1,email_1,name_2,email_2' in line:
                found_header = True
                continue
                
            if found_header and line:
                if line.count(',') >= 3 and '@' in line and not line.startswith('**'):
                    all_duplicates.append(line)
                elif line.startswith('**') or 'Summary' in line:
                    break

print(f"\nTotal duplicates found: {len(all_duplicates)}")

# Save all duplicates to CSV
if all_duplicates:
    with open("project1devs/llm_detected_duplicates.csv", 'w', newline='', encoding='utf-8') as f:
        f.write("name_1,email_1,name_2,email_2,reason\n")
        for dup in all_duplicates:
            f.write(dup + '\n')
    print(f"Successfully saved {len(all_duplicates)} duplicate pairs to 'project1devs/llm_detected_duplicates.csv'")
else:
    print("No duplicate pairs found.")