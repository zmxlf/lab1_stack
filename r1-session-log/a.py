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
        return len(self.data) == 0

def main():
    sessions = 0
    stack=Stack()
    stroka = 0

    stroki_stacks={}
    active={}
    per_user = "--per-user" in sys.argv

    if len(sys.argv) < 3:
            print("Ошибка: Укажите входной или выходной файлы")
            return
    input_file = sys.argv[1]    
    output_file = sys.argv[2]
    # input_file = "input.txt"     
    # output_file = "output.txt" 
    with  open(input_file, 'r', encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        lines = infile.readlines()
        
        check_begin=0    
        stroka_begin=0
        
        bufer_stack=Stack()
        
        for line in lines:
            norm_stroka=0
            stroka+=1
            line = " ".join(line.split())
            if line:
                    
                    if line.find("BEGIN")==0 and line.find("N")==4:
                        norm_stroka+=1 
                        if check_begin>=1 and norm_stroka==1:
                            outfile.write(f"ERROR {stroka} nested_begin\n")
                        else:    
                            bufer_stack.data+=stack.data
                            stroka_begin=stroka
                            check_begin+=1
                        
                       

                        

                    if (line.find("LOGIN")==0 and line.find(" ")==5) or (line.find("LOGOUT")==0 and line.find(" ")==6):
                        probel = line.find(" ")
                        commond = line[0:probel]
                        znach = line[probel+1:]
                        norm_stroka+=1
                        if commond=="LOGIN":
                            if per_user:
                                active[znach] = active.get(znach, 0) + 1
                            else:
                                stack.push(znach)
                            stroki_stacks[znach] = stroka
                        if commond=="LOGOUT":
                            if per_user:
                                if active.get(znach, 0) == 0:
                                    outfile.write(f"ERROR {stroka} logout_without_login\n")
                                else:
                                    active[znach] -= 1
                                    sessions += 1
                            else:
                                if stack.is_empty():
                                    outfile.write(f"ERROR {stroka} logout_without_login\n")
                                else:
                                    if stack.top()!=znach:
                                        outfile.write(f"ERROR {stroka} order_violation\n")
                                    else:
                                        stack.pop()
                                        sessions+=1
                    
                    
                    
                    if line.find("ROLLBACK")==0 and line.find("K")==7:
                        norm_stroka+=1
                        if check_begin ==0:
                            outfile.write(f"ERROR {stroka} no_transaction\n")
                        else:
                                
                            check_begin=0
                            stack.data=bufer_stack.data
                            bufer_stack=Stack()
                            
                                    
                                            
                                        
                    if line.find("COMMIT")==0 and line.find("T")==5:
                        norm_stroka+=1
                        if check_begin ==0:
                            outfile.write(f"ERROR {stroka} no_transaction\n")
                        else:    
                            check_begin=0
                            bufer_stack=Stack()    
                    
                    
                    
                    
                    
                    if norm_stroka==0:
                        norm_stroka=0
                        outfile.write(f"ERROR {stroka} bad_event\n")                
                     
                    
        if check_begin==1:
            outfile.write(f"ERROR {stroka_begin} transaction_not_closed\n")
                        
        
        if per_user:
            for name, cnt in active.items():
                for _ in range(cnt):
                    if name in stroki_stacks:
                        outfile.write(f"ERROR {stroki_stacks[name]} session_not_closed\n")
        else:
            if stack.is_empty()==0:
                for i in stack.data:
                    if i in stroki_stacks:
                        outfile.write(f"ERROR {stroki_stacks[i]} session_not_closed\n")
        outfile.write(f"SESSIONS {sessions} \n")

if __name__ == '__main__':
    main()