#! /usr/bin/env python3

import sys, os
import shutil
import argparse
import logging
import logging.config
import http.server
import threading
import subprocess
import webbrowser

import serviceHandler

APP_NAME = 'mcop-sim-platform-gateway'
APP_VERSION = '0.1'
PORT_NUMBER = 8080
MY_FOLDER = os.path.dirname(os.path.realpath(__file__))


logging.basicConfig(stream = sys.stdout, level = logging.DEBUG,             
                    format = '%(levelname)-8s [%(name)-8s] %(message)s',)

def parse_args():
    """ Parsing arguments """

    def host_port(s):
        """ host:port type for argparse"""
        try:
            host, port = s.split(':')
            port = int(port)
            return host, port
        except:
            raise argparse.ArgumentTypeError('Server hostname must be address:port')

    parser = argparse.ArgumentParser(description = 'To parse some simple arguments',
                                     formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-iM', '--inputMode',
                        nargs='+',
                        type=str,
                        default='webserver',
                        help='Input mode launching the simulation platform (''webserver'' launches a webserver that wait for a form to be input; ''direct'' directly processes the command line arguments to launch the supervisor', metavar = 'webserver or direct')
    parser.add_argument('-ha', '--httpListenAddress',
                        type=str,
                        default='127.0.0.1',
                        help='Embedded webserver listen address', metavar='127.0.0.1 or ::')
    parser.add_argument('-hp', '--httpListenPort',
                        type=int,
                        default=8080,
                        help='Embedded webserver listen port', metavar='8080')
    parser.add_argument('-hP', '--http-admin-passwd',
                        type=str,
                        default='admin',
                        help='Embedded webserver admin password (for write routes)', metavar='admin')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Set default logger level to DEBUG instead of INFO')
	
    return parser.parse_args() 

def main(args):
    """
    Starting application...
    """
    if args.inputMode == 'webserver':

        print('Webserver is being launched')
        try:

            #Create a web server and define the handler to manage the
            #incoming request
            server_handler = serviceHandler.ServerHandler

            server_handler.args = args
            server = http.server.HTTPServer(('', PORT_NUMBER), server_handler)
            print('Started httpserver on port ', PORT_NUMBER)	

            # Pipe a new thread on the socket.close method in order to close the server
            # from the do_post command. Not sure if
            # server.socket.close is more appropriate than server.shutdown
            server_handler.assassin = threading.Thread(target=server.shutdown)
            server_handler.assassin.daemon = True

            mainURL = f'http://{args.httpListenAddress}:{args.httpListenPort}/WhatIfAnalysesTool/'

            #open default browser
            os.system(f'xdg-open {mainURL}')


            #Wait forever for incoming http requests
            server.serve_forever()

        # This part of code below is apparently not necessary to catch the ctrl+c
        except KeyboardInterrupt:
            print('^C received, shutting down the web server')
            server.socket.close()
    else:
        print('Not implemented yet')
    
    # Coded but useless as there is no event programming yet
    logger.info("Event loop running forever, press Ctrl+C to interrupt.")
    logger.info("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
     
if __name__ == '__main__':

    # Raise terminal size to maximum
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)

    # Init logger
    logging.basicConfig(level=logging.DEBUG, format = '%(levelname)-8s [%(name)-8s] %(message)s')

    logger = logging.getLogger('__main__')

    # Parse arguments for basic configuration of the federate
    print("Parsing command line arguments")
    args = parse_args()

    main(args)




# -*- coding: utf-8 -*-

