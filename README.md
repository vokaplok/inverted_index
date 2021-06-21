# inverted_index
Inverted index creation and use with socket connection

# Dataset
The dataset is the list of reviews to films on Imb. It contains directories with txt files (sum of 2000 files)
The method for handling the files is located in inverted_index.py file at load_directories function.

# Usage
to process all files in a directory, before starting the program specify the path to files:
- to specify number of threads to process the directory, simply edit 
```
THREADS = 32
```
parameter in *inverted_index.py* (line 4)
```
python inverted_index.py files/path
```

After files are processed and index is created the program moves to endless loop and creates a socket connection.
For searching files containing needed word you need to launch the client application
```
python client_index_search.py
```
After launching the program will ask you to input the: 
1. word
1. num of docs to output
1. type of need the content of the file or name only   

# Example of server program
```
$ python inverted_index.py aclImdb
aclImdb\test\neg\3502_1.txt was added to queue
..................
aclImdb\test\neg\3500_1.txt was added to queue
44.7616943 lasts to process 2000 files with 32 threads
Sent info from client to get top documents contains the word
10 Docs was sent to ('127.0.0.1', 65214)
```
# Example of client program
```
Enter word: world
Enter count docs: 10
Receive text or not (y/n): n
[('aclImdb\\train\\unsup\\14994_0.txt', 1), ('aclImdb\\train\\unsup\\14991_0.txt', 1), ('aclImdb\\train\\unsup\\14989_0.txt', 1), ('aclImdb\\train\\unsup\\14981_0.txt', 1), ('aclImdb\\train\\unsup\\14958_0.txt', 1), ('aclImdb\\train\\unsup\\14952_0.txt', 1), ('aclImdb\\train\\unsup\\14944_0.txt', 1), ('aclImdb\\train\\unsup\\14950_0.txt', 1), ('aclImdb\\train\\unsup\\14941_0.txt', 1), ('aclImdb\\train\\unsup\\14929_0.txt', 1)]
```
