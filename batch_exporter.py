import os
import re
import glob

def process_note_batches(target_folder):
    if not os.path.exists(target_folder):
        print(f"Error: The folder '{target_folder}' does not exist.")
        return

    search_pattern = os.path.join(target_folder, '*.txt')
    text_files = glob.glob(search_pattern)

    if not text_files:
        print(f"No .txt files found in '{target_folder}'.")
        return

    print(f"Found {len(text_files)} files to process. Starting export...\n")

    for filepath in text_files:
        base_filename = os.path.basename(filepath)
        folder_name = os.path.splitext(base_filename)[0]
        
        output_dir = os.path.join(target_folder, folder_name)
        os.makedirs(output_dir, exist_ok=True)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split on 4 or more consecutive line breaks
        notes = re.split(r'\n(?:\s*\n){3,}', content)
        
        saved_count = 0
        for note in notes:
            note = note.strip()
            note = re.sub(r'^\s*', '', note).strip()
            
            if not note:
                continue
                
            lines = note.split('\n')
            first_line = lines[0].strip()
            
            # --- ULTIMATE SAFEGUARD: Keep the entire raw note as the body ---
            # This guarantees 100% no data loss.
            body_text = note
            
            # --- BETTER FILENAMES FOR LINKS ---
            # Check if the first line contains a URL
            url_match = re.search(r'https?://(?:www\.)?([^/\s]+)', first_line, re.IGNORECASE)
            
            if url_match:
                # Extract just the domain (e.g., 'yourstory.com')
                clean_domain = re.sub(r'[\/\?<>\\:\*\|"]', '', url_match.group(1))
                safe_title = f"Link - {clean_domain}"
            else:
                # Standard OS character cleaning for normal text titles
                safe_title = re.sub(r'[\/\?<>\\:\*\|"]', '', first_line).strip()
            
            # Enforce OS length limit
            if len(safe_title) > 150:
                safe_title = safe_title[:150].strip() + "..."
                
            if not safe_title:
                safe_title = f"Untitled_Note"
                
            # --- DUPLICATE HANDLING ---
            # Prevent files with the same name from overwriting each other
            base_safe_title = safe_title
            out_filepath = os.path.join(output_dir, f"{safe_title}.md")
            counter = 1
            
            while os.path.exists(out_filepath):
                safe_title = f"{base_safe_title} ({counter})"
                out_filepath = os.path.join(output_dir, f"{safe_title}.md")
                counter += 1
                
            # Write the file
            with open(out_filepath, 'w', encoding='utf-8') as out_f:
                out_f.write(body_text + '\n')
                
            saved_count += 1
            
        print(f"✅ Processed '{base_filename}': Saved {saved_count} notes into '/{folder_name}'")

    print("\nAll files have been successfully processed!")

# --- Setup ---
BATCH_FOLDER = "Keep_Exports"
process_note_batches(BATCH_FOLDER)
