def build_xml_element(tag, content, **kwargs):
    xml = "\"<" + tag
    for key, value in kwargs.items():
        xml += " " + key + "=\"" + value + "\\ \""
    xml += "> " + content + "< /" + tag + ">\""
    return xml

def main():
    print(build_xml_element ("a", "Hello there", href =" http://python.org ", _class =" my-link ", id= " someid "))

main()