import os, zipfile, shutil

src_dir = '_cache/downloads'
out_dir = '_cache/extracted'
os.makedirs(out_dir, exist_ok=True)

for item in os.listdir(src_dir):
    if item.endswith('.zip'):
        zip_path = os.path.join(src_dir, item)
        extract_to = os.path.join(out_dir, item[:-4])
        if not os.path.exists(extract_to):
            print(f'Extracting {item}...')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)

print('Extraction complete. Subdirectories:')
for d in os.listdir(out_dir):
    print(' ', d)
