from sys import argv
class BrainfuckTranslator:
    def __init__(self,init_code:str, tear_down_code:str) -> None:
        self.indentation:int=0
        self.inc:int=0
        self.dec:int=0
        self.right:int=0
        self.left:int=0
        self.code:int=""
        self.init_code:str=init_code
        self.tear_down_code:str=tear_down_code
    def __enter__(self):
        self.code=self.code+self.init_code
        return self
    def __exit__(self, exc_type, exc_value, tb):
        self.code=self.code+self.tear_down_code.replace('_',self.get_indent())
        return self
    def translate(self,code:str)->str:
        self.indentation=0
        python_code="""\
array=[0]*30000
pointer=0\n"""
        for character in code:
            if character=='[':
                python_code=python_code+f"{'    '*self.indentation}\
while array[pointer]:\n"
                self.indentation+=1
            elif character==']':
                self.indentation-=1
            elif character=='+':
                python_code=\
                    python_code+f"{'    '*self.indentation}array[pointer]+=1\n"
            elif character=='-':
                python_code=\
                    python_code+f"{'    '*self.indentation}array[pointer]-=1\n"
            elif character=='>':
                python_code=\
                    python_code+f"{'    '*self.indentation}pointer+=1\n"
            elif character=='<':
                python_code=\
                    python_code+f"{'    '*self.indentation}pointer-=1\n"
            elif character=='.':
                python_code=\
                    python_code+f"{'    '*self.indentation}print(chr(array[pointer]),end=\"\")\n"
            elif character==',':
                python_code=\
                    python_code+f"{'    '*self.indentation}array[pointer]=ord(input())\n"
            else:
                pass
        return python_code
    def translate_C(self,code:str)->str:
        self.indentation=1
        self.code="#include <stdio.h>\n\
#include <stdlib.h>\n\
int main(){\n\
  char* array = calloc(30000, sizeof(char));\n\
  int pointer=0;\n"
        for character in code:
            if character=='[':
                self.code=self.code+f"{'  '*self.indentation}"+"while(array[pointer]){\n"
                self.indentation+=1
            elif character==']':
                self.indentation-=1
                self.code=self.code+f"{'  '*self.indentation}"+"}\n"
            elif character==">":
                self.code=self.code+f"{'  '*self.indentation}"+"pointer++;\n"
            elif character=="<":
                self.code=self.code+f"{'  '*self.indentation}"+"pointer--;\n"
            elif character=="+":
                self.code=self.code+f"{'  '*self.indentation}"+"array[pointer]++;\n"
            elif character=="-":
                self.code=self.code+f"{'  '*self.indentation}"+"array[pointer]--;\n"
            elif character==".":
                self.code=self.code+f"{'  '*self.indentation}"+'putchar(array[pointer]);\n'
            elif character==",":
                self.code=self.code+f"{'  '*self.indentation}"+"array[pointer]=getchar();\n"
        self.code=self.code+f"{'  '*self.indentation}"+"free(array);\n}\n"
        return self.code
    def translate_c_opt(self,code:str)->None:
        self.indentation=1
        for character in code:
            if character=='[':
                self.eval_optimized_C()
                self.code=self.code+self.get_indent()+"while(array[pointer]){\n"
                self.indentation+=1
            elif character==']':
                self.eval_optimized_C()
                self.indentation-=1
                self.code=self.code+self.get_indent()+"}\n"
            elif character==">":
                self.eval_optimized_C(right_=False)
                self.right+=1
            elif character=="<":
                self.eval_optimized_C(left_=False)
                self.left+=1
            elif character=="+":
                self.eval_optimized_C(inc_=False)
                self.inc+=1
            elif character=="-":
                self.eval_optimized_C(dec_c=False)
                self.dec+=1
            elif character==".":
                self.eval_optimized_C()
                self.code=self.code+self.get_indent()+'putchar(array[pointer]);\n'
            elif character==",":
                self.eval_optimized_C()
                self.code=self.code+f"self.get_indent()"+"array[pointer]=getchar();\n"
    def eval_optimized_C(self,inc_:bool = True, dec_c:bool = True, left_:bool=True,right_:bool=True)->None:
        if self.inc and inc_:
            self.code=self.code+"_array[pointer]+=val;\n"\
                .replace("_",self.get_indent())\
                .replace("val",str(self.inc))
            self.inc=0
        elif self.dec and dec_c:
            self.code=self.code+"_array[pointer]-=val;\n"\
                .replace("_",self.get_indent())\
                .replace("val",str(self.dec))                    
            self.dec=0
        elif self.left and left_:
            self.code=self.code+"_pointer-=val;\n"\
                .replace('_',self.get_indent())\
                .replace('val',str(self.left))
            self.left=0
        elif self.right and right_:
            self.code=self.code+"_pointer+=val;\n"\
                .replace('_',self.get_indent())\
                .replace('val',str(self.right))
            self.right=0
    def get_indent(self)->str:
        return '    '*self.indentation
if __name__=="__main__":
    assert len(argv)==2
    with open(argv[1],'r') as f:
        file = f.read()
    with BrainfuckTranslator("#include <stdio.h>\n\
#include <stdlib.h>\n\
int main(){\n\
  char* array = calloc(30000, sizeof(char));\n\
  int pointer=0;\n","_free(array);\n}\n") as bf:
        bf.translate_c_opt(file)
    print(bf.code)
    with BrainfuckTranslator("#include <stdio>\n\
#include <vector>\n\
int main(){\n\
    std::vector<char> array(30000,0);\n\
    int pointer=0;\n","_}") as bf:
        bf.translate_c_opt(file)
    print(bf.code)