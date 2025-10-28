
import lmstudio as lms
import sys, io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the CSV file
csv_data = pd.read_csv("project1devs/devs.csv")
csv_content = csv_data.to_string()

with lms.Client() as client:
    prompt = f"""Please analyze this CSV data containing developer names and emails. 

{csv_content}

I need you to:
1. Identify possible duplicate developers (same person using different accounts) with high confidence
2. Look for similar names, email patterns, typos, variations, etc.
3. Output the duplicates in CSV format like this:
name_1,email_1,name_2,email_2,confidence_reason

Only include pairs you are highly confident are the same person. Be conservative with your matches.
After the CSV output, provide a brief summary of the duplicates found."""

    result = client.llm.model("openai/gpt-oss-20b").respond(prompt)
    response = str(result)
    print(response)
    
    # Extract CSV lines from the response
    csv_lines = []
    lines = response.split('\n')
    
    # Look for the header line
    found_header = False
    for line in lines:
        line = line.strip()
        
        # Check if this is the CSV header
        if 'name_1,email_1,name_2,email_2' in line:
            found_header = True
            csv_lines.append(line)
            continue
            
        # If we found the header, look for CSV data lines
        if found_header and line:
            # Check if line has the expected CSV structure (commas and emails)
            if line.count(',') >= 3 and '@' in line and not line.startswith('**'):
                csv_lines.append(line)
            elif line.startswith('**') or line.startswith('#') or 'Summary' in line:
                break
    
    # Save to CSV file
    if len(csv_lines) > 1:
        with open("project1devs/llm_detected_duplicates.csv", 'w', newline='', encoding='utf-8') as f:
            for line in csv_lines:
                f.write(line + '\n')
        print(f"\nSuccessfully saved {len(csv_lines)-1} duplicate pairs to 'project1devs/llm_detected_duplicates.csv'")
    else:
        print("\nNo duplicate pairs found or could not extract CSV data from response.")