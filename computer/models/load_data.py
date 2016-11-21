import random

# Return tuple: (ys, xs) 
def getBatch(data_dir, batch_size):
    with open(data_dir, 'r') as fin:
        lines = fin.readlines()
        batch_lines = random.sample(range(len(lines)), batch_size)

        ys = []
        xs = []
        
        for line in batch_lines:
            nums = [int(x) for x in lines[batch_lines].split(" ")]
            ys += nums[0]
            xs += nums[3:]

        return (ys, xs)
