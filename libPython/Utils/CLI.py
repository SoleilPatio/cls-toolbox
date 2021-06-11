import subprocess


def Run(command_str, sync_output = False):
    print "Run: %s"%command_str
    if sync_output:
        subprocess.call(command_str)
        print "----------"
    else:
        output = subprocess.check_output(command_str)
        print "Output: %s"%output
        print "----------"
        return output
        


if __name__ == '__main__':
    pass