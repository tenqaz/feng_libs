from feng_libs.utils import ExcelUtils

excel = ExcelUtils()
excel.load("1.xlsx")
print(excel.get_cell_value(0,0))