import sys

def ip_to_str(ipv4:str) -> str:
    ip_str:str = ""
    for i in (lst:=ipv4.split('.')):
        i_int:int = int(i)
        if i_int<0 or i_int>255 or len(lst)!=4:
            raise ValueError("IP Address Not Valid")
        ip_str = r'\x'+ "%02x"%i_int + ip_str #Little Endian
    return ip_str

def port_to_str(port:str) -> str:
    try:
        int(port)
    except ValueError:
        print("Port number must be a 2 byte integer")
        exit()
    if int(port)<0 or int(port)>65535:
        raise ValueError("Port number is not valid")
    port_hex:str = "%04x"%int(port)
    port_hex:str = r"\x"+port_hex[-2:]+r"\x"+port_hex[0:2]
    return port_hex

def set_host_conn(shellcode:str) -> str:
    shellcode = shellcode.replace("IP", ip_to_str(sys.argv[2]))
    shellcode = shellcode.replace("PORT", port_to_str(sys.argv[3]))
    return shellcode

def main() -> None:
    try:
        file_test = open(sys.argv[1], 'r')
        file_test.close()
    except FileNotFoundError:
        print("Invalid file")
        exit()
    shellcode:str = ""
    with open(sys.argv[1], 'r') as shell_file:
        shellcode = shell_file.read()
    if 'IP' not in shellcode or 'PORT' not in shellcode:
        raise ValueError("There is no IP or port to change. Add an IP address by putting 'IP' and 'PORT' where they need to be set in your shellcode")
    shellcode = shellcode.replace('"','')
    shellcode = shellcode.replace('\n','')
    shellcode = shellcode.replace(' ','')
    shellcode = set_host_conn(shellcode)
    with open(sys.argv[1], 'w') as shell_file:
        shell_file.write(shellcode)

if __name__=="__main__":
    main()
