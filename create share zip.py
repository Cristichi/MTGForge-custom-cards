import os
import shutil
import zipfile

def list_editions(editions_folder):
    return [f for f in os.listdir(editions_folder) if f.endswith('.txt')]

def parse_edition_file(filepath, starterdecks_folder):
    cards = []
    tokens = []
    decks = []
    code = ''
    with open(filepath, encoding='utf-8') as f:
        section = None
        for line in f:
            line = line.strip()
            if line.startswith('Code='):
                code = line.split('=')[1].strip()
            if line.startswith('['):
                section = line.lower()
            elif section == '[cards]' and line and not line.startswith('#'):
                parts = line.split('@')[0].strip().split(' ', 2)
                if len(parts) == 3:
                    card_name = parts[2].strip()
                    cards.append(card_name)
            elif section == '[tokens]' and line and not line.startswith('#'):
                parts = line.split('@')[0].strip().split(' ', 1)
                if len(parts) == 2:
                    token_name = parts[1].strip()
                    tokens.append(token_name)

    for fname in os.listdir(starterdecks_folder):
        if "["+code+"]" in fname:
            decks.append(fname)
    return cards, tokens, decks

def find_card_file(card_name, src_folder):
    letter = card_name[0].lower()
    card_dir = os.path.join(src_folder, letter)
    if not os.path.isdir(card_dir):
        return None
    for fname in os.listdir(card_dir):
        if fname.endswith('.txt'):
            fpath = os.path.join(card_dir, fname)
            try:
                with open(fpath, encoding='utf-8') as f:
                    for line in f:
                        if line.strip().lower().startswith('name:'):
                            file_card_name = line.strip()[5:].strip()
                            if file_card_name.lower() == card_name.lower():
                                return fpath
                            break
            except Exception as e:
                print(f"Error reading {fpath}: {e}")
    return None

def copy_cards(cards, src_folder, dest_folder):
    for card in cards:
        letter = card[0].lower()
        src_path = find_card_file(card, src_folder)
        dest_dir = os.path.join(dest_folder, letter)
        os.makedirs(dest_dir, exist_ok=True)
        if src_path:
            shutil.copy2(src_path, os.path.join(dest_dir, os.path.basename(src_path)))
        else:
            print(f"Warning: Card script file not found for card name: {card} (make sure it's a real card)")

def copy_tokens(tokens, src_folder, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    for token in tokens:
        src_path = os.path.join(src_folder, f"{token.lower().replace(' ', '_')}.txt")
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(dest_folder, os.path.basename(src_path)))
        else:
            print(f"Warning: Token file not found: {src_path}")

def copy_decks(decks, src_folder, dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    for deck in decks:
        src_path = os.path.join(src_folder, deck)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(dest_folder, os.path.basename(src_path)))
        else:
            print(f"Warning: Deck file not found: {src_path}")

def get_expansion_code(edition_file):
    with open(edition_file, encoding='utf-8') as f:
        for line in f:
            if line.strip().lower().startswith('code='):
                return line.strip().split('=', 1)[1].strip()
    return None


def main():
    editions_folder = './editions'
    cards_folder = './cards'
    tokens_folder = './tokens'
    decks_folder = './starterdecks'
    share_folder = './share'
    custom_folder = os.path.join(share_folder, 'custom')
    custom_editions_folder = os.path.join(custom_folder, 'editions')
    custom_cards_folder = os.path.join(custom_folder, 'cards')
    custom_tokens_folder = os.path.join(custom_folder, 'tokens')

    custom_decks_folder = os.path.join(share_folder, 'decks')

    pics_folder = os.path.join(share_folder, 'pics')
    pics_cards_folder = os.path.join(pics_folder, 'cards')
    
    install_script_path = os.path.join(share_folder, "(CHECK README FIRST) Install custom cards.bat")
    readme_path = os.path.join(share_folder, "README.md")
    zip_path = os.path.join(share_folder, 'share.zip')

    editions = list_editions(editions_folder)
    print("Select edition files (separated by space, or 0 for all):")
    for idx, edition in enumerate(editions):
        print(f"{idx+1}: {edition}")
    print("0: All editions")
    choice = input("Enter the numbers of the editions you want to pack: ").strip()
    if choice == "0":
        selected_indices = list(range(len(editions)))
    else:
        selected_indices = [int(x)-1 for x in choice.split(' ') if x.strip().isdigit() and 1 <= int(x) <= len(editions)]

    # Clean share folder
    if os.path.exists(custom_folder):
        shutil.rmtree(custom_folder)
    if os.path.exists(custom_decks_folder):
        shutil.rmtree(custom_decks_folder)
    if os.path.exists(pics_cards_folder):
        shutil.rmtree(pics_cards_folder)

    # The folders
    os.makedirs(custom_cards_folder)
    os.makedirs(custom_tokens_folder)
    os.makedirs(custom_editions_folder)
    os.makedirs(pics_cards_folder)
    os.makedirs(custom_decks_folder)

    appdata = os.getenv('LOCALAPPDATA')

    for idx in selected_indices:
        # Get expansion info
        edition_file = os.path.join(editions_folder, editions[idx])
        expansion_code = get_expansion_code(edition_file)
        if not expansion_code:
            print(f"Warning: Could not find expansion code in edition file {editions[idx]}.")
            expansion_code = "UNKNOWN"

        cards, tokens, decks = parse_edition_file(edition_file, decks_folder)

        # Copy files
        edition_file = os.path.join(editions_folder, editions[idx])
        shutil.copy2(edition_file, os.path.join(custom_editions_folder, os.path.basename(edition_file)))

        copy_cards(cards, cards_folder, custom_cards_folder)
        copy_tokens(tokens, tokens_folder, custom_tokens_folder)
        copy_decks(decks, decks_folder, custom_decks_folder)

        # Copy images for each card
        forge_img_folder = os.path.join(appdata, 'Forge', 'Cache', 'pics', 'cards', expansion_code)
        pics_expansion_folder = os.path.join(pics_cards_folder, expansion_code)
        os.makedirs(pics_expansion_folder, exist_ok=True)

        for card in cards:
            img_filename = f"{card}.fullborder.png"
            img_path = os.path.join(forge_img_folder, img_filename)
            dest_img_path = os.path.join(pics_expansion_folder, img_filename)
            if os.path.exists(img_path):
                shutil.copy2(img_path, dest_img_path)
            else:
                print(f"Warning: Image file missing for card '{card}': {img_path}")

    # Compress both "custom", "pics", and the install script inside share.zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in ['custom', 'pics', 'decks']:
            folder_path = os.path.join(share_folder, folder)
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, share_folder)
                    zipf.write(abs_path, rel_path)
                # Ensure empty folders are included
                for d in dirs:
                    folder_abs_path = os.path.join(root, d)
                    rel_path = os.path.relpath(folder_abs_path, share_folder)
                    zip_info = zipfile.ZipInfo(rel_path + '/')
                    zipf.writestr(zip_info, '')
        # Add the install script to the zip
        install_script_src = os.path.join(os.path.dirname(__file__), "install custom cards.bat")
        if os.path.exists(install_script_src):
            zipf.write(install_script_src, os.path.basename(install_script_path))
        # Add the README file
        readme_src = os.path.join(os.path.dirname(__file__), "README.md")
        if os.path.exists(readme_src):
            zipf.write(readme_src, os.path.basename(readme_path))

    # Cleanup: remove generated files
    shutil.rmtree(custom_folder)
    shutil.rmtree(custom_decks_folder)
    shutil.rmtree(pics_folder)

    print(f"Share zip created at {zip_path}")

if __name__ == "__main__":
    main()