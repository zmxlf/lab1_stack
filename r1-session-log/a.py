import sys

class Stack:

    def __init__(self):
        self.data = []


    def push(self,znach):
        self.data+=[znach]
        
    def pop(self):
        a = self.data[-1]
        del self.data[-1]
        return a

    def top(self):
        return self.data[-1]

    def is_empty(self):
        count = 0
        for i in self.data:
            count+=1
        return count==0

def main():
    sessions = 0
    stack=Stack()
    stroka = 1
    input_file=""
    output_file=""
    if len(sys.argv) < 3:
            print("Ошибка: Укажите входной или выходной файлы")
            return
    input_file = sys.argv[1]    
    output_file = sys.argv[2]
    # input_file = "input.txt"
    # output_file = "output.txt"
    with  open(input_file, 'r', encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        lines = infile.readlines()
        
            

        for line in lines:
            
            if line.strip():

                if (line.find("LOGIN")==0 and line.find(" ")==5) or (line.find("LOGOUT")==0 and line.find(" ")==6):
                    probel = line.find(" ")
                    commond = line[0:probel]
                    znach = line[probel+1:]
                    if commond=="LOGIN":
                        stack.push(znach)
                    if commond=="LOGOUT":
                                        
                        if stack.is_empty():
                            outfile.write(f"ERROR {stroka} logout_without_login\n")
                        else:
                            if stack.top()!=znach:
                                outfile.write(f"ERROR {stroka} order_violation\n")
                            else:
                                stack.pop()
                                sessions+=1
                    
                

                else:
                    outfile.write(f"ERROR {stroka} bad_event\n")
                print(line)
            stroka+=1
        if stack.is_empty()==0:
            for i in range(len(stack.data)):
                outfile.write(f"ERROR {i+1} session_not_closed\n")
        outfile.write(f"SESSIONS {sessions} \n")

if __name__ == '__main__':
    main()