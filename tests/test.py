from Algorithms import parse_file, dijkstra, augmenting_paths_method
import os


def main():
    #dfg = parse_file("Instances/inst-100-0.1.txt")
    dfg = parse_file("tests/testgraph.txt")
    print(augmenting_paths_method(dfg))

if __name__ == "__main__":
    main()



# def check_files_for_duplicates(folder_path):
#     file_list = os.listdir(folder_path)
#     for filename in file_list:
#         filepath = os.path.join(folder_path, filename)
#         if os.path.isfile(filepath):
#             duplicates = find_duplicates(filepath)
#             if duplicates:
#                 for node, target_node in duplicates:
#                     print(f"Duplicates found File: {filename}")
#                     print(f"Node {node} to target node {target_node}")
#                     input()
#             else:
#                 print("No duplicates found.")
#             print()
#
# def find_duplicates(file_path):
#     duplicates = set()
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         sink = lines[2][5:]
#         for line in lines[4:]:
#             node, target_node, _ = line.strip().split(' ')
#             if (node, target_node) in duplicates:
#                 if((int(node),int(target_node)) == (0,int(sink))):
#                     pass
#                 else:
#                     return [(node, target_node)]
#             duplicates.add((node, target_node))
#     return None
#     # Specify the folder path where the files are located
#     folder_path = 'instances'
#
#     # Call the function to check files for duplicates
#     check_files_for_duplicates(folder_path)


