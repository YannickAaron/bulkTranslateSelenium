from SeleniumTranslator import *

from time import sleep

translator = SeleniumTranslator("de","en-US")

print(translator.translate("Hallo ich bin ein Test ob das hier geht"))

translator.exit()