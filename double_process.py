###############只处理数据,对数据进行插值处理
import pandas as pd
from scipy.interpolate import interp1d

#####文件名字
EXO_ON_trc = r'HIL\a.trc'
NO_EXO_trc = r'HIL\b.trc'

NEW_EXO_ON_TRC = r'HIL\generation\NEW_EXO_ON_TRC.trc'
NEW_NO_EXO_TRC = r'HIL\generation\NEW_NO_EXO_TRC.trc'

# 内插处理函数
def interpolate_data(column):
    indices = column.index
    non_nan_indices = indices[~column.isna()]

    if len(non_nan_indices) == 0:
        # 如果所有值都是空值，无法进行插值，返回原列
        return column

    # 使用有效数据的索引和值创建插值函数
    interpolator = interp1d(non_nan_indices, column[non_nan_indices], fill_value="extrapolate")

    # 执行插值
    interpolated_values = interpolator(indices)

    # 创建新列，只替换空值部分
    new_column = column.copy()
    new_column[column.isna()] = interpolated_values[column.isna()]

    return new_column


# 外插处理函数
def extrapolate_data(column):
    indices = column.index
    non_nan_indices = indices[~column.isna()]

    if len(non_nan_indices) == 0:
        return column

    head_index = non_nan_indices[0]
    tail_index = non_nan_indices[-1]

    # 使用首尾有效数据的索引和值创建外插值函数
    interpolator = interp1d([head_index, tail_index], [column[head_index], column[tail_index]],
                            fill_value="extrapolate")

    # 对每列的开头或结尾为空的情况进行外部插值
    extrapolated_values = column.apply(lambda x: interpolator(x) if pd.isna(x) else x)

    # 创建新列，只替换开头或结尾为空的部分
    new_column = column.copy()
    new_column[(pd.isna(column.iloc[0]) or pd.isna(column.iloc[-1]))] = extrapolated_values[
        (pd.isna(column.iloc[0]) or pd.isna(column.iloc[-1]))]

    return new_column


# 数据处理函数
def process_data(file):
    # 读取原始 TRC 文件数据
    trcdatatable = pd.read_csv(file, sep='\t', header=4)
    # 对每列进行内插和外插处理
    # 对每列进行内插处理，如果有缺失值则进行内插，否则保持不变
    processed_data = trcdatatable.apply(lambda col: interpolate_data(col) if col.isna().any() else col)
    # 进一步处理已处理的数据，如果首或尾元素缺失，则进行外插，否则保持不变
    processed_data = processed_data.apply(
        lambda col: extrapolate_data(col) if pd.isna(col.iloc[0]) or pd.isna(col.iloc[-1]) else col)
    return processed_data

if __name__=="__main__":
    #处理第穿exo的文件
    new_EXO_ON_data = process_data(EXO_ON_trc)
    #处理没穿exo的文件
    new_NO_EXO_data = process_data(NO_EXO_trc)

    # 保存新的数据到新文件 NEW_EXO_ON_TRC.trc
    new_EXO_ON_data.to_csv(NEW_EXO_ON_TRC, sep ='\t',index =False )
    print("Interpolation and save completed in NEW_EXO_ON_TRC.trc.")

    # 保存新的数据到新文件 NEW_NO_EXO_TRC.trc
    new_NO_EXO_data.to_csv(NEW_NO_EXO_TRC, sep ='\t',index =False )
    print("Interpolation and save completed in NEW_NO_EXO_TRC.trc.")


