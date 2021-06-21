import sys, socket, os, re, time
from index import Index

THREADS = 32 # num of threads processing the queue

def process_file_name_and_text(path):
    with open(path) as f:
        return path.replace("/","\\"), f.read()

def load_directories(path):
    docs = [path]
    while docs:
        top = docs.pop()
        if os.path.isdir(top):
            for i in os.listdir(top):
                abs_path = os.path.join(top, i)
                docs.append(abs_path)
        elif top.endswith('.txt'):
            try:
                yield process_file_name_and_text(top) # generators
            except:
                pass

def create_dictionary_index(path):
    index = Index()
    docs_from_load = load_directories(path)
    start_time = time.perf_counter()
    index.bulk_index(docs_from_load, threads=THREADS)
    print("%s lasts to process 2000 files with %s threads" % (time.perf_counter() - start_time, THREADS))
    return index

def main():
    print(sys.argv)
    if len(sys.argv) == 2:
        path = sys.argv[1]
        print('Inverted index would be created on data from folder %s' % path)
        index = create_dictionary_index(path)

    # local - console
    # print('Enter word to get top 10 documents that contains it')
    # while True:
    #     try:
    #         token = input('\nInput: ')
    #         print(index.get_documents_containing_word(token, count=10, text_=True))
    #     except KeyboardInterrupt:
    #         break

    # socket solution - https://habr.com/ru/post/149077/

    print('Sent info from client to get top documents contains the word')
    while True:
        sock = socket.socket()
        sock.bind(('', 9090)) # on port 9090
        sock.listen(10)
        conn, addr = sock.accept()

        while True:
            try:
                data = conn.recv(1024)
            except: # connection closed
                break
            if not data:
                break

            client_res_list = data.decode().replace("'","").strip(')(').split(', ')
            word = client_res_list[0]
            count = int(client_res_list[1])

            if client_res_list[2].lower() == "y":
                send_text = True
            else:
                send_text = False

            index_res = index.get_documents_containing_word(word, count, text_=send_text)

            print(str(len(index_res)) + " Docs was sent to " + str(addr))
            conn.send(str(index_res).encode())
        conn.close()


if __name__ == '__main__':
    main()
