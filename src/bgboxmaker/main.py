import argparse
import logging
import yaml
import sys
import os
from bgboxmaker import Box, BoxConfig, ConfigurationError
from PIL import Image, ImageDraw, ImageFont

def main():
    parser = argparse.ArgumentParser(description='Generate Tuck')
    parser.add_argument('-f', '--filename', help='YAML data file', default="")
    parser.add_argument('-s', '--sample', dest='sample', action='store_true',
                    help='Generate sample YAML with instructions.')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help='Activate debug log')

    args = parser.parse_args()
    if args.debug:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    logfile = f"{os.getcwd()}/bgboxmaker.log"

    logging.basicConfig(
        level = loglevel,
        format = "{asctime} {levelname:<8} {message}",
        style = "{",
        filename = logfile,
        filemode='w'
    )

    if not args.filename == "":
        with open(args.filename, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    else:
        if args.sample:
            sys.exit(0)
        else:
            sys.exit(1)

    try:
        config = BoxConfig(data)
    except ConfigurationError:
        print("Invalid configuration. See logfile for details.")
        print("See https://github.com/thetalorian/bgboxmaker for usage instructions.")
        sys.exit(1)

    box = Box(config)
    logging.info(f"{box}")
    box.generate()
    #box.test_generate()

if __name__ == "__main__":
    main()