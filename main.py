from lexer import Lexer
from parser import Parser
from CodeGenerator import CodeGenerator

import subprocess
import tempfile
import os
import argparse

#TODO:
#compiler flags:
# generate intermediary files

#comments.

def generate_asm(code):
    tokens = Lexer(code).lex()
    ast = Parser(tokens=tokens).parse()
    cg = CodeGenerator()
    for node in ast:
        cg.generate(node)
    return cg.get_output()


def compile_asm(asm, debug):
    with tempfile.NamedTemporaryFile(suffix=".asm", delete=False) as asm_file:
        asm_file.write(asm.encode())
        asm_file_name = asm_file.name
    try:
        command = ["nasm", "-f", "elf32", "-o", "output.o", asm_file_name]
        if debug:
            command.insert(3, "-g")
        subprocess.run(command, check=True)
        subprocess.run(["ld", "-m", "elf_i386", "-o", "output", "output.o"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")
    finally:
        os.remove(asm_file_name)
        if os.path.exists("output.o"):
            os.remove("output.o")

def main():
    parser = argparse.ArgumentParser(description="TofuScript Compiler")
    parser.add_argument('source_file', type=str, help="The source file to compile")
    parser.add_argument('-d', '--debug', action="store_true")

    args = parser.parse_args()

    try:
        with open(args.source_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: Source file '{args.source_file}' not found")
        return
    
    output = generate_asm(source_code)
    with open('output.asm', 'w') as f:
        f.write(output)
    compile_asm(output, args.debug)

if __name__ == "__main__":
    main()