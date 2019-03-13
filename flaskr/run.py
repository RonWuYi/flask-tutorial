import os
import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


subprocess_cmd('cd /usr/local/bin ; ./virtualenvwrapper.sh ; workon flask001 ; cd ~/PycharmProjects/flask-tutorial/flaskr ; pwd')
# os.system()
# os.system('FLASK_APP=__init_.py')
# os.system('flask run')
# /usr/local/bin/virtualenvwrapper.sh
