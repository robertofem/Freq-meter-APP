#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import sys

if __name__ == '__main__':
    from model import startup
    sys.exit(startup.run())
