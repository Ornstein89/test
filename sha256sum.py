#!/usr/bin/python

'''
Аргументы:

–basedir - базовый каталог поиска файлов
–check <файл хэшей> - режим проверки, читает хэши и имена файлов из файл хэшей
–hash <файл хэшей> - режим вычисления, пишет хэши и имен файлов в файл хэшей
–num-cpus - количество используемых CPU (по-умолчанию - все доступные)
'''

import os, sys, argparse, tqdm, hashlib, re

def sha256_bigfile(filename : str) -> str:
    '''
    Функция для подсчёта хеш-функции sha256 файла
    '''
    file_to_calc = open(filename, "rb")
    hash_obj = hashlib.sha256()
    # print(file_to_calc.readlines())
    while True:
        chunk = file_to_calc.read(256)
        if not chunk:
            break
        hash_obj.update(chunk)
    file_to_calc.close()
    # print("hash_obj.hexdigest()=", hash_obj.hexdigest())
    return hash_obj.hexdigest()

#& python sha256sum.py --basedir testdir --hash hashfile.txt --num-cpus 2

if not __name__=="__main__":
    exit()

parser = argparse.ArgumentParser()

parser.add_argument('-b', '--basedir', type=str, nargs=1, default=[os.getcwd()],
                    help="Каталог, для файлов воторого нужно посчитать sha256", required=True)
parser.add_argument('-c', '--check', type=str, nargs=1,
                    help="Файл хешей, скрипт работает в режиме проверки", required=False)
parser.add_argument('-s', '--hash', type=str, nargs=1, default=["hashes_calculated.txt"],
                    help="Файл хешей, скрипт работает в расчёта и записи хешей", required=False)
parser.add_argument("--num-cpus", type=int, nargs=1, default=[os.cpu_count()],
                    help="Количество используемых CPU", required=False)                    
args = parser.parse_args()
print(args)

# if not os.path.exists(args.basedir[0]):
#     print("Ошибка. Путь --basedir=", args.basedir[0], " не существует. Работа скрипта прекращена.")
#     exit(-1)

check_mode = False
if (args.check is not None):
    correct_pattern = r"^([0-9a-fA-F])+\ \*([\w\d\.\ \(\)\_\-\+])+$"
    # print("correct_pattern=", correct_pattern)
    compiled_pattern = re.compile(correct_pattern)
    sha_file = open(args.check[0], "r+", encoding="utf-8")
    for nextline in sha_file:
        nextline = nextline.strip()
        # nextline = sha_file.readline()
        # if nextline is None:
        #     break
        #print("nextline=", nextline)
        #print("match()=", re.match(correct_pattern, nextline) )
        #print("fullmatch()=", compiled_pattern.fullmatch( nextline.strip() ))
        if compiled_pattern.fullmatch(nextline):
            print("Ошибка. Срока", nextline, "в файле", sha_file.name, "не соответствует формату")
            continue
        splitted = nextline.split(" *")
        hash_str = splitted[0]
        filename = splitted[1]
        # print("hash_str=", hash_str)
        # print("filename=", filename)
        if hash_str != sha256_bigfile(filename):
            print("Ошибка. Хеш файла",filename,"не соответствует записанному в ", sha_file.name)
            break
        else:
            print("OK",filename)

elif (args.hash is not None):
    sha_file = open(args.hash[0], "w+", encoding="utf-8")
    for root, dirs, files in os.walk(args.basedir[0]):
        for  filename in  files:
            #print("filename=", root + "\\" + filename)
            hash_value = sha256_bigfile(root + "\\" + filename)
            #print("hash_obj.hexdigest()=", hash_value)
            sha_file.write(hash_value + " *" + root + "\\" + filename + "\n")
sha_file.close()
# else:
#     print("Ошибка. Не задан ни параметр --hash, ни параметр --check. Работа скрипта прекращена.")
#     exit(-1)
