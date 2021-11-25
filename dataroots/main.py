import os
import sys


lib_path = os.path.abspath("..")
sys.path.append(lib_path)

lib_path = os.path.abspath("../base")
sys.path.append(lib_path)



from base import api, web_client, endpoint

def main():
    print("Hello world")

if __name__ == "__main__":
    main()
