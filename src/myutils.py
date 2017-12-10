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

# 根据flag判断是第一类操作还是第二类操作，然后映射操作符
opc = {
    "0000": ['J', 'ADD'],
    "0001": ['JR', 'SUB'],
    "0010": ['BEQ', 'MUL'],
    "0011": ['BLTZ', 'AND'],
    "0100": ['BGTZ', 'OR'],
    "0101": ['BREAK', 'XOR'],
    "0110": ['SW', 'NOR'],
    '0111': ['LW', 'SLT'],
    '1000': ['SLL', 'ADDI'],
    '1001': ['SRL', 'ANDI'],
    '1010': ['SRA', 'ORI'],
    '1011': ['NOP', 'XORI']
}


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
        self.pre_issue = []
        self.reg_ready = [True] * 32
    """
    执行分支语句，在执行之前需要判断需要比较的寄存器是否就位
    """
    def brach(self,instructionName,rs, rt, rd, shiftAmt, functionCode):
        is_ready = Ture
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
                if self.regValues[int(rs, 2)] == self.regValues[int(rt, 2)]:
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
            elif self.regValues[rs_index] == self.regValues[rt_index]:
                offset = rd + shiftAmt + functionCode + "00"
                if self.regValues[rs_index] < 0:
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
            elif self.regValues[rs_index] == self.regValues[rt_index]:
                offset = rd + shiftAmt + functionCode + "00"
                if self.regValues[rs_index] > 0:
                    self.currentAddress[0] = self.currentAddress[0] + int(offset, 2) + 4
                else:
                    self.currentAddress[0] = self.currentAddress[0] + 4
        return is_ready # 不ready的话就要进入等待，知道寄存器就位

    def if_unit(self):
        # 取值阶段取到的指令，最多为2条，设置一个队列
        fetched_instructions = []  
        self.executed_instruction = ""

        if self.is_stall:
            pass
        else:
            fetched_num = 2 # 一次最多取两条指令
            while not self.is_break and fetched_num > 0 and len(self.pre_issue) < 4:
                i = int((self.currentAddress[0] / 4) - 64) # 获取指令所在地址对应的下标
                instructionName = opc[self.opCodes[i]][self.flags[i]]  # 获取指令名称
                instructionArgs = instructions.switch[instructionName](self.rs[i], self.rt[i], self.rd[i], self.shiftAmts[i], self.functionCodes[i])
                if instructionName == "BREAK":
                    self.is_break = True # 结束
                    self.executed_instruction = '[' + instructionName + ' ' + instructionArgs + ']'
                elif instructionName in ['J','JR','BEQ','BLTZ','BGTZ']: # 如果是分支指令
                    # 需要改变下一个指令的地址
                    if self.brach(instructionName,self.rs[i], self.rt[i], self.rd[i], self.shiftAmt[i], self.functionCodes[i]):
                        self.executed_instruction = '[' + instructionName + ' ' + instructionArgs + ']'
                    else:
                        self.waiting_instruction = '[' + instructionName + ' ' + instructionArgs + ']'
                else:
                    fetched_instructions.append(i) # 只需要记录第几条指令，到时候再解析，方法比较笨但是可以快速理解
                    






def test():
    filename = input("请输入二进制文件:\n")
    instructions = read_bin(filename)
    print(instructions[0][:2])


if __name__ == "__main__":
    test()
