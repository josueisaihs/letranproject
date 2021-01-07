import paramiko
import sys
from subprocess import check_output

hostname = "bartolo.org"
port = 7722

username = sys.argv[1]
password = sys.argv[2]

def connect():
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

if __name__ == "__main__":
    check_output('cd .. && git push', shell=True)

    intentos = 0
    while (intentos < 5):
        try:
            print("\n%s\nIntentos: %s\n\n" % ( 20 * "*", intentos))
            connect()
            break
        except EOFError as error:
            print("Error de conexion")
            intentos += 1