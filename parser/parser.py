
index_for_row_name, index_for_col_name, index_for_data_name = 0, 0, 0

import pandas as pd
from pathlib import Path

def get_value_type(t):
    if t == 'object':
        return 'String'
    elif t == 'category':
        return 'Categorical'
    elif t == 'float64':
        return 'Float'
    elif t == 'int64':
        return'Int'
    elif t == 'bool' or t == 'uint8':
        return'Boolean'
    elif t == 'datetime64' or t == 'timedelta':
        return'DateTime'





def generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids, CURRENT_DSET, DIFFERENCE):
    global index_for_row_name, index_for_col_name, index_for_data_name
    used_ids.append(dset_name)
    index_col = 0
    output_path = Path(path)
    output_path_parent = output_path.parent
    if not output_path_parent.exists():
        output_path_parent.mkdir(parents=True)

    f = open(path, 'w')
    f.write("!create %s:Dataset\n" % dset_name)
    f.write("!%s.null_values:=Set{'nan'}\n"% dset_name)
    used_rows = []
    for col in dset.columns:
        col_name=col.replace(" ","").replace("[","").replace("]","").replace("-","")
        i = index_for_col_name
        while col_name in used_ids:
            col_name = col.replace(" ","").replace("[","").replace("]","").replace("-","") + str(i)
            i+=1
        index_for_col_name = i
        f.write ('!create %s:Column\n' % col_name)
        used_ids.append(col_name)
        f.write ("!%s.uri:=%s\n" % (col_name,index_col))
        f.write ("!%s.name:='%s'\n" % (col_name,col))
        value_type = get_value_type(dset.dtypes[col].name)
        f.write ("!%s.type:=ValueType::%s\n" % (col_name,value_type))
        target_column = str(col in target_columns).lower()
        f.write ("!%s.target:=%s\n" % (col_name,target_column))
        id_column = str(col in id_columns).lower()
        f.write ("!%s.id:=%s\n" % (col_name,id_column))
        f.write("!insert (%s,%s) into DSCol\n" % (dset_name, col_name))
        index_row = 0
        for item in dset[col]:
            data = col_name.replace(" ","").replace("[","").replace("]","").replace("-","") + '_data'
            i = index_for_data_name
            data_obj = data
            while data_obj in used_ids:
                data_obj = data + str(i)
                i+=1
            index_for_data_name = i
            data = data_obj
            f.write ('!create %s:Data\n' % data)
            used_ids.append(data)
            f.write ("!%s.value:='%s'\n" % (data,item))
            f.write ("!insert (%s,%s) into DSData\n" % (dset_name,data))
            f.write ("!insert (%s,%s) into DataCol\n" % (data, col_name))
            row_name = 'row' + str(index_row)

            if dset_name != CURRENT_DSET:
                i = index_for_row_name
                while row_name in used_ids:
                    i+=1
                    row_name = 'row' + str(i)
                index_for_row_name = i
                DIFFERENCE = i - index_row
                CURRENT_DSET = dset_name
            else:
                row_name = 'row' + str(index_row +  DIFFERENCE)
            if row_name not in used_rows:
                used_rows.append(row_name)
                f.write("!create %s:Row\n" % row_name)
                f.write("!%s.uri:=%s\n" % (row_name,index_row))
                f.write("!insert (%s,%s) into DSRow\n" %(dset_name,row_name))
            f.write("!insert (%s, %s) into DataRow\n" %(data, row_name))
            index_row+=1
        index_for_data_name = 0
        index_col+=1
    used_ids = used_rows + used_ids
    f.close()
    return (used_ids,CURRENT_DSET,DIFFERENCE)




def reset_vector():
    return []


def main():
    # colFilter_input = pd.read_csv('../intermediate_datasets/0_credit_dataset.csv')
    #
    # dset_name = 'col_filter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # id_columns = ['Column0']
    # dset = colFilter_input
    # used_ids = reset_vector()
    # path = '../models/1_col_filter/col_filter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colFilter_output = pd.read_csv('../intermediate_datasets/1_credit_output_dataset_colFilter_node.csv')
    #
    # dset_name = 'col_filter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colFilter_output
    # path = '../models/1_col_filter/col_filter_output.soil'
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    # id_columns = reset_vector()

    global index_for_row_name, index_for_col_name, index_for_data_name

    index_for_row_name, index_for_col_name, index_for_data_name = (0, 0, 0)

    string_to_number_input = pd.read_csv('../validation_pipeline/intermediate_datasets/1_credit_output_dataset_colFilter_node.csv')
    dset_name = 'string_to_number_input'
    target_columns = ['SeriousDlqin2yrs']
    dset = string_to_number_input
    used_ids = reset_vector()
    path = '../validation_pipeline/models/2_string_to_number_15000/string_to_number_input.soil'
    DIFFERENCE = 0
    CURRENT_DSET = ''

    used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, [], used_ids,DIFFERENCE, CURRENT_DSET)

    string_to_number_output = pd.read_csv('../validation_pipeline/intermediate_datasets/2_credit_output_dataset_stringToNumber_missingVal.csv')
    dset_name = 'string_to_number_output'
    target_columns = ['SeriousDlqin2yrs']
    dset = string_to_number_output
    path = '../validation_pipeline/models/2_string_to_number_15000/string_to_number_output.soil'

    used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, [], used_ids,DIFFERENCE, CURRENT_DSET)

    # string_to_number_input = pd.read_csv('../intermediate_datasets/1_credit_output_dataset_colFilter_node.csv')
    # dset_name = 'string_to_number_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = string_to_number_input
    # used_ids = reset_vector()
    # path = '../models/2_string_to_number/string_to_number_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # string_to_number_output = pd.read_csv('../intermediate_datasets/2_credit_output_dataset_stringToNumber_missingVal.csv')
    # dset_name = 'string_to_number_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = string_to_number_output
    # path = '../models/2_string_to_number/string_to_number_output.soil'
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)


    # missingVal_input = pd.read_csv('../intermediate_datasets/2_credit_output_dataset_stringToNumber_missingVal.csv')
    # dset_name = 'missingVal_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_input
    # used_ids = reset_vector()
    # path = '../models/3_missingVal/missingVal_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # missingVal_output = pd.read_csv('../intermediate_datasets/3_credit_output_dataset_missingVal_discretize.csv')
    # dset_name = 'missingVal_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_output
    # path = '../models/3_missingVal/missingVal_output.soil'
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # discretize_input = pd.read_csv('../intermediate_datasets/3_credit_output_dataset_missingVal_discretize.csv')
    # dset_name = 'discretize_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = discretize_input
    # used_ids = reset_vector()
    # path = '../models/4_discretize/discretize_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # discretize_output = pd.read_csv('../intermediate_datasets/4_credit_output_dataset_discretize_ruleFilter.csv')
    # dset_name = 'discretize_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = discretize_output
    # path = '../models/4_discretize/discretize_output.soil'
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # ruleFilter_input = pd.read_csv('../intermediate_datasets/4_credit_output_dataset_discretize_ruleFilter.csv')
    # dset_name = 'ruleFilter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleFilter_input
    # used_ids = reset_vector()
    # path = '../models/5_ruleFilter/ruleFilter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleFilter_output = pd.read_csv('../intermediate_datasets/5_credit_output_dataset_ruleFilter_colFilter.csv')
    # dset_name = 'ruleFilter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleFilter_output
    # path = '../models/5_ruleFilter/ruleFilter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # colFilter_input = pd.read_csv('../intermediate_datasets/5_credit_output_dataset_ruleFilter_colFilter.csv')
    # dset_name = 'colFilter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colFilter_input
    # used_ids = reset_vector()
    # path = '../models/6_colFilter/colFilter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colFilter_output = pd.read_csv('../intermediate_datasets/6_credit_output_dataset_colFilter_nextNode.csv')
    # dset_name = 'colFilter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colFilter_output
    # path = '../models/6_colFilter/colFilter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # rowFilter_input = pd.read_csv('../intermediate_datasets/6_credit_output_dataset_colFilter_nextNode.csv')
    # dset_name = 'rowFilter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowFilter_input
    # used_ids = reset_vector()
    # path = '../models/7a_rowFilter/rowFilter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowFilter_output = pd.read_csv('../intermediate_datasets/7.a_credit_output_dataset_rowFilter_constantVal.csv')
    # dset_name = 'rowFilter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowFilter_output
    # path = '../models/7a_rowFilter/rowFilter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # rowFilter_input = pd.read_csv('../intermediate_datasets/6_credit_output_dataset_colFilter_nextNode.csv')
    # dset_name = 'rowFilter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowFilter_input
    # used_ids = reset_vector()
    # path = '../models/7b_rowFilter/rowFilter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowFilter_output = pd.read_csv('../intermediate_datasets/7.b_credit_output_dataset_rowFilter_rowSplitter.csv')
    # dset_name = 'rowFilter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowFilter_output
    # path = '../models/7b_rowFilter/rowFilter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # constantVal_input = pd.read_csv('../intermediate_datasets/7.a_credit_output_dataset_rowFilter_constantVal.csv')
    # dset_name = 'constantVal_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = constantVal_input
    # used_ids = reset_vector()
    # path = '../models/8a_constantVal/constantVal_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # constantVal_output = pd.read_csv('../intermediate_datasets/8.a_credit_output_dataset_constantVal_concatenate.csv')
    # dset_name = 'constantVal_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = constantVal_output
    # path = '../models/8a_constantVal/constantVal_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # rowSplitter_input = pd.read_csv('../intermediate_datasets/7.b_credit_output_dataset_rowFilter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/8b_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/8.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/8b_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/8.b.b_credit_output_dataset_rowSplitter_rowSplitter.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/8b_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # mathFormula_input = pd.read_csv('../intermediate_datasets/8.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'mathFormula_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_input
    # used_ids = reset_vector()
    # path = '../models/9ba_mathFormula/mathFormula_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # mathFormula_output = pd.read_csv('../intermediate_datasets/9.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'mathFormula_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_output
    # path = '../models/9ba_mathFormula/mathFormula_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # rowSplitter_input = pd.read_csv('../intermediate_datasets/8.b.b_credit_output_dataset_rowSplitter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/9bb_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/9.b.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/9bb_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/9.b.b.b_credit_output_dataset_rowSplitter_rowSplitter.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/9bb_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # mathFormula_input = pd.read_csv('../intermediate_datasets/9.b.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'mathFormula_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_input
    # used_ids = reset_vector()
    # path = '../models/10bba_mathFormula/mathFormula_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # mathFormula_output = pd.read_csv('../intermediate_datasets/10.b.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'mathFormula_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_output
    # path = '../models/10bba_mathFormula/mathFormula_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)


    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/9.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/10ba_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/10.b.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/10ba_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/10.b.a_credit_output_dataset_concatenate_concatenate.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/10ba_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # rowSplitter_input = pd.read_csv('../intermediate_datasets/9.b.b.b_credit_output_dataset_rowSplitter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/10bbb_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/10.b.b.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/10bbb_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/10.b.b.b.b_credit_output_dataset_rowSplitter_rowSplitter.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/10bbb_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # mathFormula_input = pd.read_csv('../intermediate_datasets/10.b.b.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'mathFormula_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_input
    # used_ids = reset_vector()
    # path = '../models/11bbba_mathFormula/mathFormula_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # mathFormula_output = pd.read_csv('../intermediate_datasets/11.b.b.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'mathFormula_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_output
    # path = '../models/11bbba_mathFormula/mathFormula_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/10.b.a_credit_output_dataset_concatenate_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/11ba_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/11.b.b.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/11ba_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/11.b.a_credit_output_dataset_concatenate_concatenate.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/11ba_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #

    # rowSplitter_input = pd.read_csv('../intermediate_datasets/10.b.b.b.b_credit_output_dataset_rowSplitter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/11bbbb_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/11.b.b.b.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/11bbbb_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/11.b.b.b.b.b_credit_output_dataset_rowSplitter_none.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/11bbbb_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # mathFormula_input = pd.read_csv('../intermediate_datasets/11.b.b.b.b.a_credit_output_dataset_rowSplitter_mathFormula.csv')
    # dset_name = 'mathFormula_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_input
    # used_ids = reset_vector()
    # path = '../models/11bbbba_mathFormula/mathFormula_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # mathFormula_output = pd.read_csv('../intermediate_datasets/12.b.b.b.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'mathFormula_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = mathFormula_output
    # path = '../models/11bbbba_mathFormula/mathFormula_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/11.b.a_credit_output_dataset_concatenate_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/12ba_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/12.b.b.b.b.a_credit_output_dataset_mathFormula_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/12ba_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/12.b_credit_output_dataset_concatenate_constantVal.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/12ba_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # constantVal_input = pd.read_csv('../intermediate_datasets/12.b_credit_output_dataset_concatenate_constantVal.csv')
    # dset_name = 'constantVal_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = constantVal_input
    # used_ids = reset_vector()
    # path = '../models/13b_constantVal/constantVal_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # constantVal_output = pd.read_csv('../intermediate_datasets/13.b_credit_output_dataset_constantVal_concatenate.csv')
    # dset_name = 'constantVal_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = constantVal_output
    # path = '../models/13b_constantVal/constantVal_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/8.a_credit_output_dataset_constantVal_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/14_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/13.b_credit_output_dataset_constantVal_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/14_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/14_credit_output_dataset_concatente_nextNode.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/14_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)



    # discretize_input = pd.read_csv('../validation_pipeline/intermediate_datasets/14_credit_output_dataset_concatente_nextNode.csv')
    # dset_name = 'discretize_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = discretize_input
    # used_ids = reset_vector()
    # path = '../validation_pipeline/models/15_discretize/discretize_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # discretize_output = pd.read_csv('../validation_pipeline/intermediate_datasets/15_credit_output_dataset_discretize_ruleFilter.csv')
    # dset_name = 'discretize_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = discretize_output
    # path = '../validation_pipeline/models/15_discretize/discretize_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # ruleFilter_input = pd.read_csv('../intermediate_datasets/15_credit_output_dataset_discretize_ruleFilter.csv')
    # dset_name = 'ruleFilter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleFilter_input
    # used_ids = reset_vector()
    # path = '../models/16_ruleFilter/ruleFilter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleFilter_output = pd.read_csv('../intermediate_datasets/16_credit_output_dataset_ruleFilter_colFilter.csv')
    # dset_name = 'ruleFilter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleFilter_output
    # path = '../models/16_ruleFilter/ruleFilter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # colFilter_input = pd.read_csv('../intermediate_datasets/16_credit_output_dataset_ruleFilter_colFilter.csv')
    # dset_name = 'colFilter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colFilter_input
    # used_ids = reset_vector()
    # path = '../models/17_colFilter/colFilter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colFilter_output = pd.read_csv('../intermediate_datasets/17_credit_output_dataset_colFilter_nextNode.csv')
    # dset_name = 'colFilter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colFilter_output
    # path = '../models/17_colFilter/colFilter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # ruleEngine_input = pd.read_csv('../intermediate_datasets/17_credit_output_dataset_colFilter_nextNode.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/18_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/18_credit_output_dataset_ruleEngine_nextNode.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/18_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # string_to_number_input = pd.read_csv('../intermediate_datasets/18_credit_output_dataset_ruleEngine_nextNode.csv')
    # dset_name = 'string_to_number_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = string_to_number_input
    # used_ids = reset_vector()
    # path = '../models/19_string_to_number/string_to_number_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # string_to_number_output = pd.read_csv('../intermediate_datasets/19_credit_output_dataset_stringToNumber_ruleEngine.csv')
    # dset_name = 'string_to_number_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = string_to_number_output
    # path = '../models/19_string_to_number/string_to_number_output.soil'
    #
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # ruleEngine_input = pd.read_csv('../intermediate_datasets/19_credit_output_dataset_stringToNumber_ruleEngine.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/20_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/20_credit_output_dataset_ruleEngine_nextNode.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/20_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # sorter_input = pd.read_csv('../intermediate_datasets/20_credit_output_dataset_ruleEngine_nextNode.csv')
    # dset_name = 'sorter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = sorter_input
    # used_ids = reset_vector()
    # path = '../models/21_sorter/sorter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # sorter_output = pd.read_csv('../intermediate_datasets/21_credit_output_dataset_sorter_rowSplitter.csv')
    # dset_name = 'sorter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = sorter_output
    # path = '../models/21_sorter/sorter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # rowSplitter_input = pd.read_csv('../intermediate_datasets/21_credit_output_dataset_sorter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/22_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/22a_credit_output_dataset_rowSplitter_concatenate.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/22_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/22b_credit_output_dataset_rowSplitter_ruleEngine.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/22_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # ruleEngine_input = pd.read_csv('../intermediate_datasets/22b_credit_output_dataset_rowSplitter_ruleEngine.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/23b_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/23b_credit_output_dataset_ruleEngine_stringManipulation.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/23b_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)


    # ruleEngine_input = pd.read_csv('../intermediate_datasets/23b_credit_output_dataset_ruleEngine_stringManipulation.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/24b_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/24b_credit_output_dataset_stringManipulation_missingVal.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/24b_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # missingVal_input = pd.read_csv('../intermediate_datasets/24b_credit_output_dataset_stringManipulation_missingVal.csv')
    # dset_name = 'missingVal_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_input
    # used_ids = reset_vector()
    # path = '../models/25b_missingVal/missingVal_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # missingVal_output = pd.read_csv('../intermediate_datasets/25b_credit_output_dataset_missingVal_concatenate.csv')
    # dset_name = 'missingVal_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_output
    # path = '../models/25b_missingVal/missingVal_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/22a_credit_output_dataset_rowSplitter_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/26_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/25b_credit_output_dataset_missingVal_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/26_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/26_credit_output_dataset_concatenate_colRename.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/26_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # colRename_input = pd.read_csv('../intermediate_datasets/26_credit_output_dataset_concatenate_colRename.csv')
    # dset_name = 'colRename_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colRename_input
    # used_ids = reset_vector()
    # path = '../models/27_colRename/colRename_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colRename_output = pd.read_csv('../intermediate_datasets/27_credit_output_dataset_colRename_stringToNumber.csv')
    # dset_name = 'colRename_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colRename_output
    # path = '../models/27_colRename/colRename_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # stringToNumber_input = pd.read_csv('../intermediate_datasets/27_credit_output_dataset_colRename_stringToNumber.csv')
    # dset_name = 'stringToNumber_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_input
    # used_ids = reset_vector()
    # path = '../models/28_stringToNumber/stringToNumber_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # stringToNumber_output = pd.read_csv('../intermediate_datasets/28_credit_output_dataset_stringToNumber_nextNode.csv')
    # dset_name = 'stringToNumber_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_output
    # path = '../models/28_stringToNumber/stringToNumber_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # sorter_input = pd.read_csv('../intermediate_datasets/28_credit_output_dataset_stringToNumber_nextNode.csv')
    # dset_name = 'sorter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = sorter_input
    # used_ids = reset_vector()
    # path = '../models/29_sorter/sorter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # sorter_output = pd.read_csv('../intermediate_datasets/29_credit_output_dataset_sorter_rowSplitter.csv')
    # dset_name = 'sorter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = sorter_output
    # path = '../models/29_sorter/sorter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_input = pd.read_csv('../intermediate_datasets/29_credit_output_dataset_sorter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/30_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/30a_credit_output_dataset_rowSplitter_concatenate.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/30_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/30b_credit_output_dataset_rowSplitter_ruleEngine.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/30_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_input = pd.read_csv('../intermediate_datasets/30b_credit_output_dataset_rowSplitter_ruleEngine.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/31b_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/31b_credit_output_dataset_ruleEngine_stringToManipulation.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/31b_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    #
    # ruleEngine_input = pd.read_csv('../intermediate_datasets/31b_credit_output_dataset_ruleEngine_stringToManipulation.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/32b_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/32b_credit_output_dataset_stringToManipulation_missingVal.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/32b_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # missingVal_input = pd.read_csv('../intermediate_datasets/32b_credit_output_dataset_stringToManipulation_missingVal.csv')
    # dset_name = 'missingVal_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_input
    # used_ids = reset_vector()
    # path = '../models/33b_missingVal/missingVal_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # missingVal_output = pd.read_csv('../intermediate_datasets/33b_credit_output_dataset_missingVal_concatenate.csv')
    # dset_name = 'missingVal_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_output
    # path = '../models/33b_missingVal/missingVal_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/30a_credit_output_dataset_rowSplitter_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/34_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/33b_credit_output_dataset_missingVal_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/34_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/34_credit_output_dataset_concatenate_colRename.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/34_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colRename_input = pd.read_csv('../intermediate_datasets/34_credit_output_dataset_concatenate_colRename.csv')
    # dset_name = 'colRename_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colRename_input
    # used_ids = reset_vector()
    # path = '../models/35_colRename/colRename_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colRename_output = pd.read_csv('../intermediate_datasets/35_credit_output_dataset_colRename_stringToNumber.csv')
    # dset_name = 'colRename_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colRename_output
    # path = '../models/35_colRename/colRename_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # stringToNumber_input = pd.read_csv('../intermediate_datasets/35_credit_output_dataset_colRename_stringToNumber.csv')
    # dset_name = 'stringToNumber_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_input
    # used_ids = reset_vector()
    # path = '../models/36_stringToNumber/stringToNumber_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # stringToNumber_output = pd.read_csv('../intermediate_datasets/36_credit_output_dataset_stringToNumber_nextNode.csv')
    # dset_name = 'stringToNumber_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_output
    # path = '../models/36_stringToNumber/stringToNumber_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    #
    # sorter_input = pd.read_csv('../intermediate_datasets/36_credit_output_dataset_stringToNumber_nextNode.csv')
    # dset_name = 'sorter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = sorter_input
    # used_ids = reset_vector()
    # path = '../models/37_sorter/sorter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # sorter_output = pd.read_csv('../intermediate_datasets/37_credit_output_dataset_sorter_rowSplitter.csv')
    # dset_name = 'sorter_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = sorter_output
    # path = '../models/37_sorter/sorter_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_input = pd.read_csv('../intermediate_datasets/37_credit_output_dataset_sorter_rowSplitter.csv')
    # dset_name = 'rowSplitter_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_input
    # used_ids = reset_vector()
    # path = '../models/38_rowSplitter/rowSplitter_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_1 = pd.read_csv('../intermediate_datasets/38a_credit_output_dataset_rowSplitter_concatenate.csv')
    # dset_name = 'rowSplitter_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_1
    # path = '../models/38_rowSplitter/rowSplitter_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # rowSplitter_output_2 = pd.read_csv('../intermediate_datasets/38b_credit_output_dataset_concatenate_ruleEngine.csv')
    # dset_name = 'rowSplitter_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = rowSplitter_output_2
    # path = '../models/38_rowSplitter/rowSplitter_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_input = pd.read_csv('../intermediate_datasets/38b_credit_output_dataset_concatenate_ruleEngine.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/39b_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/39b_credit_output_dataset_ruleEngine_stringManipulation.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/39b_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    #
    # ruleEngine_input = pd.read_csv('../intermediate_datasets/39b_credit_output_dataset_ruleEngine_stringManipulation.csv')
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../models/40b_ruleEngine/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../intermediate_datasets/40b_credit_output_dataset_stringManipulation_missingValue.csv')
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../models/40b_ruleEngine/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # missingVal_input = pd.read_csv('../intermediate_datasets/40b_credit_output_dataset_stringManipulation_missingValue.csv')
    # dset_name = 'missingVal_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_input
    # used_ids = reset_vector()
    # path = '../models/41b_missingVal/missingVal_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # missingVal_output = pd.read_csv('../intermediate_datasets/41b_credit_output_dataset_missingValue_concatenate.csv')
    # dset_name = 'missingVal_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = missingVal_output
    # path = '../models/41b_missingVal/missingVal_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_1 = pd.read_csv('../intermediate_datasets/38a_credit_output_dataset_rowSplitter_concatenate.csv')
    # dset_name = 'concatenate_input_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_1
    # used_ids = reset_vector()
    # path = '../models/42_concatenate/concatenate_input_1.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_input_2 = pd.read_csv('../intermediate_datasets/41b_credit_output_dataset_missingValue_concatenate.csv')
    # dset_name = 'concatenate_input_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_input_2
    # path = '../models/42_concatenate/concatenate_input_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # concatenate_output = pd.read_csv('../intermediate_datasets/42_credit_output_dataset_concatenate_colRename.csv')
    # dset_name = 'concatenate_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = concatenate_output
    # path = '../models/42_concatenate/concatenate_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colRename_input = pd.read_csv('../intermediate_datasets/42_credit_output_dataset_concatenate_colRename.csv')
    # dset_name = 'colRename_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colRename_input
    # used_ids = reset_vector()
    # path = '../models/43_colRename/colRename_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # colRename_output = pd.read_csv('../intermediate_datasets/43_credit_output_dataset_colRename_stringToNumber.csv')
    # dset_name = 'colRename_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = colRename_output
    # path = '../models/43_colRename/colRename_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # stringToNumber_input = pd.read_csv('../intermediate_datasets/43_credit_output_dataset_colRename_stringToNumber.csv')
    # dset_name = 'stringToNumber_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_input
    # used_ids = reset_vector()
    # path = '../models/44_stringToNumber/stringToNumber_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # stringToNumber_output = pd.read_csv('../intermediate_datasets/44_credit_output_dataset_stringToNumber_nextNode.csv')
    # dset_name = 'stringToNumber_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_output
    # path = '../models/44_stringToNumber/stringToNumber_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # stringToNumber_input = pd.read_csv('../intermediate_datasets/44_credit_output_dataset_stringToNumber_nextNode.csv')
    # dset_name = 'stringToNumber_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_input
    # used_ids = reset_vector()
    # path = '../models/45_stringToNumber/stringToNumber_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # stringToNumber_output = pd.read_csv('../intermediate_datasets/45_credit_output_dataset_stringToNumber_numberToString.csv')
    # dset_name = 'stringToNumber_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = stringToNumber_output
    # path = '../models/45_stringToNumber/stringToNumber_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # numberToString_input = pd.read_csv('../intermediate_datasets/45_credit_output_dataset_stringToNumber_numberToString.csv')
    # dset_name = 'numberToString_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = numberToString_input
    # used_ids = reset_vector()
    # path = '../models/46_numberToString/numberToString_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # numberToString_output = pd.read_csv('../intermediate_datasets/46_credit_output_dataset_numberToString_nextNode.csv')
    # dset_name = 'numberToString_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = numberToString_output
    # path = '../models/46_numberToString/numberToString_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # split_input = pd.read_csv('../intermediate_datasets/46_credit_output_dataset_numberToString_nextNode.csv')
    # dset_name = 'split_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = split_input
    # used_ids = reset_vector()
    # path = '../models/47_split/split_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # split_output_1 = pd.read_csv('../intermediate_datasets/47a_credit_output_dataset_partitioning_smote.csv')
    # dset_name = 'split_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = split_output_1
    # path = '../models/47_split/split_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # split_output_2 = pd.read_csv('../intermediate_datasets/47b_credit_output_dataset_partitioning_smote.csv')
    # dset_name = 'split_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = split_output_2
    # path = '../models/47_split/split_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # smote_input = pd.read_csv('../intermediate_datasets/47a_credit_output_dataset_partitioning_smote.csv')
    # dset_name = 'smote_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = smote_input
    # used_ids = reset_vector()
    # path = '../models/48_smote/smote_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # smote_output = pd.read_csv('../intermediate_datasets/48a_credit_output_dataset_smote.csv')
    # dset_name = 'smote_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = smote_output
    # path = '../models/48_smote/smote_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

    # Corrected operation

    # ruleEngine_input = pd.read_csv('../validation_pipeline/intermediate_datasets/38b_credit_output_dataset_'
    #                                'concatenate_ruleEngine.csv', nrows=10)
    # dset_name = 'ruleEngine_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_input
    # used_ids = reset_vector()
    # path = '../validation_pipeline/models/39b_ruleEngine_corrected/ruleEngine_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # ruleEngine_output = pd.read_csv('../validation_pipeline/intermediate_datasets/corrected_39b_credit_output_dataset_'
    #                                 'ruleEngine_stringManipulation.csv',nrows=10)
    # dset_name = 'ruleEngine_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = ruleEngine_output
    # path = '../validation_pipeline/models/39b_ruleEngine_corrected/ruleEngine_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns, id_columns, used_ids,DIFFERENCE, CURRENT_DSET)


    ##Ilustrative Example:

    # remove_col_input = pd.read_csv('../illustrative_example/datasets/1_edrop_to_remove_col.csv')
    # dset_name = 'remove_col_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = remove_col_input
    # used_ids = reset_vector()
    # path = '../illustrative_example/1_edrop_remove_col_to_imb_learn/remove_col_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # remove_col_output = pd.read_csv('../illustrative_example/datasets/2_edrop_remove_col_to_imb_learn.csv')
    # dset_name = 'remove_col_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = remove_col_output
    # path = '../illustrative_example/1_edrop_remove_col_to_imb_learn/remove_col_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # imb_learn_input = pd.read_csv('../illustrative_example/datasets/2_edrop_remove_col_to_imb_learn.csv')
    # dset_name = 'imb_learn_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = imb_learn_input
    # used_ids = reset_vector()
    # path = '../illustrative_example/2_edrop_imb_learn_to_one_hot/imb_learn_input'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # imb_learn_output = pd.read_csv('../illustrative_example/datasets/3_edrop_imb_learn_to_one_hot.csv')
    # dset_name = 'imb_learn_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = imb_learn_output
    # path = '../illustrative_example/2_edrop_imb_learn_to_one_hot/imb_learn_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # one_hot_input = pd.read_csv('../illustrative_example/datasets/3_edrop_imb_learn_to_one_hot.csv')
    # dset_name = 'one_hot_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = one_hot_input
    # used_ids = reset_vector()
    # path = '../illustrative_example/3_edrop_one_hot_to_split/one_hot_input'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # one_hot_output = pd.read_csv('../illustrative_example/datasets/4_edrop_one_hot_to_split.csv')
    # dset_name = 'one_hot_output'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = one_hot_output
    # path = '../illustrative_example/3_edrop_one_hot_to_split/one_hot_output.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # split_input = pd.read_csv('../illustrative_example/datasets/4_edrop_one_hot_to_split.csv')
    # dset_name = 'split_input'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = split_input
    # used_ids = reset_vector()
    # path = '../illustrative_example/4_edrop_split/split_input.soil'
    # DIFFERENCE = 0
    # CURRENT_DSET = ''
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # split_output_1 = pd.read_csv('../illustrative_example/datasets/4.1_edrop_split.csv')
    # dset_name = 'split_output_1'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = split_output_1
    # path = '../illustrative_example/4_edrop_split/split_output_1.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)
    #
    # split_output_2 = pd.read_csv('../illustrative_example/datasets/4.2_edrop_split.csv')
    # dset_name = 'split_output_2'
    # target_columns = ['SeriousDlqin2yrs']
    # dset = split_output_2
    # path = '../illustrative_example/4_edrop_split/split_output_2.soil'
    # used_ids,DIFFERENCE,CURRENT_DSET = generate_file_with_cols_and_data(path, dset, dset_name, target_columns,
    #                                                                     id_columns, used_ids,DIFFERENCE, CURRENT_DSET)

if __name__ == "__main__":
    main()



