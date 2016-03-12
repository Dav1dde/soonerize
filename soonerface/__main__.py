import sys

from soonerface import create_application
from soonerface.face import soonerize
import argparse
import cv2


def www(ns):
    app = create_application(debug=ns.debug, verbose=ns.verbose)
    app.run(port=int(ns.port), host=ns.host)


def local(ns):
    image = cv2.imread(ns.i)
    image = soonerize(image)

    cv2.imshow('Sooner Me', image)
    cv2.waitKey(0)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    www_parser = subparsers.add_parser('www')
    www_parser.add_argument('--port', default=5000, help='Port to listen on.')
    www_parser.add_argument('--host', default='127.0.0.1', help='Host to bind to.')
    www_parser.add_argument('--debug', action='store_true', help='TESTING ONLY')
    www_parser.add_argument('--verbose', action='store_true', help='Log to stdout and stderr')

    local_parser = subparsers.add_parser('local')
    local_parser.add_argument('-i', required=True)
    ns = parser.parse_args()

    func = getattr(sys.modules[__name__], ns.subparser_name)
    func(ns)


if __name__ == '__main__':
    main()
