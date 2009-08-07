#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""wikigrab.py - Wiki Grabber"""

import urllib
import os
import os.path
import re
import dircache
import codecs
import htmlentitydefs
import random
import gtranslate
import sfjp

from BeautifulSoup import BeautifulSoup

class WikiPusherError(Exception):
    def __init__(self, name, value):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name + ":" + repr(self.value)

class WikiPusher(object):
    """Wiki grabbing tool"""

    def __init__(self, config):
        """Constructor"""
        self._config = config


    def get_config(self, string):
        """get config value"""
        return self._config[string]


    def _read(self, pathname):
        f = codecs.open(pathname, "r", "utf-8")
        text = f.read()
        f.close()
        return text


    def entity2unicode(self, text):
        reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
        num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
        num10_regex = re.compile(u'#\d+', re.IGNORECASE)

        result = u''
        i = 0
        while True:
            match = reference_regex.search(text, i)
            if match is None:
                result += text[i:]
                break

            result += text[i:match.start()]
            i = match.end()
            name = match.group(1)

            # 実体参照
            if name in htmlentitydefs.name2codepoint.keys():
                result += unichr(htmlentitydefs.name2codepoint[name])
            # 文字参照
            elif num16_regex.match(name):
                # 16進数
                result += unichr(int(u'0'+name[1:], 16))
            elif num10_regex.match(name):
                # 10進数
                result += unichr(int(name[1:]))

        return result
        
    def _repl_link(self, map, link):
        m = re.match(r"\[(.*?)\s+(.*)\]", link)
        if m:
            url = m.group(1)
            linkstr = m.group(2)
        else:
            url = link.strip("[]")
            linkstr = url

        id = """<a href="%s">%s</a>""" % (url, linkstr)
        map[id] = link

        return id

    def itranslate(self, text):
        """interigent translator"""
        map = {}
        repl = lambda m: self._repl_link(map,m.group(0))
        rex = re.compile(r"\[.*?\]", re.S)

        tmp = rex.sub(repl, text)

#        print "\n\n", tmp, "\n\n"

        tmp = gtranslate.translate(tmp)
#        for key in map:
#            tmp = tmp.replace(key, map[key])
        tmp = re.sub(r"""<a href="(.*?)">(.*?)</a>""", r"[\1 \2]", tmp)
        return self.entity2unicode(tmp)
        

    def callback(self, url, file, text):
        regex_list = [
            (r"\[\[(.*?)\|(.*?)\]\]",  r"[\1 \2]"),
            (r"\[\[(.*?)\]\]", r"[\1]"),
            (r"\*\*(.*?)\*\*", r"'''\1'''"),  # bold
            (r"http://", "http-+-"),
            (r"https://", "https-+-"),
            (r"//(.*?)//", r"''\1''"),  # italic
#            (r"\\\\", r"<tmpbr>"),
            (r"\\\\", r" "),
            (r"^======([^=].*?)======", r"= \1"),
            (r"^=====([^=].*?)=====", r"== \1"),
            (r"^====([^=].*?)====", r"=== \1"),
            (r"^===([^=].*?)===", r"==== \1"),
            (r"^==([^=].*?)==", r"===== \1"),
            (r"^=([^=].*?)=", r"====== \1"),
            (r"^\s+-\s(.*?)", r" 1. "),
            (r"\[(.*?):(.*?) (.*)\]", r"[\1-\2 \3]"),
            (r"(http|https)\-\+\-", r"\1://"),
            (r"&quot;", r'"'),
            ]

        code_mode = 0;

        output = []
        translation_buffer = ""
        regex_p = re.compile(r"^[A-Za-z0-9]")
        regex_h = re.compile(r"^=")
        regex_ol = re.compile(r"^\s+1.")
        regex_ul = re.compile(r"^\s+\*")

        # substitute <code></code> block
        repl = lambda m: "\n " + m.group(1).replace("\n", "\n ")
        rex_code_m = re.compile(r"&lt;code&gt;(.*?)&lt;/code&gt;", re.S)
        text = re.sub(r"&lt;code&gt;(.*?)&lt;/code&gt;", r"\n\n \1 \n\n", text)
        text = rex_code_m.sub(repl, text)

        for line in text.split("\n"):
            line = line.rstrip()
            for (regex, subst) in regex_list:
                line = re.sub(regex, subst, line)

            if regex_p.search(line):
                translation_buffer = translation_buffer + line
            else:
                if not translation_buffer == "":
                    japanese = self.itranslate(translation_buffer)
                    hidden = "{{{ comment \n" + translation_buffer + "\n}}}\n"
                    output.append(hidden)
                    output.append(japanese)
                    output.append("")
                    translation_buffer = ""
                if regex_h.search(line):
                    m = re.search(r"^(=+)\s*?(.*)\s*=*$", line)
                    lv = m.group(1)
                    h_txt = m.group(2)
                    japanese = self.itranslate(h_txt)
                    output.append("{{{ comment\n" + line + "\n}}}\n")
                    line = u"%s %s" % (lv, japanese)
                if regex_ol.search(line):
                    m = re.search(r"^(\s+1.)\s*?(.*)$", line)
                    lv = m.group(1)
                    h_txt = m.group(2)
                    japanese = self.itranslate(h_txt)
                    output.append("{{{ comment\n" + line + "\n}}}\n")
                    line = u"%s %s" % (lv, japanese)
                if regex_ul.search(line):
                    m = re.search(r"^(\s+\*)\s*?(.*)$", line)
                    lv = m.group(1)
                    h_txt = m.group(2)
                    japanese = self.itranslate(h_txt)
                    output.append("{{{ comment\n" + line + "\n}}}\n")
                    line = u"%s %s" % (lv, japanese)
                output.append(line)

        if not translation_buffer == "":
            japanese = self.itranslate(translation_buffer)
            hidden = "{{{ comment \n" + translation_buffer + "\n}}}\n"
            output.append(hidden)
            output.append(japanese)
            translation_buffer = ""        

        footer = u"""
{{{ html
<div style="border:1px solid; background:#EEEEEE;padding:4px;margin-top:2em;">
<a href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img src="http://sourceforge.jp/projects/ffdshow-tryout/wiki/home/attach/cc-by-nc-sa.png" alt="cc-by-nc-sa" title="cc-by-nc-sa.png" height="15" width="80"></a> このWikiページは、<a href="%s">ffdshow wiki</a>を日本語訳したものです。
</div>
}}}
"""
        file = "http://ffdshow-tryout.sourceforge.net/wiki/" + file.replace("-", ":")
        output.append(footer % file)

        #print "\n".join(output).encode("utf-8")
        return "\n".join(output)


    def run(self):
        """Run grubbber"""
        target_dir = self.get_config("dir")
        prefix = self.get_config("prefix")
        for file in dircache.listdir(target_dir):
            filepath = os.path.join(target_dir, file)

            # print file, filepath
            if re.search(r"\.txt$", file):
                if os.path.isfile(filepath):
                    bodytext = self._read(filepath)

#                    file = file.replace("-", "/")
                    file = file.replace(".txt", "")
                    url = self.get_config("prefix") + file + "?action=update"
                    bodytext = self.callback(url, file, bodytext)
                    params = dict(textarea_height="24", text=bodytext, commit=u"保存", comment="")
                    print "post: %s" % (url,)
                    #print bodytext.encode("utf-8")
                    self.push_by_post(url, params)
                    


    def check_config(self):
        """check config"""
        key_vital = ["prefix", "dir", "max_recur"]
        for key in key_vital:
            if not self._config.has_key(key):
                raise WikiPusherError("config_no_vital_key", key_vital)

    def push_by_post(self, url, params):
        """grab given url as local html by POST method"""
        for key in params:
            if isinstance(params[key], unicode):
                params[key] = params[key].encode("utf-8")
        encoded_params = urllib.urlencode(params)

        sfjp_opener = sfjp.FancyURLopenerWithCookie()
        try:
            sfjp_opener.load_cookie("./cookie")
        except IOError:
            sys.stderr.write("cannot use cookie file. create.\n")

        if sfjp_opener.get_cookie() == "":
            try:
                uname = raw_input("user: ")
            except KeyboardInterrupt:
                sys.exit("\nabort.")

            try:
                passwd = getpass.getpass("login password:")
            except KeyboardInterrupt:
                sys.exit("\nabort.")
                if sfjp_opener.login(uname, passwd) != 1:
                    sys.exit("login error!")
                    
            sfjp_opener.login(uname, passwd)
            sfjp_opener.save_cookie("./cookie")
        sfjp_opener.regist_cookie()

        urllib._urlopener = sfjp_opener

        u = urllib.urlopen(url, encoded_params)
        data = u.read()
#        print data
        return data

