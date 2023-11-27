def merge_files(files, output, separator='\n'):
    try:
        with open(output, 'w') as outfile:
            for fname in files:
                with open(fname) as infile:
                    file_contents = infile.read()
                    outfile.write(file_contents + separator)
    except Exception as e:
        print(f"Error: {e}")
