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
            
        # THE FIX: Split ONLY on 4 or more consecutive line breaks.
        # This bypasses paragraph spacing and only catches the gaps between distinct notes.
        notes = re.split(r'\n(?:\s*\n){3,}', content)
        
        saved_count = 0
        for note in notes:
            note = note.strip()
            # Clean out any artifacts like "" that might have snuck in during the text export
            note = re.sub(r'^\\s*', '', note).strip()
            
            if not note:
                continue
                
            lines = note.split('\n')
            first_line = lines[0].strip()
            body_text = '\n'.join(lines[1:]).strip()
            
            # Clean the filename of illegal OS characters
            safe_title = re.sub(r'[\/\?<>\\:\*\|"]', '', first_line).strip()
            
            # Enforce a safe character limit for macOS
            if len(safe_title) > 200:
                safe_title = safe_title[:200].strip() + "..."
                body_text = f"{first_line}\n\n{body_text}".strip()
            
            if not safe_title:
                safe_title = f"Untitled_Note_{saved_count + 1}"
                
            out_filepath = os.path.join(output_dir, f"{safe_title}.md")
            
            with open(out_filepath, 'w', encoding='utf-8') as out_f:
                if body_text:
                    out_f.write(body_text + '\n')
                    
            saved_count += 1
            
        print(f"✅ Processed '{base_filename}': Saved {saved_count} notes into '/{folder_name}'")

    print("\nAll files have been successfully processed!")

# --- Setup ---
BATCH_FOLDER = "Keep_Exports"
process_note_batches(BATCH_FOLDER)