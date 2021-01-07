import paramiko
import sys
from subprocess import check_output

hostname = "bartolo.org"
port = 7722

# try:
username = sys.argv[1]
password = sys.argv[2]

if __name__ == "__main__":
    check_output('cd .. && git push', shell=True)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    stdin, stdout, stderr = ssh.exec_command("su -l " + username)

    stdin.write(password + '\n')
    stdin.flush()

    stdin, stdout, stderr = ssh.exec_command('bash letranproject/copiar.sh')

    for line in stdout.readlines():
        print('>>', line)

    ssh.close()

# except:
#     print("Error no servidor ni contraseña")