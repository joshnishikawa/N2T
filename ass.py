from sys import argv
from os.path import exists

script, in_file_name, out_file_name = argv
with open(in_file_name) as in_file_lines:
    raw = in_file_lines.readlines()

stripped = [] # list of lines stripped of comments and other artifacts
counter = 0 # to keep track of addresses for (JUMP HEADERS) when found
jump_list = [] # stores addresses and names of (JUMP HEADERS)

ALU = {'0': '0101010', '1': '0111111', '-1': '0111010',
        'D': '0001100', 'A': '0110000',
        '!D': '0001101', '!A': '0110001', '-D': '0001111', '-A': '0110011',
        'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110', 'A-1': '0110010',
        'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
        'D&A': '0000000', 'D|A': '0010101',
        'M': '1110000', '!M': '1110001', '-M': '1110011',
        'M+1': '1110111', 'M-1': '1110010',
        'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
        'D&M': '1000000', 'D|M': '1010101'}

D123 = {'NULL': '000',
        'M': '001',
        'D': '010',
        'A': '100',
        'MD': '011', 'DM': '011',
        'AM': '101', 'MA': '101',
        'AD': '110', 'DA': '110',
        'ADM': '111', 'AMD': '111', 'DAM': '111',
        'DMA': '111', 'MAD': '111', 'MDA': '111'}

J123 = {'NULL': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'}

def a_instruction(x):
    """assigns ROM address for jump-to inst, RAM address for others."""
    found = False
    for i in jump_list:
        if x[1:] == i[1]:
            result = "{0:016b}\n".format(i[0]) # binary with leading 0s
            found = True
            break # or next tup checked & no match, nullifying found match
        else: pass
    if found:
        return result
    else:
        result = "{0:016b}\n".format(int(x[1:])) # FIXME only numeric addresses are valid
        return result

def c_instruction(x):
    """assembles a c-instruction"""
    if '=' in x:
        parts = x.split('=')
        inst = ALU[parts[1]]
        dest = D123[parts[0]]
        jump = J123['NULL']
    else:
        parts = x.split(';')
        inst = ALU[parts[0]]
        dest = D123['NULL']
        jump = J123[parts[1]]
    result = '111' + inst + dest + jump + '\n'
    return result

for i in raw:
    if i[0] in [' ', '\t', '#', '\r', '\n']:
        continue                    # skips lines without code
    elif '#' in i:
        i = i[:i.index('#')].strip() # strips comments
    else: pass
    stripped.append(i.strip())       # strips empty space

for i in stripped: # writes the entire jump_list before assembly begins
    if i[0] == '(':
        jump_list.append((counter, i[1:-1]))
        counter -= 1 # (JUMP HEADERS) don't count as instrucitons
    else: pass
    counter += 1

with open(out_file_name, 'w') as out_file_object:
    for i in stripped:
        if i[0] == '(':
            continue
        elif i[0] == '@':
            out_file_object.write(a_instruction(i))
        else: out_file_object.write(c_instruction(i))

    if exists(out_file_name):
        print "%s already exists. Overwrite it?" % out_file_name
        print "Hit RETURN to continue or CTRL+C to cancel."
        raw_input("> ")
    else: pass
