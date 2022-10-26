from anytree import NodeMixin, Node, RenderTree, findall
import pickle


BLOCK_SIZE = 10

block_obj_read = open("blocks.txt", "r+")
free_blocks = block_obj_read.readline().split(',')[:-1] # read all blocks except last

# returns first free block
def get_free_block():
    return free_blocks[0];

# remove first free block from free block list
def remove_free_block():
    return free_blocks.pop(0)

# maintains file structure
class File(NodeMixin):
    # fileLoc is an array that shows the block which contain this file's data
    def __init__(self, file_dir, name, parent=None, children=None):
        super(File, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children
        self.file_dir = file_dir
        if (file_dir == 1):  # if file (not directory) then assign it free block
            self.file_blocks = [get_free_block()]
            remove_free_block()
        else:
            self.file_blocks = []

    def delete_file(self):
        print("deleted", name)
        # remove the parent
        self.parent = None
        # add this file location to free space

    def add_block(self):
        if len(free_blocks)<=1: return -1
        self.file_blocks.append(get_free_block())
        return remove_free_block()


# with open('sample.dat', 'wb') as file_structure:
#     pickle.dump(f1, file_structure)

# with open('sample.dat', 'rb') as file_structure:
#     abc = pickle.load(file_structure)
#     print(abc.children[0].name)



# make file/directory
def create_file(dir_file, name, parent): # dir_file if 1 = file, if 0 = directory
    print("Creating file")
    # if the name already exists in parent directory then throw error
    for c in parent.children:
        if c.name == name:
            print("this file already exists in current director")
            return
    # get one free block for file, if not available throw error
    if ((dir_file ==1) and (len(free_blocks) <= 1)):
        print("no free blocks available")
        return

    File(dir_file, name, parent)

# returns the file if it exists, else returns current directory
def file_found(file_name, cur_dir):
    for c in cur_dir.children:
        if c.name == file_name:
            if c.file_dir == 0:
                return 0, c # it is a directory
            else:
                return 1, c # it is a file

    return -1, cur_dir  # file doesn't exists

# returns another directory if it exists
def change_dir(current_dir, dir_name):
    flag, new_dir = file_found(dir_name, current_dir)
    if (flag == 1):
        print(f"{dir_name} is a file not directory!")
        return current_dir
    elif (flag == -1):
        print("no such file or directory")
        return current_dir
    else:
        print("directory exists")
        return new_dir

# takes line number to read and returns the line data and its starting seek position
def read_line(line_num):
    block_obj_read.seek(0)
    seek_pos = 0
    for i in range(int(line_num)):
        block_obj_read.readline()
        seek_pos = block_obj_read.tell()
    file_line = block_obj_read.readline()
    return file_line.strip('\n'), seek_pos

# append characters at the end of file
def append_text(file_name, cur_dir, text):
    # check if file exists in the directory
    flag, my_file = file_found(file_name, cur_dir)

    # get the last block number used by the file
    last_block = my_file.file_blocks[-1]

    # read the next line as well because "seek" deletes some data from next line
    file_line, seek_pos = read_line(int(last_block))
    next_line, next_seek_pos = read_line(int(last_block)+1)
    if (len(file_line)+len(text)>3*BLOCK_SIZE):
        print(f"cant write more than {3*BLOCK_SIZE} characters in one file")
        return
    else:
        while (True):
            if len(file_line)+len(text) < BLOCK_SIZE:
                block_obj_read.seek(seek_pos)
                block_obj_read.write(file_line+text+'\n')
                block_obj_read.write(next_line+'\n')
                break
            else:
                block_obj_read.seek(seek_pos)
                write_char = text[0:BLOCK_SIZE-len(file_line)]
                text = text[BLOCK_SIZE-len(file_line):]
                block_obj_read.write(file_line+write_char+'\n')
                block_obj_read.write(next_line+'\n')
                last_block = my_file.add_block()
                if last_block == -1:
                    print("some data is not stored because of shortage of memory")
                    break
                file_line, seek_pos = read_line(int(last_block))
                next_line, next_seek_pos = read_line(int(last_block)+1)

# def write_at(fie_name, cur_dir, start, text):

# returns entire data of a file
def read_file_seq(file_name, cur_dir):
    flag, my_file = file_found(file_name, cur_dir)
    if (flag != 1):
        print(f"no such file {file_name}")
        return "-1"
    file_data = ""
    for i in my_file.file_blocks:
        file_line, seek_pos = read_line(int(i))
        file_data += file_line
    print("sequential data: ", file_data)
    return file_data

# read file from 'start' index and get 'size' characters
def read_file_from(file_name, cur_dir, start, size):
    file_data = read_file_seq(file_name, cur_dir)
    if (len(file_data)<=start):
        print("Starting position is greater than file data length")
        return "-1"
    elif (start+size>len(file_data)):
        print("Size is bigger than file. Can't read outside file")
        return "-1"
    print("from data: ", file_data[start:start+size])
    return file_data[start:start+size]

# returns size of file. If doesn't exists returns -1
def file_size(file_name, cur_dir):
    file_data = read_file_seq(file_name, cur_dir)
    if file_data == "-1":
        print(f"no such file {file_name}")
        return -1
    else:
        return len(file_data)

