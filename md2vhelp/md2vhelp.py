# md2vhelp - md2vhelp.py

# Created by Thomas Da Costa <tdc.input@gmail.com>

# Copyright (C) 2014 Thomas Da Costa

# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.


import os
import sys
import argparse
import logging
import re


def print_line(symbol, on = 78):
    print symbol * on


def print_both_sides(left, right, space = ' ', on = 78):
    space_len = on - len(right) - len(left) - 2
    print '%s %s %s' % (left, space * space_len, right)


def print_right(text, space = ' ', on = 78):
    begin = on - len(text)
    if begin < 0:
        bebin = 0
    print '%s%s' % (space * begin, text)


def print_center(text, space = ' ', on = 78):
    begin = (on / 2) - len(text) / 2
    if begin < 0:
        bebin = 0
    print '%s%s' % (space * begin, text)


def process(title, chapters, plugin):
    print '*%s.txt*' % plugin
    print '*%s*' % plugin
    print
    print_center('%s~' % title)
    print_line('=')
    print
    for i, chapter in enumerate(chapters):
        chapter['tag'] = re.sub(
                r'[^0-9a-zA-Z]+',
                '-',
                '%s-%s' % (plugin, chapter['title'].lower()))
        print_both_sides(
                '%2d. %s' % (i + 1, chapter['title']),
                '|%s|' % chapter['tag'],
                '.'
                )
    print
    for i, chapter in enumerate(chapters):
        print_line('=')
        print_right('*%s*' % chapter['tag'])
        print '%2d. %s~' % (i + 1, chapter['title'])
        for c in chapter['content']:
            print c
    print
    print 'vim:tw=78:ts=8:ft=help:norl:'


def parse(content):
    title = ''
    chapters = []
    title_regex = r'==='
    chapter_regex = r'---'
    for i, line in enumerate(content):
        if re.search(title_regex, line):
            if title:
                logging.warning('more than one title detected')
            title = str.strip(content[i - 1])
        elif re.search(chapter_regex, line):
            if chapters:
                chapters[-1]['content'].remove(chapters[-1]['content'][-1])
            chapters.append(
                    {'title': str.strip(content[i - 1]), 'content': []}
                    )
        else:
            if chapters:
                chapters[-1]['content'].append(line.rstrip('\n'))
    if not title:
        logging.warning('no title detected')
    if not chapters:
        logging.warning('no chapter detected')
    return title, chapters


def md2vhelp(file_name, plugin):
    try:
        with open(file_name) as f:
            content = f.readlines()
        title, chapters = parse(content)
        process(title, chapters, plugin)
    except IOError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)


def get_args():
    parser = argparse.ArgumentParser(
            description = 'Convert simple markdown file to vim help format'
            )
    parser.add_argument(
            'file',
            help = 'file to be processed'
            )
    parser.add_argument(
            'plugin',
            help = 'plugin name'
            )
    parser.add_argument(
            '-v',
            '--verbose',
            action = 'store_true',
            help = 'increase output verbosity'
            )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    logging.basicConfig(
            level = level,
            format = '%(levelname)s: %(message)s'
            )
    if os.path.isfile(args.file):
        md2vhelp(args.file, args.plugin)
    else:
        logging.error('%s is not a valid file' % args.file)
