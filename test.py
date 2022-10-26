from main import *



my_root = File(0, "root")
create_file(0, "muneeb", my_root)
create_file(0, "haseeb", my_root)
current_dir = change_dir(my_root, "muneeb")
create_file(1, "m.txt", current_dir)
append_text("m.txt", current_dir, "haseeb")
create_file(1, "b.txt", current_dir)
append_text("b.txt", current_dir, "muneeb")
create_file(1, "c.txt", current_dir)
append_text("c.txt", current_dir, "tayyab")

append_text("b.txt", current_dir, "abcdefghijkl")
append_text("b.txt", current_dir, "mnopqrstuv")


read_file_from("b.txt", current_dir, 2, 11)

for pre,fill,node in RenderTree(my_root):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(8))
    print(node.file_blocks)

print(f"free block {free_blocks}")

block_obj_read.close()
