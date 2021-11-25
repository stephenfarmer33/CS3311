import os

#create dummy folder

#variable path
path = '/folder' # ???
#get all file names in path
#names = os.listdir(path)
names = ['meow.pdf', 'bob.wer', 'cat.csv']
#parse through each file name, classifying into "valid" or "invalid"
valid = {'pdf', 'xlsx', 'docx', 'doc', 'csv'} #pdf, excel, word
valid_files = []
invalid_files = []

for f in names:
  s = f.split('.')
  ext = s[1]
  if ext in valid:
    valid_files.append(f)
  else:
    invalid_files.append(f)


#print out valid types as valid, invalid types as invalid
print('Valid Files:', valid_files)
print('Invalid Files:', invalid_files)
