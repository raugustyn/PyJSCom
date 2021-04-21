#  -*- coding: utf-8 -*-
###########################################################
#                                                         #
# Copyright (c) 2018 Radek Augustýn, licensed under MIT.  #
#                                                         #
###########################################################
__author__ = "radek.augustyn@email.cz"
# @PRODUCTION MODULE [Full]

import os, codecs

import logging as log

def fileToStr(fileName, encoding="utf-8", baseFileName=None):
    """fileRead aliaz. Reads file content using encoding specified, utf-8 as default if parameter not provided.

    :param str fileName: name of the file
    :param str encoding: encoding codec name, utf-8 as a default

    :return: file content as a string
    :rtype: str

    >>> content = fileRead(__name__ + ".py")
    >>> content.startswith("# -*- coding: utf-8 -*-")
    True
    """
    return fileRead(fileName, encoding, baseFileName)

def fileRead(fileName, encoding="utf-8", baseFileName=None):
    """ Reads file content using encoding specified, utf-8 as default if parameter not provided.

    :param str fileName: name of the file
    :param str encoding: encoding codec name, utf-8 as a default

    :return: file content as a string
    :rtype: str

    >>> content = fileRead(__name__ + ".py")
    >>> content.startswith("# -*- coding: utf-8 -*-")
    True
    """
    if baseFileName:
        fileName = os.path.dirname(baseFileName) + os.sep + fileName

    if os.path.exists(fileName) and os.path.isfile(fileName):
        file = codecs.open(fileName, "r", "utf-8")
        result = file.read()
        file.close()
        return result

def getFileContent(fileName):
    """Reads file content into string. Obsolete function provided for backward compatibility only.
    New code should use fileRead instead.

    :param str fileName: name of the file

    :return: file content as a string
    :rtype: str

    """
    if os.path.exists(fileName) and os.path.isfile(fileName):
        f = open(fileName, "rb")
        s = f.read()
        f.close()
        return s

def getFileExtension(path):
    """getExtension aliaz. Extracts file extension of the given path.

    :param str path: path or file name

    :return: extension including separator
    :rtype: str

    >>> getFileExtension("c:/temp/test.html")
    '.html'
    """
    return getExtension(path)


def getExtension(path):
    """ Extracts file extension of the given path.

    :param str path: path or file name

    :return: extension including separator
    :rtype: str

    >>> getExtension("c:/temp/test.html")
    '.html'
    """
    (fileName, fileExtension) = os.path.splitext(path)
    return fileExtension

def pathLeaf(path):
    """ Extracts file name or directory name from given path.

    :param str path: Full or relative path

    :return: File name from given path.
    :rtype: str

    >>> pathLeaf("c:/temp/test.html")
    'test.html'

    >>> pathLeaf("c:/temp/")
    'temp'

    """
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def replaceStringBlocks(str: str, startId: str, endId: str, newContent: str):
    """ Replaces all string sections in blocks given by startId and endId tags by newContent.

    :param str str: Text content to be updated.
    :param str startId: Start identifier of the block to be replaced.
    :param str endId: End identifier of the block to be replaced.
    :param str newContent: New text content.

    :return: Updated str block.
    :rtype: str


    >>> replaceStringBlocks("Text pred.<ReplaceStart>StaryText<ReplaceEnd>Text za.", "<ReplaceStart>", "<ReplaceEnd>", "Next content.")
    'Text pred.Next content.Text za.'

    """
    endPos = 0
    while True:
        startPos = str.find(startId, endPos)
        endPos = str.find(endId, startPos)
        if startPos < 0 or endPos < startPos:
            break

        str = str[:startPos] + newContent + str[endPos + len(endId):]

    return str


def replaceHTMLBlock(html, commentIdentifier, newContent):
    """ Replaces html content in block of <!-- commentIdentifier -->Old content<!-- end of commentIdentifier --> by new value.

    :param html: source html containing section(s) to be replaced
    :param commentIdentifier: identifier of section to be replaced
    :param newContent: new content of identified section

    :return: resulting html

    >>> html = "<html><body><h1>Title</h1><p><!-- content -->Here should be page content<!-- end of content --></p></body></html>"
    >>> html = replaceHTMLBlock(html, "content", "My content of page.")
    >>> print html
    <html><body><h1>Title</h1><p>My content of page.</p></body></html>
    """
    commentIdentifier = commentIdentifier.strip()
    startId = ("<!-- %s -->" % commentIdentifier).upper()
    endId = ("<!-- END OF %s -->" % commentIdentifier).upper()
    while html.upper().find(startId) >= 0:
        upperCase = html.upper()
        startPos = upperCase.find(startId)

        endPos = upperCase.find(endId)
        if endPos < 0:
            import logging
            logging.error("replaceHTMLBlock endPos(%d) < 0" % (endPos))
            return html

        endCutPos = upperCase.find("-->", endPos) + 3
        if endCutPos < 3:
            return html

        if startPos>=0 and endCutPos>=0:
            html = html[:startPos] + newContent + html[endCutPos:]

    return html


def initializeJavaScriptVariable(html, variableName, value):
    startId = "var %s = " % variableName
    return replaceStringBlocks(html, startId, ";", startId + value + ";")


def replaceJavaScriptBlock(html, commentIdentifier, newContent):
    """Replaces JavScript code block in html code.

    :param html: Source html code.
    :param commentIdentifier: JavaScript comment identifier.
    :param newContent: New content of the block.

    :return: html with replaced blocks of code.


    """
    identifier = commentIdentifier.upper().strip()
    html = replaceStringBlocks(html, "// %s" % identifier, "// END OF %s" % identifier, newContent)
    html = replaceStringBlocks(html, "/* %s */" % identifier, "/* END OF %s */" % identifier, newContent)

    return html


def replaceHTMLTags(html, tags):
    """Replace HTML tags.

    <#LOGLINES#/> ... just replace values
    <#LOGLINES#> ... replace in block
    /* DATA */ ... replace data in block
    //DATA ... replace data in block

    :param html:
    :param tags:

    :return:

    """
    for tagName, value in tags.items():
        if (tagName.startswith("<") and tagName.endswith("/>")):
            html = html.replace(tagName, value)
        elif tagName.startswith("//"):
            html = replaceJavaScriptBlock(html, tagName[3:], value)
        elif tagName.startswith("<"):
            html = replaceHTMLBlock(html, tagName[2:], value)
        elif tagName.startswith("/*") and tagName.endswith("*/"):
            html = replaceJavaScriptBlock(html, tagName[2:len(tagName)-2], value)

    return html


def strToBool(s):
    return s.lower() in ["true", "T", "1"]


class HTMLTemplateProcessor:

    def __init__(self, templateFileName):
        log.debug("Reading HTML Templates from '%s'" % templateFileName)
        self.templates = {}
        templatesContent = fileToStr(templateFileName)
        searchPos = 0
        while True:
            templateEndMarker_StartPos = templatesContent.find("<!-- END OF ", searchPos)
            if templateEndMarker_StartPos >= 0:
                templateEndMarker_EndPos = templatesContent.find("-->", templateEndMarker_StartPos)
                templateName = templatesContent[templateEndMarker_StartPos+12:templateEndMarker_EndPos].strip()
                templateStartMarker_StartPos = templatesContent.find("<!-- %s -->" % templateName, searchPos)
                if templateStartMarker_StartPos>=0:
                    templateContent = templatesContent[templateStartMarker_StartPos+len(templateName)+9:templateEndMarker_StartPos]
                    self.templates[templateName] = templateContent
                else:
                    log.error("'%s' not found" % "<!-- %s -->" % templateName)
                searchPos = templateEndMarker_EndPos + 3
            else:
                break

        log.info("Template names:%s (HTMLTemplateProcessor)" % str(self.templates.keys()))
        #log.closeSection()


    def processContent(self, content, fileName=""):
        for templateName, templateContent in self.templates.items():
            log.debug("Found template '%s'" % templateName)
            content = replaceHTMLBlock(content, templateName, templateContent)

        if fileName: # Bootstrap active menu item
            fileName = pathLeaf(fileName)
            content = content.replace('<li class="active">', '<li>')
            content = content.replace("<li class='active'>", '<li>')
            content = content.replace('<li><a href="%s">' % fileName, '<li class="active"><a href="%s">' % fileName)
            content = content.replace("<li><a href='%s'>" % fileName, "<li class='active'><a href='%s'>" % fileName)

        return content


    def processFile(self, fileName):
        return self.processContent(fileToStr(fileName))


class VariableReplaceProcessor:
    def __init__(self, items={}):
        self.items = items


    def processContent(self, content, fileName=""):
        for key, value in self.items.items():
            content = content.replace("{{%s}}" % key, str(value))
        return content



# @NO-PRODUCTION CODE
if __name__ == "__main__":
    processor = HTMLTemplateProcessor("C:/ms4w/Apache/htdocs/Generalizace/projects/Tutorials/01_DataExtraction/manager_data/CodeTemplates.html")
    processor.processFileContent("C:\Python27\Lib\site-packages\mapgen\manager\web\manager\Data.html")
