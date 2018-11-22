from feng_libs.utils import ExcelUtils

eu = ExcelUtils()
eu.load('绑定优化方案小范围公测第二批测试.xlsx')
print(eu.sheet_names)
print(eu.get_column_values(1))
