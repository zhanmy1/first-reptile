import FileUtil
import conf

row = FileUtil.get_file_rows(conf.projects[0],'/core/src/main/java/org/apache/mahout/fpm/pfpgrowth/package-info.java')
print(row)

s = 'ababa'

print(len(s.split('a')))