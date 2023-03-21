import time
import datetime

# datetime object containing current date and time

# dd/mm/YY H:M:S

def quad_data_assert(data):
    assert type(data) is list
    assert type(data[0]) is list
    assert len(data)==4
    return True

def write_file_dump(ch1,ch2,ch3,ch4):
    #quad_data_assert(data)
    stamp = datetime.datetime.utcnow()
    file = open('quadcell_reading/%s_%s.txt'%('raw_quad_dump',stamp),'w')
    for i in len(ch1):
        file.write(str(ch1[i])+" "+str(ch2[i])+" "+str(ch3[i])+" "+str(ch4[i]))
    file.close()

def read_file():
    pass

if __name__=="__main__":
    write_file_dump(["Hi"])