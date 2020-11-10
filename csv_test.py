import csv

def get_source_list(file_path: str):
    """
    获取下载资源的路径列表
    :param file_path: 这是列表文件的路径，从列表文件中获取需要下载的资源列表
    :return: 返回所有资源文件列表的路径，以数组形式返回
    """
    path_list = []
    f = open(file_path, "r")
    raw_data = f.read().splitlines()
    for line in raw_data:
        path_list.append([line.split("\t")[1]])
    f.close()
    return path_list


source_list = get_source_list("source_list/id_pdf_path.txt")

f = open("source_list/csv.csv", "w", encoding="utf-8", newline="")
csv_writer = csv.writer(f)

for row in source_list:
    csv_writer.writerow(row)

f.close()


