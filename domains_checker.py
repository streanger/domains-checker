import sys
import os
import codecs
import subprocess
from termcolor import colored
from pathlib import Path
from sys import platform


def script_path():
    '''set current path, to script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def read_file(filename, mode='r'):
    '''read from file'''
    content = ''
    try:
        with codecs.open(filename, mode, encoding='utf-8') as f:
            content = f.read()
            
    except Exception as err:
        print('failed to read from file: {}, err: {}'.format(filename, err))
        
    return content
    
    
def write_file(filename, text, mode='w'):
    '''write to file'''
    try:
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(text)
            
    except Exception as err:
        print('failed to write to file: {}, err: {}'.format(filename, err))
        
    return None
    
    
def check_domain_exist(domains):
    '''check if domains exists'''
    existing_domains = []
    total_domains = len(domains)
    for index, domain in enumerate(domains):
        command = 'nslookup {}'.format(domain)
        response = subprocess.getoutput(command)
        not_exist_pattern1 = "server can't find"
        not_exist_pattern2 = "Can't find"
        not_exists_status = (not_exist_pattern1 in response) or (not_exist_pattern2 in response)
        if not_exists_status:
            info = colored('    [x] does not exist', 'yellow')
        else:
            response_lines = response.splitlines()
            name_pattern = 'Name:'
            for lines_index, line in enumerate(response_lines):
                if name_pattern in line:
                    address_index = lines_index+1
                    break
            domain_address = response_lines[address_index].split()[1].strip()
            info = colored('    [+] exists, ip address: {}'.format(domain_address), 'green')
            existing_domains.append(domain)
        print('{}/{}) {}\n{}\n'.format(index+1, total_domains, domain, info))
        # ~ print(response)
    return existing_domains
    
    
if __name__ == "__main__":
    script_path()
    if platform == 'win32':
        os.system('color')
        
        
    # ******* read domains *******
    filename = 'domains.txt'
    domains = [line.strip() for line in read_file(filename).splitlines() if line.strip()]
    domains = sorted(list(set(domains)))


    # ******* iter domains *******
    existing_domains = check_domain_exist(domains)


    # ******* save output *******
    existing_domains_file = 'existing_domains.txt'
    write_file(existing_domains_file, '\n'.join(existing_domains))
    print('[*] data saved to: {}'.format(existing_domains_file))
