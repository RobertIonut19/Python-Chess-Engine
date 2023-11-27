from file_merger import merger

file_paths = ['file_1.txt', 'file_2.txt', 'file_3.txt']
output = '/Users/robertrascanu/Documents/Facultate/PY/test/output.txt'
custom_separator = '\n\n----+-+-+-+-+-+-+-+-+-+-+-+----\n\n\n'

merger.merge_files(file_paths, output, custom_separator)

print(f"Output file: {output}")
