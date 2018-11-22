'''
    author: jim
    date: 2018-09-07

    操作excel的工具类

    TODO(2018-09-07): 目前还不完善，只有简单读功能，后续如有需要加上写功能
'''
import xlrd


class ExcelUtils:

    __slots__ = ['sheet_names', 'cur_sheet_name', 'cur_sheet', 'workbook']

    def __init__(self):
        pass

    def load(self, file):
        '''加载文件

        Args:
            file: 文件路径

        '''
        self.workbook = xlrd.open_workbook(file)
        self.sheet_names = self.workbook.sheet_names()
        self.cur_sheet_name = self.sheet_names[0]
        self.cur_sheet = self.workbook.sheet_by_index(0)

    def select(self, sheet_name_or_index):
        ''' 选择sheet

        Args:
            sheet_name_or_index: sheet的名字或索引

        '''
        if isinstance(sheet_name_or_index, int):
            self.cur_sheet_name = sheet_names[sheet_name_or_index]
            self.cur_sheet = self.workbook.sheet_by_index(sheet_name_or_index)
        elif isinstance(sheet_name_or_index, str):
            self.cur_sheet_name = sheet_name_or_index
            self.cur_sheet = self.workbook.sheet_by_name(sheet_name)

    def get_row_values(self, row):
        '''获取指定行的数据

        Args:
            row: 行数,int

        Return:
            一行的数据. list
        '''
        return self.cur_sheet.row_values(row)

    def get_column_values(self, col):
        ''' 获取指定列的数据

        Args:
            col: 列数

        Return:
            返指定列的数据. list
        '''
        return self.cur_sheet.col_values(col)

    def get_cell_value(self, row, col):
        """ 获取指定单元格的值

        Args:
            row: 行, int
            col: 列, int

        Return:
            单元格的值
        """

        return self.cur_sheet.cell_value(row, col)


if __name__ == '__main__':
    eu = ExcelUtils()
    eu.load('绑定优化方案小范围公测第二批测试.xlsx')
    # print(eu.sheet_names)
    # print(eu.get_row_values(0))
    # print(eu.get_column_values(1))

    print(eu.get_cell_value(2, 1))
