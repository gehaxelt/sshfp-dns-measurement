import logging

logger = logging.getLogger('test')

logger.setLevel(getattr(logging, 'DEBUG'))

logger.addHandler(logging.FileHandler("test.log"))


import csv
import io

output = io.StringIO()

writer = csv.writer(output)
writer.writerow(["test", 1, "fooba,r'\\"])

print(output.getvalue())

writer.writerow(["test2", 1, "foo,bar2'\\"])

print(output.getvalue())

logger.info(output.getvalue())