#!/usr/bin/env python
# William Wu, 2013-06-26
import os, sys, datetime, getopt, subprocess

# parameters
author_name = "William Wu"
time_fmt = "%Y-%m-%d %H:%M"

# usage
def usage():
    print('Usage:\n\t%s' % sys.argv[0])
    print('Synopsis:')
    print('\tGenerates bare git repository with e-mail hooks enabled.')

# main method
def main(argv):
    
    # defaults
    prompts_flag = True
    directory_name = "project.git"
    project_description = "project"
    email_addresses = ["willywutang@gmail.com"]
        
    # command-line argument parsing
    try:
        opts, args = getopt.gnu_getopt(argv, "fh", ["fast","help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--fast"):
            prompts_flag = False
                
    # gather parameters from user
    if prompts_flag: 
        directory_name = raw_input("Enter directory name: ").strip()
        project_description = raw_input("Enter project description: ").strip()
        email_addresses = raw_input("Enter e-mail addresses of developers, separated by spaces: ").split()

    # construct git repository
    os.system("mkdir %s" % directory_name)
    os.chdir(directory_name)
    process = subprocess.Popen(['git', 'init', '--bare'], shell=False, stdout=subprocess.PIPE)
    process.communicate()
    os.system("git config hooks.mailinglist \"%s\"" % (", ".join(email_addresses)) )
    os.system("git config hooks.emailprefix \"[git] \"")
    os.system("echo '(%s) ' > description" % project_description )
    os.chdir("hooks")
    os.system("sed -e \"s/#\. //g\" post-receive.sample > post-receive")

# invoke main
if __name__ == "__main__":
    main(sys.argv[1:])