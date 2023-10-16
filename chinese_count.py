import os

print("%101s | %6s" % ("File Name", "NUM"))
print("-"*110)

def count_chinese_chars(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                if not (file_path.endswith('.cc') or file_path.endswith('.c') or file_path.endswith('.h') or\
                        file_path.endswith('.sh') or file_path.endswith('.cu') or file_path.endswith('.l') or\
                        file_path.endswith('.y') or file_path.endswith('.def') or file_path.endswith('.cpp')):
                    continue
                if "/build/" in file_path:
                    continue
                if "gpu-app-collection/4.2/" in file_path:
                    continue
                if "gpu-app-collection/src/cuda/" in file_path:
                    continue
                if "sim_run_11.0/" in file_path:
                    continue
                if "hw_run/" in file_path:
                    continue
                
                print("%101s" % file_path, end="")
                with open(file_path, 'r', encoding='utf-8') as f:
                    self_count = 0
                    content = f.read()
                    for char in content:
                        if '\u4e00' <= char <= '\u9fff' or '\u3002' <= char <= '\u303f' or char == '\uff0c' or\
                           char == '\uff1f' or char == '\uff1a' or char == '\uff1b' or char == '\u201d' or char == '\u201c' or\
                           char == '\u2018' or char == '\u2019' or char == '\u300b' or char == '\u300a' or char == '\u3001' or\
                           char == '\u2014':
                            count += 1
                            self_count += 1
                    print(" | %6d" % self_count)
    return count

# 指定要搜索的文件夹路径
root_folder = './'
total_chars = count_chinese_chars(root_folder)

print("-"*110)
print("%101s   %6s words" % ("Total:", str(total_chars)))

print(f"\nTotal: All files in Folder '{root_folder}' have {total_chars} chinese words.")