#x86 asm notes
# eax - 32 bit general register
# DWORD - double word, 32 bits
# mov DWORD [ident], eax - moves a 32 bit value from eax to the identifier i think #TODO check this

from ast_nodes import *
class CodeGenerator:
    def __init__(self):
        self.output = []
        self.data_section = []
        self.labels = 0
        self.declared_vars = set()
        self.print_used = False

    def generate(self, node):
        if isinstance(node, AssignmentNode):
            self.generate_assignment(node)
        elif isinstance(node, BinaryOpNode):
            return self.generate_binary_op(node)
        elif isinstance(node, NumberNode):
            return self.generate_number(node)
        elif isinstance(node, IdentifierNode):
            return self.generate_identifier(node)
        elif isinstance(node, IfNode):
            self.generate_if(node)
        elif isinstance(node, PrintNode):  
            self.generate_print_int(node)
        else:
            raise TypeError(f"Unknown AST node type: {type(node)}")
        
    def generate_assignment(self, node):

        if node.identifier not in self.declared_vars:
            self.data_section.append(f"{node.identifier} dd 0") #< 32 bit var for the assignment goes in data section
            self.declared_vars.add(node.identifier)

        value = self.generate(node.value)
        self.output.append(f"mov eax, {value}")
        self.output.append(f"mov DWORD [{node.identifier}], eax")
    
    def generate_binary_op(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)

        self.output.append(F"mov eax, {left}")
        self.output.append(f"mov ebx, {right}")

        #in x86, teh jump instructions use a flag that is the result of the cmp instruction
        if node.operator in ['>', '<', '>=', '<=', '==', '!=']:
            self.output.append(f"cmp eax, ebx")  

        if node.operator == '>':
            return "jle"  # Jump if less or equal 
        elif node.operator == '<':
            return "jge"  # Jump if greater or equal 
        elif node.operator == '>=':
            return "jl"   # Jump if less 
        elif node.operator == '<=':
            return "jg"   # Jump if greater 
        elif node.operator == '==':
            return "jne"  # Jump if not equal 
        elif node.operator == '!=':
            return "je"   # Jump if equal 

        
        if node.operator == '+':
            self.output.append("add eax, ebx")
        elif node.operator == '-':
            self.output.append("sub eax, ebx")
        elif node.operator == '*':
            self.output.append("imul eax, ebx")
        elif node.operator == '/':
            self.output.append("cdq")
            self.output.append("idiv ebx")
        
        return "eax"

    def generate_number(self, node):
        return str(node.value)
    
    def generate_identifier(self, node):
        return f"[{node.name}]"

    def generate_if(self, node):
        condition = self.generate(node.condition)
        end_label = self.get_unique_label("end_if")
        self.output.append(f"{condition} {end_label}")

        for statement in node.body:
            self.generate(statement)

        self.output.append(f"{end_label}:")

    
    def get_unique_label(self, prefix):
        self.labels += 1
        return f"{prefix}_{self.labels}"

    def generate_exit_code(self):
        exit_code = [
            "mov eax, 1",     
            "mov ebx, 0",     
            "int 0x80"        
        ]
        return "\n".join(exit_code) 

    def generate_print_int(self, node):
        self.print_used = True
        value = self.generate(node.value)
    
        self.output.append(f"mov eax, {value}")
        self.output.append("call print_int")


    def generate_print_int_code(self):
        print_code = [
            "print_int:",
            "mov eax, 4            ; syscall number for write (sys_write)",
            "mov ebx, 1            ; file descriptor (stdout)",
            "lea ecx, [esp-4]      ; Load the address of the 4-byte value to print",
            "mov [esp-4], ecx      ; Store the 4-byte value in the stack temporarily",
            "mov edx, 4            ; Print 4 bytes (32 bits)",
            "int 0x80              ; Make the syscall",
            "ret"
        ]
        return "\n".join(print_code)

    def get_output(self):
        data_section_str = "section .data\n" + "\n".join(self.data_section) if self.data_section else ""
        text_section_str = "section .text\nglobal _start\n\n_start:\n" + "\n".join(self.output)

        if self.print_used:
            text_section_str += "\n\n" + self.generate_print_int_code()
        text_section_str += "\n\n" + self.generate_exit_code()
        return f"{data_section_str}\n\n{text_section_str}"


