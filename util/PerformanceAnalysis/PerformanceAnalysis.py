import os
import pickle

# 所有指令的信息，key: {pc, start_cycle. sid, wid}
all_sm_warp_insns = []

sm_warp_insns = {}

stall_type = {
  0:  "Issue: ibuffer_empty", 
  1:  "Issue: waiting for barrier",
  2:  "Issue: ibuffer_empty and also waiting for barrier",
  3:  "Issue: control hazard",
  4:  "Issue: m_mem_out has no free slot",
  5:  "Issue: previous_issued_inst_exec_type is MEM",
  6:  "Issue: m_int_out has no free slot",
  7:  "Issue: previous_issued_inst_exec_type is INT",
  8:  "Issue: m_sp_out has no free slot",
  9:  "Issue: previous_issued_inst_exec_type is SP",
  10: "Issue: m_dp_out has no free slot",
  11: "Issue: previous_issued_inst_exec_type is DP",
  12: "Issue: m_sfu_out has no free slot",
  13: "Issue: previous_issued_inst_exec_type is SFU",
  14: "Issue: m_tensor_core_out has no free slot",
  15: "Issue: previous_issued_inst_exec_type is TENSOR",
  16: "Issue: m_spec_cores_out has no free slot",
  17: "Issue: previous_issued_inst_exec_type is SPECIALIZED",
  18: "Issue: scoreboard",
  19: "Fetch: read miss an insn from L1I",
  20: "Fetch: reservation fail an insn from L1I",
  21: "Execute: m_memport of L1D is not free",
  22: "Execute: m_dispatch_reg of fu is not empty",
  23: "Execute: result_bus has no slot",
  24: "Execute: dispatch delay of insn is > 0",
  25: "Execute: l1_latency_queue is not free",
  26: "Execute: COAL_STALL occurs",
  27: "Execute: mf_next->get_inst()'s out_reg[Rx] has pending writes",
  28: "Execute: icnt_injection_buffer is full",
  29: "Execute: m_next_wb's out_reg[Rx] has pending writes",
  30: "Execute: m_next_global of ldst unit is not free",
  31: "Execute: fill_port of L1D is not free",
  32: "Execute: m_pipeline_reg is not empty",
  33: "Execute: m_dispatch_reg has pending writes",
  34: "Execute: bank of reg is not idle",
  35: "Readoperands: bank reg belonged to was allocated for write",
  36: "Readoperands: bank reg belonged to was allocated for other regs",
  37: "Readoperands: not found free cu",
  38: "Writeback: bank of reg is not idle",
}

stall_type_specific = {
  0:  "Issue: ibuffer_empty", 
  1:  "Issue: waiting for barrier",
  2:  "Issue: ibuffer_empty and also waiting for barrier",
  3:  "Issue: control hazard",
  4:  "Issue: m_mem_out has no free slot",
  5:  "Issue: previous_issued_inst_exec_type is MEM",
  6:  "Issue: m_int_out has no free slot",
  7:  "Issue: previous_issued_inst_exec_type is INT",
  8:  "Issue: m_sp_out has no free slot",
  9:  "Issue: previous_issued_inst_exec_type is SP",
  10: "Issue: m_dp_out has no free slot",
  11: "Issue: previous_issued_inst_exec_type is DP",
  12: "Issue: m_sfu_out has no free slot",
  13: "Issue: previous_issued_inst_exec_type is SFU",
  14: "Issue: m_tensor_core_out has no free slot",
  15: "Issue: previous_issued_inst_exec_type is TENSOR",
  16: "Issue: m_spec_cores_out has no free slot",
  17: "Issue: previous_issued_inst_exec_type is SPECIALIZED",
  18: "Issue: scoreboard",
  19: "Fetch: read miss an insn from L1I",
  20: "Fetch: reservation fail an insn from L1I",
  21: "Execute: m_memport of L1D is not free",
  22: "Execute: m_dispatch_reg of fu\[\d+\]-\w+\s is not empty",
  23: "Execute: result_bus has no slot for latency-\d+",
  24: "Execute: dispatch delay of insn is \d+ > 0",
  25: "Execute: l1_latency_queue\[\d+\]\[\d+\] is not free",
  26: "Execute: COAL_STALL occurs",
  27: "Execute: mf_next->get_inst()'s out_reg\[R\d+\] has \d+ pending writes",
  28: "Execute: icnt_injection_buffer is full",
  29: "Execute: m_next_wb's out_reg\[R\d+\] has \d+ pending writes",
  30: "Execute: m_next_global of ldst unit is not free",
  31: "Execute: fill_port of L1D is not free",
  32: "Execute: m_pipeline_reg\[\d+\] is not empty",
  33: "Execute: m_dispatch_reg has pending writes",
  34: "Execute: bank-\d+ of reg-\d+ is not idle",
  35: "ReadOperands: bank\[\d+\] reg-\d+ \(order:\d+\) belonged to was allocated for write",
  36: "ReadOperands: bank\[\d+\] reg-\d+ \(order:\d+\) belonged to was allocated for other regs",
  37: "ReadOperands: port_num-\d+/m_in_ports\[\d+\].m_in\[\d+\] fails as not found free cu",
  38: "Writeback: bank-\d+ of reg-\d+ is not idle",
}

stall_type_cycles = {
  0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, \
  11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, \
  21:0, 22:0, 23:0, 24:0, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, \
  31:0, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, \
}

def get_stall_type_cycles():
  import re
  for insn in all_sm_warp_insns:
    for stall_str in insn.stall_all_strs:
      for _ in range(len(stall_type_specific)):
        stall_t = stall_type_specific[_].split(': ')[0]
        stall_reason = stall_type_specific[_].split(': ')[1]
        if stall_t in stall_str:
          pattern = re.compile(stall_reason)
          match = pattern.match(insn.stall_strs[insn.stall_all_strs.index(stall_str)])
          if match:
            pass
            #print("@", insn.stall_strs[insn.stall_all_strs.index(stall_str)], "  |  ", stall_reason)
            stall_type_cycles[_] += 1
  # num_insn = 0
  # for insn in all_sm_warp_insns:
  #   num_insn += len(insn.stall_all_strs)
  # print(num_insn)
  #print("Stall Num:")
  #for _ in range(len(stall_type_cycles)):
  #  print('{0:>5}  |  '.format(str(stall_type_cycles[_])), stall_type_specific[_])

# 指令信息类，key: {pc, start_cycle. sid, wid}
class Insn:
  def __init__(self, pc, start_cycle, sid, wid):
    self.pc = pc
    self.insn_str = None
    self.start_cycle = start_cycle
    self.end_cycle = None
    self.sid = sid
    self.wid = wid
    self.stall_cycles = []
    self.flying_cycles = []
    self.stall_strs = []
    self.stall_all_strs = []
  
  def print(self):
    if self.insn_str == None or self.end_cycle == None:
      print("pc[%6s]: start_cycle[%8d], sid[%2d], wid[%2d]" % \
            (hex(self.pc), self.start_cycle, self.sid, self.wid))
    else:
      print("pc[%6s]: start_cycle[%8d], end_cycle[%8d], sid[%2d], wid[%2d], insn_str[%50s]" % \
            (hex(self.pc), self.start_cycle, self.end_cycle, self.sid, self.wid, self.insn_str.split("\n")[0]))
  
  def set_end_cycle(self, end_cycle):
    self.end_cycle = end_cycle
  
  def set_insn_str(self, insn_str):
    self.insn_str = insn_str

def find_insn(pc, sid, wid):
  for insn in all_sm_warp_insns:
    if insn.pc == pc and insn.sid == sid and insn.wid == wid:
      return insn
  return None

# "Start cycle"
def get_start_cycle(lines):
  for line in lines:
    if "Start cycle" in line:
      pc = int(line.split("pc[0x")[1].split("]")[0], 16)
      start_cycle = int(line.split("Start cycle[")[1].split("]")[0])
      sid = int(line.split("SM-")[1].split("/")[0])
      wid = int(line.split("wid-")[1].split(" ")[0])
      insn = Insn(pc, start_cycle, sid, wid)
      assert(insn.pc == pc)
      assert(insn.start_cycle == start_cycle)
      assert(insn.sid == sid)
      assert(insn.wid == wid)
      all_sm_warp_insns.append(insn)
      # insn.print()

# "End cycle"
def get_end_cycle(lines):
  for line in lines:
    if "End cycle" in line:
      # End cycle[21090]: SM-0/wid-1 end an insn, insn pc[0x0000]: 
      # pc[0x0000] w01[11111111111111111111111111111111]: 0000 ffffffff 1 R1 IMAD.MOV.U32 2 R255 R255 0
      pc = int(line.split("pc[0x")[1].split("]")[0], 16)
      end_cycle = int(line.split("End cycle[")[1].split("]")[0])
      sid = int(line.split("SM-")[1].split("/")[0])
      wid = int(line.split("wid-")[1].split(" ")[0])
      insn_str = line.split(": pc[0x")[1].split("]: ")[1]
      insn = find_insn(pc, sid, wid)
      # print("pc-%6s, sid-%2d, wid-%2d: " % (hex(pc), sid, wid))
      # assert(not insn == None) # yangjianchao16 del 20231028
      if insn == None:
        continue
      insn.set_end_cycle(end_cycle)
      insn.set_insn_str(insn_str)
      

# 在每次取指时会取两条指令到Ibuffer中，但可能最后一次取指的第二条指令不需要执行，因此在
# get_start_cycle()中会有多余的Insn对象被创建。这些Insn对象的end_cycle和insn_str都为
# None，这里需要将这些多余的指令删除。
def pop_invalid_insn():
  for insn in all_sm_warp_insns:
    if insn.end_cycle == None and insn.insn_str == None:
      # print("pc-%6s, sid-%2d, wid-%2d: " % (hex(insn.pc), insn.sid, insn.wid))
      all_sm_warp_insns.pop(all_sm_warp_insns.index(insn))

def get_issue_stall(lines):
  for line in lines:
    # Stall cycle[21091]: Issue, SM-0/wid-1 fails as scoreboard, insn pc[0x0050]: 
    # pc[0x0050] w01[11111111111111111111111111111111]: 0050 ffffffff 1 R0 IMAD 2 R0 R3 0 
    if "Stall cycle" in line and "Issue" in line and "pc[0x" in line:
      pc = int(line.split("pc[0x")[1].split("]")[0], 16)
      stall_cycle = int(line.split("Stall cycle[")[1].split("]")[0])
      sid = int(line.split("SM-")[1].split("/")[0])
      wid = int(line.split("wid-")[1].split(" ")[0])
      insn = find_insn(pc, sid, wid)
      assert(insn.insn_str == line.split("] w")[1].split("]: ")[1])
      assert(stall_cycle <= insn.end_cycle and stall_cycle >= insn.start_cycle)
      if (not stall_cycle in insn.stall_cycles) and (not stall_cycle == insn.end_cycle) and \
         (not stall_cycle == insn.start_cycle):
        insn.stall_cycles.append(stall_cycle)
        insn.stall_strs.append(line.split(", insn pc[")[0].split("fails as ")[1])
        insn.stall_all_strs.append(line)

def get_readoperands_stall(lines):
  for line in lines:
    # Stall cycle[22470]: ReadOperands, SM-0/wid-0 port_num-0/m_in_ports[0].m_in[5] fails as not found free cu, insn pc[0x0490]: 
    # pc[0x0490] w00[11111111111111111111111111111111]: 0490 ffffffff 1 R55 LEA.HI.X 2 R42 R43 0 
    if "Stall cycle" in line and "ReadOperands" in line and "pc[0x" in line:
      pc = int(line.split("pc[0x")[1].split("]")[0], 16)
      stall_cycle = int(line.split("Stall cycle[")[1].split("]")[0])
      sid = int(line.split("SM-")[1].split("/")[0])
      wid = int(line.split("wid-")[1].split(" ")[0])
      insn = find_insn(pc, sid, wid)
      assert(insn.insn_str == line.split("] w")[1].split("]: ")[1])
      assert(stall_cycle <= insn.end_cycle and stall_cycle >= insn.start_cycle)
      if (not stall_cycle in insn.stall_cycles) and (not stall_cycle == insn.end_cycle) and \
         (not stall_cycle == insn.start_cycle):
        insn.stall_cycles.append(stall_cycle)
        insn.stall_strs.append(line.split(", insn pc[")[0].split("fails as ")[1])
        insn.stall_all_strs.append(line)
        
def get_execute_stall(lines):
  for line in lines:
    # Stall cycle[22730]: Execute, SM-0/wid-2 fails as m_dispatch_reg has pending writes, insn pc[0x0590]: 
    # pc[0x0590] w02[11111111111111111111111111111111]: 0590 ffffffff 1 R10 LDG.E.64.SYS 1 R50 8 2 0x7fd106704020 
    # 8 8 8 232 8 8 8 232 8 8 8 232 8 8 8 232 8 8 8 232 8 8 8 232 8 8 8 232 8 8 8 
    if "Stall cycle" in line and "Execute" in line and "pc[0x" in line:
      # print(line)
      pc = int(line.split("pc[0x")[1].split("]")[0], 16)
      stall_cycle = int(line.split("Stall cycle[")[1].split("]")[0])
      # print(line.split("SM-")[1].split("/wid-")[0])
      sid = int(line.split("SM-")[1].split("/wid-")[0])
      wid = int(line.split("wid-")[1].split(" ")[0])
      insn = find_insn(pc, sid, wid)
      assert(insn.insn_str == line.split("] w")[1].split("]: ")[1])
      assert(stall_cycle <= insn.end_cycle and stall_cycle >= insn.start_cycle)
      if (not stall_cycle in insn.stall_cycles) and (not stall_cycle == insn.end_cycle) and \
         (not stall_cycle == insn.start_cycle):
        insn.stall_cycles.append(stall_cycle)
        insn.stall_strs.append(line.split(", insn pc[")[0].split("fails as ")[1])
        insn.stall_all_strs.append(line)

def get_writeback_stall(lines):
  for line in lines:
    # Stall cycle[23544]: Writeback, SM-0, bank-0 of reg-7 is not idle, insn pc[0x0710]: 
    # pc[0x0710] w04[11111111111111111111111111111111]: 0710 ffffffff 1 R7 FADD 2 R27 R7 0 
    if "Stall cycle" in line and "Writeback" in line and "pc[0x" in line:
      pc = int(line.split("pc[0x")[1].split("]")[0], 16)
      stall_cycle = int(line.split("Stall cycle[")[1].split("]")[0])
      sid = int(line.split("SM-")[1].split("/")[0])
      wid = int(line.split("wid-")[1].split(" ")[0])
      insn = find_insn(pc, sid, wid)
      assert(insn.insn_str == line.split("] w")[1].split("]: ")[1])
      # print(stall_cycle, insn.end_cycle, insn.start_cycle)
      assert(stall_cycle <= insn.end_cycle and stall_cycle >= insn.start_cycle)
      if (not stall_cycle in insn.stall_cycles) and (not stall_cycle == insn.end_cycle) and \
         (not stall_cycle == insn.start_cycle):
        insn.stall_cycles.append(stall_cycle)
        insn.stall_strs.append(line.split(", insn pc[")[0].split("fails as ")[1])
        insn.stall_all_strs.append(line)

def get_flying_cycles():
  for insn in all_sm_warp_insns:
    for cycle in range(insn.start_cycle, insn.end_cycle+1):
      if not cycle in insn.stall_cycles:
        insn.flying_cycles.append(cycle)

def get_min_start_cycle():
  min_start_cycle = 1000000000000
  for insn in all_sm_warp_insns:
    if insn.start_cycle < min_start_cycle:
      min_start_cycle = insn.start_cycle
  return min_start_cycle

def get_max_end_cycle():
  max_end_cycle = 0
  for insn in all_sm_warp_insns:
    if insn.end_cycle > max_end_cycle:
      max_end_cycle = insn.end_cycle
  return max_end_cycle

def get_sm_nums():
  sm_nums = set()
  for insn in all_sm_warp_insns:
    sm_nums.add(insn.sid)
  return sm_nums

def get_warp_nums():
  warp_nums = set()
  for insn in all_sm_warp_insns:
    warp_nums.add(insn.wid)
  return warp_nums

def get_max_pc():
  max_pc = 0
  for insn in all_sm_warp_insns:
    if insn.pc > max_pc:
      max_pc = insn.pc
  return max_pc

def get_min_pc():
  min_pc = 1000000000000
  for insn in all_sm_warp_insns:
    if insn.pc < min_pc:
      min_pc = insn.pc
  return min_pc

def classify_sm_warp_insn(sm_nums):
  for sm_num in sm_nums:
    if not sm_num in sm_warp_insns.keys():
      sm_warp_insns[sm_num] = {}
    for insn in all_sm_warp_insns:
      if insn.sid == sm_num:
        if not insn.wid in sm_warp_insns[sm_num].keys():
          sm_warp_insns[sm_num][insn.wid] = []
        sm_warp_insns[sm_num][insn.wid].append(insn)
        # print(insn.sid, insn.wid, insn.pc, insn.insn_str)

def plot_insn_stall_sid_wid(max_end_cycle, min_start_cycle, max_pc, min_pc, sid, wid):
  # sm_warp_insns, specify sid and wid:
  #   for insn in sm_warp_insns[sid][wid]:
  #     for cycle in insn.flying_cycles:
  #       x: cycle
  #       y: insn.pc/16
  # figure size:
  #   x: max_end_cycle - min_start_cycle + 1
  #   y: max_pc/16 - min_pc/16 + 1
  x_data = []
  y_data = []
  for insn in sm_warp_insns[sid][wid]:
    for cycle in insn.flying_cycles:
      x_data.append(cycle - min_start_cycle)
      y_data.append(max_pc/16 - min_pc/16 - insn.pc/16)

  import matplotlib.pyplot as plt
  plt.figure(figsize=(10, 10), dpi=50)
  plt.scatter(x_data, y_data, marker="_", s=2)
  plt.savefig("plot.pdf")

def plot_insn_stall_sid(max_end_cycle, min_start_cycle, max_pc, min_pc, sid):
  # sm_warp_insns, specify sid and wid:
  #   for insn in sm_warp_insns[sid][wid]:
  #     for cycle in insn.flying_cycles:
  #       x: cycle
  #       y: insn.pc/16
  # figure size:
  #   x: max_end_cycle - min_start_cycle + 1
  #   y: max_pc/16 - min_pc/16 + 1
  import matplotlib.pyplot as plt
  plt.figure(figsize=(10, 10), dpi=100)
  for wid in sm_warp_insns[sid].keys():
    x_data = []
    y_data = []
    for insn in sm_warp_insns[sid][wid]:
      for cycle in insn.flying_cycles:
        x_data.append(cycle - min_start_cycle)
        # y_data.append(max_pc/16 - min_pc/16 - insn.pc/16 - wid*0.0)
        y_data.append(insn.pc/16 + wid*0.0)
    plt.scatter(x_data, y_data, marker="_", s=1, label='wid: %2d'%wid)
  plt.xlim((0, max_end_cycle-min_start_cycle))
  plt.ylim((max_pc/16 - min_pc/16, 0))
  plt.xlabel("Cycle")
  plt.ylabel("Insn order")
  plt.legend()
  plt.savefig("plot.pdf")
  # plt.show()

def plot_insn_stall_sid_limited(max_end_cycle, min_start_cycle, max_pc, min_pc, sid, \
                                left_cycle, right_cycle, left_pc, right_pc):
  # sm_warp_insns, specify sid and wid:
  #   for insn in sm_warp_insns[sid][wid]:
  #     for cycle in insn.flying_cycles:
  #       x: cycle
  #       y: insn.pc/16
  # figure size:
  #   x: max_end_cycle - min_start_cycle + 1
  #   y: max_pc/16 - min_pc/16 + 1
  import matplotlib.pyplot as plt
  plt.figure(figsize=(10, 10), dpi=100)
  for wid in sm_warp_insns[sid].keys():
    x_data = []
    y_data = []
    for insn in sm_warp_insns[sid][wid]:
      for cycle in insn.flying_cycles:
        if left_cycle < cycle < right_cycle and left_pc < int(insn.pc/16) < right_pc:
            x_data.append(cycle - min_start_cycle)
            y_data.append(insn.pc/16 + wid*0.0)
    plt.scatter(x_data, y_data, marker="_", s=1, label='wid: %2d'%wid)
  # plt.xlim((0, max_end_cycle-min_start_cycle))
  plt.xlim((left_cycle - min_start_cycle, right_cycle-min_start_cycle))
  plt.ylim((right_pc - min_pc/16, left_pc - min_pc/16))
  plt.xlabel("Cycle")
  plt.ylabel("Insn order")
  plt.legend()
  plt.savefig("plot.pdf")
  # plt.show()

if __name__ == "__main__":
  f = open("./heartwall.txt", "r")
  lines = f.readlines()
  f.close()

  if not os.path.exists('all_sm_warp_insns.pkl'):
    print("Not exists all_sm_warp_insns.pkl...")
    get_start_cycle(lines)
    get_end_cycle(lines)
    pop_invalid_insn()
    
    get_issue_stall(lines)
    get_readoperands_stall(lines)
    get_execute_stall(lines)
    get_writeback_stall(lines)
    
    get_flying_cycles()
    
    f_save = open('all_sm_warp_insns.pkl', 'wb')
    pickle.dump(all_sm_warp_insns, f_save)
    f_save.close()
  else:
    print("Exists all_sm_warp_insns.pkl...")
    f_read = open('all_sm_warp_insns.pkl', 'rb')
    all_sm_warp_insns = pickle.load(f_read)
    f_read.close()
  
  min_start_cycle = get_min_start_cycle()
  max_end_cycle = get_max_end_cycle()
  sm_nums = get_sm_nums()
  warp_nums = get_warp_nums()
  
  max_pc = get_max_pc()
  min_pc = get_min_pc()
  
  if not os.path.exists('sm_warp_insns.pkl'):
    print("Not exists sm_warp_insns.pkl...")
    classify_sm_warp_insn(sm_nums)
  
    f_save = open('sm_warp_insns.pkl', 'wb')
    pickle.dump(sm_warp_insns, f_save)
    f_save.close()
  else:
    print("Exists sm_warp_insns.pkl...")
    f_read = open('sm_warp_insns.pkl', 'rb')
    sm_warp_insns = pickle.load(f_read)
    f_read.close()
  
  print("min_start_cycle, max_end_cycle, sm_num, warp_num:", \
        min_start_cycle, max_end_cycle, len(sm_nums), len(warp_nums))
  print("max_pc/16, min_pc/16:", int(max_pc/16), int(min_pc/16))
  
  sid = 0
  wid = 0
  left_cycle = 21000
  right_cycle = 24000
  left_pc_div16 = 30
  right_pc_div16 = 60
  
  # plot_insn_stall_sid_wid(max_end_cycle, min_start_cycle, max_pc, min_pc, sid, wid)
  # plot_insn_stall_sid(max_end_cycle, min_start_cycle, max_pc, min_pc, sid)
  # plot_insn_stall_sid_limited(max_end_cycle, min_start_cycle, max_pc, min_pc, sid, left_cycle, right_cycle, left_pc_div16, right_pc_div16)
  
  get_stall_type_cycles()
