import random

import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup


def parse_data_to_model(f, path_csv, id_dfield, name_dfield, used_ids,
                        output_path, sep=','):
    output_path = Path(output_path)
    output_path_parent = output_path.parent
    if not output_path_parent.exists():
        output_path_parent.mkdir(parents=True)

    dataframe = pd.read_csv(path_csv, sep=sep)
    j = 0
    for d in dataframe[name_dfield]:
        i = 0
        id_data = 'data_' + str(d) + '_' + str(i)
        while id_data in used_ids:
            i += 1
            id_data = 'data_' + str(d) + '_' + str(random.randint(0, len(dataframe[name_dfield])))
            id_data = id_data.replace(" ", "").replace("[", "").replace("]", "").replace("-", "").replace('.', "_")
        used_ids.append(id_data)
        f.write('!create ' + id_data + ':Data\n ')
        f.write('!' + id_data + '.value:=' + "'" + str(d) + "'" + '\n')
        f.write('!' + id_data + '.index:=' + str(j) + '\n')
        f.write('!insert(' + id_dfield + ',' + id_data + ') into DataOfDataField\n ')
        j += 1


def parse_to_model(path_xml, path_csv, name, target_columns, id_columns,
                   used_ids, output_path, sep=','):
    output_path = Path(output_path)
    output_path_parent = output_path.parent
    if not output_path_parent.exists():
        output_path_parent.mkdir(parents=True)

    f = open(output_path, 'w')
    f.write('!create ' + name + ':DataDictionary\n ')
    dataframe = pd.read_csv(path_csv, sep=sep)
    f.write('!' + name + '.rows:=' + str(dataframe.shape[0]) + '\n')
    f.write('!' + name + ".name:='" + name + "'" + '\n')
    with open(path_xml, 'r') as f_xml:
        ddict = f_xml.read()
    bs_ddict = BeautifulSoup(ddict, 'xml')
    op_types = ['categorical', 'continuous']
    dfields = bs_ddict.find_all('DataField')
    for dfield in dfields:
        name_dfield = dfield.get('name')
        i = 0
        id_dfield = name_dfield + '_' + str(i)
        while id_dfield in used_ids:
            i += 1
            id_dfield = name_dfield + '_' + str(i)
        id_dfield = id_dfield.replace(" ", "").replace("[", "").replace("]", "").replace("-", "").replace('.', "_")
        used_ids.append(id_dfield)
        if dfield.get('optype') == op_types[1]:
            f.write('!create ' + id_dfield + ':Continuous\n ')
            f.write('!insert(' + name + ',' + id_dfield + ') into DataDictDataField\n ')
            for interval in dfield.find_all('Interval'):
                leftMargin = interval.get('leftMargin')
                rightMargin = interval.get('rightMargin')
                closure = interval.get('closure')
                i = 0
                int_name = 'interval_' + name_dfield + '_' + str(i)
                while (int_name in used_ids):
                    i += 1
                    int_name = 'interval_' + name_dfield + '_' + str(i)
                used_ids.append(int_name)
                f.write('!create ' + int_name + ':Interval' + '\n')
                f.write('!' + int_name + '.leftMargin:=' + leftMargin + '\n')
                f.write('!' + int_name + '.rightMargin:=' + rightMargin + '\n')
                f.write('!' + int_name + '.closure:=' + 'ClosureType::' + closure + '\n')
                count = -1
                leftMargin = float(leftMargin)
                rightMargin = float(rightMargin)
                if closure == 'closedClosed':
                    count = dataframe[(dataframe[name_dfield] >= leftMargin) &
                                      (dataframe[name_dfield] <= rightMargin)].shape[0]
                elif closure == 'closedOpen':
                    count = dataframe[(dataframe[name_dfield] >= leftMargin) &
                                      (dataframe[name_dfield] < rightMargin)].shape[0]
                elif closure == 'openOpen':
                    count = dataframe[(dataframe[name_dfield] > leftMargin) &
                                      (dataframe[name_dfield] < rightMargin)].shape[0]
                elif closure == 'openClosed':
                    count = dataframe[(dataframe[name_dfield] > leftMargin) &
                                      (dataframe[name_dfield] <= rightMargin)].shape[0]

                f.write('!' + int_name + '.count:=' + str(count) + '\n')
                f.write('!insert(' + id_dfield + ',' + int_name + ') into ContinuousInterval\n ')
        else:
            f.write('!create ' + id_dfield + ':Categorical\n ')
            if (dfield.get('optype') == op_types[0]):
                f.write('!' + id_dfield + '.ordinal:=false\n ')
            else:
                f.write('!' + id_dfield + '.ordinal:=true\n ')
            f.write('!insert(' + name + ',' + id_dfield + ') into DataDictDataField\n ')
            for vField in dfield.find_all('Value'):
                i = 0
                id_vfield = 'value_' + vField.get('value') + '_' + str(i)
                while (id_vfield in used_ids):
                    i += 1
                    id_vfield = 'value_' + vField.get('value') + '_' + str(i)
                used_ids.append(id_vfield)
                f.write('!create ' + id_vfield + ':ValueField\n ')
                f.write('!' + id_vfield + ".value:= '" + vField.get('value') + "'" + '\n')
                count = dataframe[dataframe[name_dfield] == vField.get('value')].shape[0]
                f.write('!' + id_vfield + '.count:=' + str(count) + '\n')
                if vField.get('property') == 'missing':
                    f.write('!insert(' + id_dfield + ',' + id_vfield + ') into MissingVals\n ')
                elif vField.get('property') == 'invalid':
                    f.write('!insert(' + id_dfield + ',' + id_vfield + ') into InvalidVals\n ')
                else:
                    f.write('!insert(' + id_dfield + ',' + id_vfield + ') into ValidValues\n ')
        if name_dfield in target_columns:
            f.write('!' + id_dfield + '.target:=true\n ')
        else:
            f.write('!' + id_dfield + '.target:=false\n ')
        if name_dfield in id_columns:
            f.write('!' + id_dfield + '.id:=true\n ')
        else:
            f.write('!' + id_dfield + '.id:=false\n ')
        f.write('!' + id_dfield + '.dataType:=DataType::' + dfield.get('dataType') + '\n')
        f.write('!' + id_dfield + ".name:='" + name_dfield + "'" + '\n')
        if (dataframe[name_dfield].isna().sum() > 0):
            i = 0
            id_missing_val = 'nan' + '_' + str(i)
            while (id_missing_val in used_ids):
                i += 1
                id_missing_val = 'nan' + '_' + str(i)
            used_ids.append(id_missing_val)
            f.write('!create ' + id_missing_val + ':ValueField\n ')
            f.write('!' + id_missing_val + ".value:= '" + 'nan' + "'" + '\n')
            f.write('!' + id_missing_val + '.count:=' + str(dataframe[name_dfield].isna().sum()) + '\n')
            f.write('!insert(' + id_dfield + ',' + id_missing_val + ') into MissingVals\n ')
    return f


def main():
    used_ids = []
    f = parse_to_model('example.pmml', 'example.csv', 'example', [], [], used_ids,
                       'example.soil')
    parse_data_to_model(f, 'example.csv', 'sex_0', 'sex', used_ids, 'example.soil')


if __name__ == "__main__":
    main()
