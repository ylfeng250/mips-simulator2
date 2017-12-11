"""
辅助工具类
-数据读取 read_bin
-解析指令 parse_instructions
-find_break 返回代码段的结尾即数据段的起点
-checkFlag 检测输入什么类型的指令
-outputDis 输出dis文件
-outputSim 输出Sim文件
"""
import instructions
import changeRegValues
from instructions import opc


# 输入二进制文件，返回指令列表
def read_bin(filename):
    instructions = []
    with open(filename, "r") as fin:
        for line in fin:
            instructions.append(line.strip())
    return instructions


# 解析指令
# 2     4       5       5       5       5           5
# flag   opCodes rs      rt      rd      shiftAmt    functionCode
def parse_instructions(instruction, flags, opCodes, rs, rt, rd, shiftAmt,
                       functionCode):
    flags.append(instruction[0:2])  # 前两位用来区分是Category-1指令还是Category-2指令
    opCodes.append(instruction[2:6])  # 四位操作码
    rs.append(instruction[6:11])
    rt.append(instruction[11:16])
    rd.append(instruction[16:21])
    shiftAmt.append(instruction[21:26])
    functionCode.append(instruction[26:])


# break之后是数据部分---暂时没有用了

def find_break(instructions):
    count = 0
    for instruction in instructions:
        if instruction[0:7] != "010101":
            count += 1
        else:
            count += 1
            break
    return count  # 数据段的开头


# 检查属于第几类指令 0-Category-1    1-Category-2
def checkFlag(flag):
    k = 0
    if flag == '01':
        k = 0
    else:
        k = 1
    return int(k)


# 生成disassembly.txt  i是当前的指令地址
def outputDis(instruction, currentAddress, flag, opCode, rs, rt, rd, shiftAmt,
              functionCode, i, disOut):
    instructionName = opc[opCode][flag]  # 获取指令名称
    instructionArgs = instructions.switch[instructionName](
        rs, rt, rd, shiftAmt, functionCode)  # 获取指令参数
    if instructionName != 'BREAK':
        disOut.write(instruction + '\t' + str(
            currentAddress[0]) + '\t' + instructionName + ' ' + str(instructionArgs) + '\n')
    else:  # break指令没有操作数
        disOut.write(instruction + '\t' +
                     str(currentAddress[0]) + '\t' + instructionName + '\n')
    # Check if instruction is a break instruction
    if instructionName == 'BREAK':
        return True

# 执行命令 生成sim文件


def outputSim(dataAddress, currentAddress, flag, opCode, rs, rt, rd, shiftAmt,
              functionCode, regValues, memoryValues, count, simOut):
    instructionName = opc[opCode][flag]  # 获取指令名称
    instructionArgs = instructions.switch[instructionName](
        rs, rt, rd, shiftAmt, functionCode)  # 获取指令参数
    returnFlag = False  # 是否结束标志

    if instructionName == 'BREAK':
        returnFlag = True
    simOut.write("--------------------" + '\n')
    if instructionName != 'BREAK':
        simOut.write("Cycle:" + str(count[0] + 1) + '\t' + str(
            currentAddress[0]) + '\t' + instructionName + ' ' + instructionArgs + '\n')
    else:
        simOut.write("Cycle:" + str(count[0] + 1) + '\t' +
                     str(currentAddress[0]) + '\t' + instructionName + '\n')
    simOut.write('\n')

    changeRegValues.switch[instructionName](
        rs, rt, rd, shiftAmt, functionCode, regValues, memoryValues, dataAddress, currentAddress)

    simOut.write('Registers' + '\n')
    simOut.write('R00:' + '\t' + str(regValues[0]) + '\t' + str(regValues[1]) + '\t' + str(regValues[2])
                 + '\t' +
                 str(regValues[3]) + '\t' + str(regValues[4]) +
                 '\t' + str(regValues[5]) + '\t'
                 + str(regValues[6]) + '\t' + str(regValues[7]) + '\n')
    simOut.write('R08:' + '\t' + str(regValues[8]) + '\t' + str(regValues[9]) + '\t' +
                 str(regValues[10]) + '\t' + str(regValues[11]) + '\t' + str(regValues[12]) + '\t' +
                 str(regValues[13]) + '\t' + str(regValues[14]) + '\t' + str(regValues[15]) + '\n')
    simOut.write('R16:' + '\t' + str(regValues[16]) + '\t' + str(regValues[17]) + '\t' +
                 str(regValues[18]) + '\t' + str(regValues[19]) + '\t' + str(regValues[20]) + '\t' +
                 str(regValues[21]) + '\t' + str(regValues[22]) + '\t' + str(regValues[23]) + '\n')
    simOut.write('R24:' + '\t' + str(regValues[24]) + '\t' + str(regValues[25]) + '\t' +
                 str(regValues[26]) + '\t' + str(regValues[27]) + '\t' + str(regValues[28]) + '\t' +
                 str(regValues[29]) + '\t' + str(regValues[30]) + '\t' + str(regValues[31]) + '\n')
    simOut.write('\n')
    simOut.write('Data' + '\n')
    simOut.write(str(dataAddress) + ':\t' + str(memoryValues[0]) + '\t' + str(memoryValues[1]) + '\t' + str(memoryValues[2]) + '\t' +
                 str(memoryValues[3]) + '\t' + str(memoryValues[4]) + '\t' + str(memoryValues[5]) + '\t' +
                 str(memoryValues[6]) + '\t' + str(memoryValues[7]) + '\n')
    simOut.write(str(dataAddress + 32) + ':\t' + str(memoryValues[8]) + '\t' + str(memoryValues[9]) + '\t' + str(memoryValues[10]) + '\t' +
                 str(memoryValues[11]) + '\t' + str(memoryValues[12]) + '\t' + str(memoryValues[13]) + '\t' +
                 str(memoryValues[14]) + '\t' + str(memoryValues[15]) + '\n')
    simOut.write(str(dataAddress + 64) + ':\t' + str(memoryValues[16]) + '\t' + str(memoryValues[17]) + '\t' + str(memoryValues[18]) + '\t' +
                 str(memoryValues[19]) + '\t' + str(memoryValues[20]) + '\t' + str(memoryValues[21]) + '\t' +
                 str(memoryValues[22]) + '\t' + str(memoryValues[23]) + '\n')
    simOut.write('\n')

    count[0] = count[0] + 1

    return returnFlag


class scoreboarding:

    def __init__(self,currentAddress,dataAddress,flags, opCodes, rs, rt, rd, shiftAmts, functionCodes, simOut):
        self.currentAddress = currentAddress
        self.dataAddress = dataAddress
        # 指令部分
        self.flags = flags
        self.opCodes = opCodes
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shiftAmts = shiftAmts
        self.functionCodes = functionCodes
        # 输出的文件地址
        self.simOut = simOut
        # 时钟周期
        self.cycle = 1
        # 寄存器
        self.regValues = [0] * 32
        # 内存值
        self.memoryValues = [0] * 60

        # 是否存在structural hazards 或者 WAW
        self.is_stall = False
        self.is_break = False
        self.pre_issue = [] # 存指令在指令队列中的编号
        self.pre_alu1 = []
        self.pre_alu2 = []
        self.pre_mem = []
        self.post_alu2 = []
        self.post_mem = []
        self.reg_ready = [True] * 32
        # per_issue队列中的4条命令比较 第0条总是最新
        self.reg_w = [4] * 32 #谁要写这个寄存器
        self.reg_r = [4] * 32 #谁要读这个寄存器
        self.executed_instruction = []
        self.waiting_instruction = []
    """
    执行分支语句，在执行之前需要判断需要比较的寄存器是否就位
    """
    def brach(self,instructionName,rs, rt, rd, shiftAmt, functionCode):
        is_ready = True
        self.is_stall = False
        if instructionName == "J":
            immediate = rs + rt + rd + shiftAmt + functionCode + "00"
            currentAddress[0] = (int(immediate, 2))
        if instructionName == 'JR':
            currentAddress[0] = (int(rs+"00", 2))
        if instructionName == 'BEQ':
            # 获取需要比较的两个寄存器的下标
            rs_index = int(rs, 2)
            rt_index = int(rt, 2)
            # 可能依赖于前面的指令，寄存器中的值是否就位
            if not self.reg_ready[rs_index] or not self.reg_ready[rt_index]:# 没有就位
                self.is_stall = True # 暂停
                is_ready = False
            # 寄存器已经就位
            elif self.regValues[rs_index] == self.regValues[rt_index]:
                offset = rd + shiftAmt + functionCode + "00"
                self.currentAddress[0] = self.currentAddress[0] + int(offset, 2) + 4
            else:
                self.currentAddress[0] = self.currentAddress[0] + 4
        if instructionName == 'BLTZ':
            rs_index = int(rs, 2)
            # 可能依赖于前面的指令，寄存器中的值是否就位
            if not self.reg_ready[rs_index] :# 没有就位
                self.is_stall = True # 暂停
                is_ready = False
            # 寄存器已经就位
            elif self.regValues[rs_index] <0 :
                offset = rd + shiftAmt + functionCode + "00"
                self.currentAddress[0] = self.currentAddress[0] + int(offset, 2) + 4
            else:
                self.currentAddress[0] = self.currentAddress[0] + 4
        if instructionName == 'BGTZ':
            rs_index = int(rs, 2)
            # 可能依赖于前面的指令，寄存器中的值是否就位
            if not self.reg_ready[rs_index] :# 没有就位
                self.is_stall = True # 暂停
                is_ready = False
            # 寄存器已经就位
            elif self.regValues[rs_index] > 0:
                offset = rd + shiftAmt + functionCode + "00"
                self.currentAddress[0] = self.currentAddress[0] + int(offset, 2) + 4
            else:
                self.currentAddress[0] = self.currentAddress[0] + 4
        return is_ready # 不ready的话就要进入等待，知道寄存器就位
    """
    我能issue吗？
    """
    def is_issue(self,instructionName,rs, rt, rd,index):
        is_ok = False
        currentStore = self.store
        if instructionName in ['ADD', 'SUB', 'MUL', 'AND', 'OR', 'XOR', 'NOR', 'SLT']:
            arg1 = int(rs,2)
            arg2 = int(rt,2)
            arg3 = int(rd,2)
            # 序号比现在准备issue的指令的序号大，说明这个寄存器可以操作
            # 在读之前判断是否有人还没写，在写之前看看是否有人没有写，然后更新一波
            if self.reg_w[arg2] >= index and self.reg_w[arg3] >= index and self.reg_r[arg1] >= index and self.reg_w[arg1] >= index:
                is_ok = True
                # 修改寄存器的状态
                if self.reg_w[arg1] > index:
                    self.reg_w[arg1] = index
                if self.reg_r[arg2] > index:
                    self.reg_r[arg2] = index
                if self.reg_r[arg3] > index:
                    self.reg_r[arg3] = index
        elif instructionName in ['SLL', 'SRL', 'SRA']:  
            rd_i = int(rd,2)
            rt_i = int(rt,2)
            if self.reg_w[rt_i] >= index and self.reg_w[rd_i] >=index and self.reg_r[rd_i] >=index:
                is_ok = True
                if self.reg_w[rd_i] >= index:
                    self.reg_w[rd_i] = index
                if self.reg_r[rt_i] >= index:
                    self.reg_r[rt_i] = index
        elif instructionName in ("ADDI", "ANDI", "ORI", "XORI"):
            rs_i = int(rs,2)
            rt_i = int(rt,2)
            if self.reg_w[rt_i] >= index and self.reg_r[rs_i] >= index and self.reg_w[rs_i] >= index:
                is_ok = True
            if self.reg_w[rs_i] > index:
                self.reg_w[rs_i] = index
            if self.reg_r[rt_i] > index:
                self.reg_r[rt_i] = index
        elif instructionName == "SW":
            rt_i = int(rt,2)
            base = int(rs,2)
            if self.reg_w[rt] >= index and self.reg_w[base] >= index and self.store:
                is_ok = True
            else:
                currentStore = False
            if self.reg_r[rt_i] > index:
                self.reg_r[rt_i] = index
            if self.reg_r[base] > index:
                self.reg_r[base] = index
        elif instructionName == "LW":
            rt_i = int(rt,2)
            base = int(rs,2)
            if self.reg_w[base] >= index and self.reg_r[rt_i] >= index and self.reg_w[rt_i] >= index and self.store:
                is_ok = True
            if self.reg_w[rt_i] > index:
                self.reg_w[rt_i] = index
            if self.reg_r[base] > index:
                self.reg_r[base] = index
        
        return is_ok, currentStore
        
    def if_unit(self):
        # 取值阶段取到的指令，最多为2条，设置一个队列
        fetched_instructions = []  
        self.executed_instruction = []

        if self.is_stall: # 继续看是否能够跳转
            j = self.waiting_instruction[0]
            if self.brach(instructionName,self.rs[j], self.rt[j], self.rd[j], self.shiftAmt[j], self.functionCodes[j]):
                self.executed_instruction[0] = self.waiting_instruction[0]
                self.waiting_instruction = []
        else:
            fetched_num = 2 # 一次最多取两条指令
            while not self.is_break and fetched_num > 0 and len(self.pre_issue) < 4:
                
                i = int((self.currentAddress[0] / 4) - 64) # 获取指令所在地址对应的下标
                print("第几条指令i:",i)
                print("指令地址current:",self.currentAddress)
                flag = checkFlag(self.flags[i])
                instructionName = opc[self.opCodes[i]][flag]  # 获取指令名称
                instructionArgs = instructions.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i])
                if instructionName == "BREAK": 
                    self.is_break = True # 结束
                    self.executed_instruction.append(i)
                elif instructionName in ['J','JR','BEQ','BLTZ','BGTZ']: # 如果是分支指令
                    # 检查是否需要改变下一个指令的地址
                    if self.brach(instructionName,self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i]):
                        self.executed_instruction.append(i)
                    else:
                        self.waiting_instruction.append(i)
                else:
                    fetched_instructions.append(i) # 只需要记录第几条指令，到时候再解析，方法比较笨但是可以快速理解
                    fetched_num -= 1 # 能够取得指令数量减1
                    if instructionName == 'SW':
                        self.reg_ready[int(self.rt[i],2)] = False
        return fetched_instructions

    """
    一次最多issue一条LW/SW到pre_alu1,一条非LW/SW指令到pre_aul2
    """
    def issue(self):
        alu1 = []
        alu2 = []
        issued_alu1 = 0 # 发射到alu1中的指令条数
        issued_alu2 = 0 # 发射到alu2z中的指令条数
        self.store = True
        i = 0
        while i < len(self.pre_issue):
            # if len(self.pre_alu1) + len(self.pre_alu2) + issued_num == 2:# issue上限
            if issued_alu1 == 1 and issued_alu2 == 1:# alu1 和 alu2都发射了一条指令就停止
                break
            index = self.pre_issue[i] # 获取指令在instructions中的index
            flag = checkFlag(self.flags[index])
            instructionName = opc[self.opCodes[index]][flag] 
            can_issue, currentStore = self.is_issue(instructionName,self.rs[index], self.rt[index], self.rd[index],index)
            self.store = currentStore and self.store
            if can_issue:
                if instructionName in ['LW','SW']:
                    issued_alu1 += 1
                    alu1.append(index) # 将指令放入alu1
                else:
                    issued_alu2 += 1
                    alu2.append(index)
            i += 1
        for j in alu1:
            self.pre_issue.remove(j)
        for j in alu2:
            self.pre_issue.remove(j)
        return alu1,alu2
    
    def alu1(self):
        pre_mem = []
        if len(self.pre_alu1) > 0:
            i = self.pre_alu1.pop(0)
            pre_mem.append(i)
        return pre_mem

    def alu2(self):
        post_alu2 = []
        if len(self.pre_alu2) > 0 :
            i = self.pre_alu2.pop(0)
            post_alu2.append(i)
        return post_alu2
    
    def mem(self):
        post_mem = []
        if len(self.pre_mem) == 1:
            i = self.pre_mem.pop(0)
            flag = checkFlag(self.flags[i])
            instructionName = opc[self.opCodes[i]][flag]
            if instructionName == 'SW':
                changeRegValues.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i], self.regValues, self.memoryValues, self.dataAddress, self.currentAddress)
            else:
                post_mem.append(i)
        return post_mem
    def wb(self):
        if len(self.post_mem) == 1:
            i = post_mem.pop(0)
            flag = checkFlag(self.flags[i])
            instructionName = opc[self.opCodes[i]][flag]
            changeRegValues.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i], self.regValues, self.memoryValues, self.dataAddress, self.currentAddress)
            rt_i = int(self.rt[i],2)
            self.reg_ready[i] = True
            self.reg_w[i] = 4
        if len(self.post_alu2) == 1:
            i = self.post_alu2.pop(0)
            flag = checkFlag(self.flags[i])
            instructionName = opc[self.opCodes[i]][flag]
            changeRegValues.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i], self.regValues, self.memoryValues, self.dataAddress, self.currentAddress)
            rd_i = int(self.rd[i],2)
            self.reg_ready[i] = True
            self.reg_w[i] = 4
    def output(self,cycle):
        string = "--------------------\n"
        string += "Cycle:" + str(cycle) + "\n" 
        string += "IF Unit:\n"
        string += "\tWaiting Instruction:"
        if len(self.waiting_instruction) > 0:
            i = self.waiting_instruction[0]
            flag = checkFlag(self.flags[i])
            instructionName = opc[self.opCodes[i]][flag]  # 获取指令名称
            instructionArgs = instructions.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i])
            string += " [" + instructionName + " " + instructionArgs + "]"
        else:
            string += "\n"
        string += "\tExecuted Instruction:"
        if len(self.executed_instruction) > 0:
            i = self.executed_instruction[0]
            flag = checkFlag(self.flags[i])
            instructionName = opc[self.opCodes[i]][flag]  # 获取指令名称
            instructionArgs = instructions.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i])
            string += " [" + instructionName + " " + instructionArgs + "]"
        else:
            string += "\n"


        return string
    def do(self):
        simulation = ""
        while True:
            fetched_instructions = self.if_unit()
            alu1,alu2 = self.issue()
            pre_mem = self.alu1()
            post_alu2 = self.alu2()
            post_mem = self.mem()
            self.wb()
            self.pre_issue.extend(fetched_instructions)
            self.pre_alu1.extend(alu1)
            self.pre_alu2.extend(alu2)
            self.pre_mem.extend(pre_mem)
            self.post_alu2.extend(post_alu2)
            self.post_mem.extend(post_mem)
            simulation += self.output(self.cycle)
            print("循环次数",self.cycle)
            self.cycle += 1
            print("执行指令",self.executed_instruction)
            print("寄存器状态",self.reg_ready)
            print("isbreak:",self.is_break)
            if self.is_break:
                break
        print(simulation)





def test():
    filename = input("请输入二进制文件:\n")
    instructions = read_bin(filename)
    print(instructions[0][:2])


if __name__ == "__main__":
    test()
