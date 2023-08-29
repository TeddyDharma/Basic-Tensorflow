#!/usr/bin/env python3
import re
import csv
import operator

pesan_error = {}
all_user = {}
logfile_location =r"/home/student-01-4f871d25f95d/syslog.log"
pola = r"(INFO|ERROR) ([\w' ]+|[\w\[\]#' ]+) (\(\w+\)|\(\w+\.\w+\))$"

with open(logfile_location, "r") as f:
 for baris in f:
  hasil = re.search(pola, baris)
#  cek hasil pencarian, jika isi nya tidak ada maka kembalikan None
  if hasil is None:
   continue
# jika hasil dari hasil.groups()[0] == INFO
  if hasil.groups()[0] == "INFO":
   kategori = hasil.groups()[0]
   message = hasil.groups()[1]
   name = str(hasil.groups()[2])[1:-1]
   if name in all_user:
    user = all_user[name]
    # melakukan proses increment jika nama ada di dalam all_user
    user[kategori] = user[kategori] + 1
   else:
    all_user[name] = {'INFO':1, 'ERROR':0}
# jika hasil dari hasil.groups()[0] == INFO
  if hasil.groups()[0] == "ERROR":
   kategori = hasil.groups()[0]
   message = hasil.groups()[1]
   name = str(hasil.groups()[2])[1:-1]
   pesan_error[message] = pesan_error.get(message, 0) + 1
   if name in all_user:
    user = all_user[name]
    user[kategori] = user[kategori] + 1
   else:
    all_user[name] = {'INFO':0, 'ERROR':1}

pesan_terurut = [("Error", "Count")] + sorted(pesan_error.items(), key = operator.itemgetter(1), reverse=True)
user_terurut = [("student-01-4f871d25f95d", "INFO", "ERROR")] + sorted(all_user.items())[0:8]
with open("error_message.csv", "w") as error_file:
 for baris in pesan_terurut:
  error_file.write("{}, {}\n".format(baris[0], baris[1]))

with open("user_statistics.csv", "w") as user_file:
 for baris in user_terurut:
  if isinstance(baris[1], dict):
   user_file.write("{}, {}, {}\n".format(baris[0], baris[1].get("INFO"), baris[1].get("ERROR")))
  else:
   user_file.write("{}, {}, {}\n".format(baris[0], baris[1], baris[2]))


if not re.match('[A-Z, 0-9._]*$')