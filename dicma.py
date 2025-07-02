#!/usr/bin/env python3

# This project is from ArtesOscuras github repo.

#-----------------------------------------------------
# INTERNAL CONFIGURATION PARAMETERS FOR PASSWORD MODE:
# -----------------------
#
# Light mode parameters:
amount_of_sufixs_used_light_mode = 200
amount_of_prefixs_used_light_mode = 50

# Default mode parameters:
amount_of_sufixs_used = 1000
amount_of_prefixs_used = 200

# Extended mode parameters:
amount_of_numericpat_used = 516
amount_of_symbolpat_used = 100
#-----------------------------------------------------


# Libraris to import
import sys
import os
import argparse
from itertools import product
import re
from collections import Counter
import unicodedata
import urllib.request
import subprocess

# General variables
LIGHT_MODE = False
FULL_MODE = False
VERBOSE = True
OUTPUT_FILE_BULEAN = False
MASSIVE_MODE = False

# Machine learning variables
NEIGHBORS_AMMOUNT = 20

# internal stored patterns: (I took it from rockyou.txt)
BASIC_SUFIXS = ['1', '2', '123', '12', '3', '7', '13', '5', '4', '11', '!', '07', '23', '22', '01', '21', '8', '14', '10', '08', '6', '06', '9', '15', '16', '69', '18', '17', '24', '05', '.', '09', '88', '19', '25', '20', '03', '0', '04', '27', '89', '02', '99', '26', '101', '77', '1234', '28', '33', '00', '2007', '92', '87', '93', '2006', '*', '29', '94', '90', '2008', '91', '95', '86', '55', '30', '666', '143', '31', '96', '85', '44', '32', '007', '34', '4ever', '84', '45', '#1', '2005', '78', '98', '66', '83', '82', '97', '1994', '79', '100', '1992', '1993', '81', '4life', '4eva', '12345', '1995', '1991', '777', '1990', '420', '76', '56', '111', '1989', '2000', '1987', '321', '2009', '67', '80', '75', '2004', '1996', '42', '1988', '35', '74', '72', '1986', '1985', '001', '36', '73', '54', '2003', '456', '50', '!!', '333', '68', '@', '1984', '64', '37', '65', '40', '71', '2002', '4u', '123456', '43', '555', '911', '1997', '52', '?', '999', '1983', '1982', '47', '$', '57', '2001', '41', '@hotmail.com', '1980', '38', '4me', '1981', '63', '46', '70', '2010', '58', '48', '222', '51', '62', '1979', '121', '619', '53', '789', '59', '39', '112', '1998', '1978', '000', '888', '49', '**', '247', '234', '61', '60', '..', '213', '1977', '1212', '200', '159', '1999', '@yahoo.com', '1976', '182', '786', '1!', '.com', '<3', '1975', ')', '125', '187', '214', '2k7', '147', '...', '1974', '.1', '102', '1973', '!!!', '4e', '123456789', '411', '212', '6969', '1010', '305', '124', '012', '1972', '345', '360', '1969', '009', '316', '1970', '313', '4lyf', '711', '210', '808', '122', '1313', '987', '311', '120', '#', '1971', '444', '369', '1000', '008', '500', '2012', '323', '2011', '211', '1111', '246', '215', ',', '300', '135', '567', '117', '003', '103', '113', '1968', '1122', '225', '713', '132', '209', '510', '002', '520', '1221', '310', '223', '105', '~', '127', '100pre', '110', '1967', '818', '011', '1213', '1012', '202', '312', '128', '109', '+', '108', '126', '098', '1966', '2k6', '1965', '909', '1.', '118', '1020', '3000', '115', '678', '714', '415', '1964', '013', '1123', '107', '718', '129', ']', '831', '010', '2121', '4l', '005', '145', '314', '224', '104', '2525', '131', ';', '221', '626', '1314', '2020', '357', '4lyfe', '114', '318', '1210', '1223', '916', '1023', '1230', '106', '900', '216', '006', '116', '1011', '2323', '201', '2468', '4321', '119', '504', '3r', '1963', '1214', '217', '315', '2u', '512', '1224', '412', '0123', '1231', '1022', '1121', '1013', '1001', '258', '890', '134', '150', '220', '421', '1021', '1220', '1024', '1218', '1215', '317', '199', '521', '1216', '***', '303', '515', '004', '707', '$$', '206', '1014', '219', '1025', '1211', '1962', '218', '320', '1960', '1217', '413', '4444', '727', '1205', '1225', '`', '912', '812', '410', '0n', '813', '227', '2k', '014', '100%', '1206', '231', '1228', '505', '1029', '7777', '0000', '1017', '1015', '1107', '133', '1112', '325', '130', '513', '4LIFE', '324', '@1', '1016', '511', '1018', '423', '180', '1026', '021', '1125', '1031', '1028', "'", '1203', '1204', '1104', '023', '2k8', '612', '400', '721', '805', '1105', '2112', '1124', '1120', '4you', '525', '1207', '228', '205', '913', '2222', '2013', '#2', '1103', '1202', '1961', '1027', '617', '1106', '1019', '1127', '717', '1227', '156', '250', '4evr', '1208', '712', '600', '1219', '254', '1414', '017', '226', '408', '925', '723', '322', '1959', '137', '817', '319', '2424', '151', '809', '910', '232', '/', '203', '1229', '414', '326', '327', '616', '1515', '1226', '1030', '516', '1*', '1201', '2x', '365', '144', '1129', '123!', '623', '1209', '523', '611', '1126', '1005', '9999', '1128', '=', '1004', '!1', '1102', '710', '1002', '654', '1101', '613', '419', '1108', '422', '921', '198', '1130', '425', '123.', '923', '915', '169', '615', '015', '416', '#3', '951', '610', '141', '190', '816', '328', '1958', '811', '720', '016', '828', '426', '702', '919', '191', '1a', '522', '1007', '501', '018', '823', '189', '715', '8888', '918', '54321', '716', '256', '1003', '424', '1234567', '963', '138', '@123', '207', '427', '2345', '787', '5150', '852', '242', '914', '621', '331', '4EVER', '741', '637', '614', '.123', '562', '252', '920', '301', '1109', '1222', '153', '330', '1e', '417', '1006', '530', '800', '0506', '1957', '*1', '245', '1956', '517', '622', '155', '235', '753', '514', '329', ':)', '1113', '0101', '157', '821', '722', '810', '5678', '429', '2526', '724', '527', '024', '069', '524', '418', '0607', '208', '922', '624', '142', '168', '152', '2me', '0808', '1008', '929', '561', '2b', '700', '1717', '928', '815', '233', '518', '136', '177', '0708', '625', '0102', '725', '901', '022', '822', '917', '0909', '519', '334', '526', '248', '183', '731', '927', '531', '1117', '167', '602', '1114', '1818', '814', '5555', '529', '019', '620', '1n', '1616', '1955', '824', '618', '%', '1009', '192', '719', '503', '924', '1919', '229', '1st', '@aol.com', '926', "'s", '820', '430', '0707', '528', '188', '181', '4EVA', '989', '432', '1412', '204', '404', '1110', '0406', '304', '428', '5000', '0405', '825', '0809', '3s', '??', '628', '0204', '281', '2212', '3d', '0205', '197', '0202', '1115', '1954', '726', '728', '237', '0505', '757', '1116', '302', '140', '954', '559', '601', '747', '1516', '405', '730', '0305', '243', '146', '154', '509', '729', '627', '0306', '1415', '"', '350', '629', '1324', '696', '0507', '0711', '0214', '253', '269', '407', '0407', '0304', '306', '4U', '650', '2310', '171', '236', '2529', '630', '1905', '239', '2528', '450', '1s', '2527', '139', '025', '195', '&', '0303', '123*', '1118', '454', '0606', '2530', '0203', '876', '930', '178', "\\\\'", '2210', '0107', '0404', '027', '0408', '1907', '819', '0812', '409', '158', '908', '543', '401', '230', '0210', '1312', '0308', '307', '1love', '240', '0412', '1369', '1310', '1953', '826', '829', '2!', '165', '2105', '161', '606', '1234567890', '160', '148', '904', '0311', '830', '0307', '0103', '2211', '2014', '193', '.12', '0110', '308', '827', '1307', '0420', '0206', '1119', '0207', '@@', '0911', '0212', '149', '990', '0105', '2123', '.2', '255', '309', '(L)', '241', '3333', '801', '0912', '185', '1432', '0104', '6666', '0987', '175', '163', '502', '1950', '671', '0106', '0208', '765', '251', '337', '1908', '170', '445', '166', '028', '173', '257', '3y', '031', '2107', '1888', '2524', '123123', '196', '&me', '1402', '0608', '2311', '1331', '!@#', '1903', '1305', '0312', '1235', '1@', '956', '174', '2312', '0509', '275', '2523', '0508', '172', '0512', '1311', '1306', '1952', '1200', '90210', '1512', '1408', '1233', '026', '1411', '2727', '1920', '978', '184', '5683', '1690', '0810', '2510', '244', '0709', '565', '2410', '667', '238', '090', '0108', '164', '12345678', '55555', '4u2', '0411', '1912', '#7', '3n', '2412', '2205', '1812', '1904', '0811', '2103', '402', '0612', '0309', '973', '0907', '336', '14344', '1410', '123321', '1906', '1323', '289', '903', '\\\\', '0211', '0209', '1405', '2106', '2828', '0712', '803', '2580', '2626', '267', '0321', '1308', '1718', '>', '2207', '1304', '262', '4ev', '077', '179', '343', '2531', '2110', '3030', '1508', '1407', '12!', '2203', '162', '0x', '585', '0906', '176', '1821', '1606', '2303']
BASIC_PREFIXS = ['1', '2', '4', '123', '3', '*', '12', '7', '5', '8', '6', '13', '11', '143', '9', '19', '@', '(', '10', '14', '0', '22', '23', '21', '$', '!', '#1', '20', '15', '24', '18', '17', '16', '1234', '69', '.', '25', '01', '27', 'i', '07', '26', '**', '28', '06', '29', '08', '30', '~', '00', '05', '123456', '88', '99', '12345', '02', '03', '100', '04', '31', '09', '[', '666', '33', '77', '#', 'sk8', '50', 'ms.', 'mr.', '123456789', '1994', 'i<3', '100%', 'mz.', '<', '89', 'l0', '44', '1992', '1993', '420', '32', '1995', '55', '2007', '101', '34', '321', '1991', '007', '92', ',', 'm1', '2006', '87', '95', '1989', '"', '<3', '1996', '1990', '98', 'no1', '93', '1987', '777', 'm0', '94', 'c0', '90', '66', '2008', '45', ';', 'r0', '91', '96', 'il0', '86', '1988', 'my1', 'ih8', '78', '97', 'my', 'h0', '..', '+', '!!', '111', 'p0', 'l1', 'j0', '56', 'b1', 'm3', '85', '1986', '1985', '52', 'd3', '35', '42', 'k1', '/', 's3', '2005', '84', '40', '79', '`', '82', '619', '***', 's0', '54', 'p1', 'b3', '76', 'te', '36', '74', '67', 'a1', 'g0', 'hi5', '=', '83', 'd0', '1997', '911', '333', '1984', 'b0', '49', 's1', '456', 'd1', '68', '555', 'm@', '80', '72', '43', 'j.', '?', '$$', '...', 'j3', '789', 'h3', '999', '187', '37', '1983', '75', '57', 'n0', '41']
NUMERIC_PATTERNS = ['1', '2', '4', '3', '123', '7', '12', '5', '0', '8', '13', '6', '9', '11', '23', '22', '10', '14', '07', '21', '01', '15', '08', '06', '16', '18', '69', '17', '24', '05', '19', '09', '20', '25', '88', '03', '00', '27', '04', '02', '33', '89', '26', '99', '1234', '28', '77', '101', '92', '2007', '93', '87', '29', '94', '2006', '143', '90', '91', '30', '95', '2008', '55', '31', '100', '86', '666', '34', '44', '32', '96', '85', '45', '007', '84', '98', '1994', '78', '66', '2005', '1992', '1993', '83', '82', '12345', '97', '1991', '1995', '79', '1990', '81', '1989', '56', '777', '1987', '76', '420', '321', '111', '35', '67', '1996', '80', '2000', '1988', '42', '75', '123456', '50', '2009', '74', '2004', '1986', '72', '54', '36', '456', '1985', '73', '43', '1984', '64', '2003', '68', '37', '40', '333', '001', '52', '65', '47', '41', '71', '1997', '57', '1983', '555', '2002', '999', '1982', '911', '38', '1980', '2001', '46', '63', '70', '1981', '48', '51', '53', '58', '789', '62', '39', '2010', '59', '619', '49', '1979', '222', '121', '000', '1998', '112', '1978', '123456789', '60', '61', '888', '234', '159', '1212', '247', '200', '1977', '213', '786', '1999', '125', '182', '1976', '187', '1975', '147', '214', '1974', '1973', '102', '305', '1010', '6969', '124', '1972', '212', '360', '987', '1000', '411', '345', '1969', '012', '808', '313', '311', '210', '1313', '1970', '369', '500', '120', '300', '316', '711', '122', '1971', '009', '1111', '444', '323', '520', '135', '2012', '246', '211', '2011', '1122', '567', '215', '103', '008', '113', '1968', '117', '225', '510', '310', '209', '1221', '110', '132', '2468', '713', '105', '003', '127', '1213', '1967', '312', '002', '223', '1012', '109', '128', '011', '818', '1966', '108', '126', '098', '202', '118', '2525', '1020', '1123', '104', '831', '1965', '115', '357', '010', '2121', '107', '714', '1314', '145', '909', '415', '900', '129', '678', '314', '224', '1964', '318', '2020', '1210', '114', '131', '2323', '718', '3000', '504', '013', '106', '4321', '1223', '1230', '221', '626', '1023', '201', '116', '005', '1011', '150', '916', '216', '512', '119', '0123', '1214', '515', '006', '412', '1963', '1224', '315', '258', '0000', '134', '217', '220', '812', '1121', '199', '890', '1001', '1231', '1024', '521', '1021', '400', '1022', '1013', '4444', '303', '1215', '1220', '421', '250', '1234567', '1216', '206', '320', '1218', '317', '707', '325', '218', '1025', '1962', '7777', '413', '1211', '1014', '219', '410', '133', '1225', '130', '600', '1029', '1205', '1960', '813', '1217', '004', '1206', '1015', '231', '1228', '1112', '912', '227', '180', '1107', '505', '654', '727', '014', '1017', '324', '1120', '1204', '1031', '513', '2222', '1016', '423', '1028', '2112', '1026', '805', '205', '1203', '156', '1018', '963', '1105', '1125', '1414', '228', '511', '1124', '021', '408', '612', '1104', '525', '2424', '1208', '232', '254', '151', '1202', '1027', '809', '319', '1103', '144', '1207', '1515', '1106', '1127', '322', '721', '913', '203', '414', '226', '54321', '137', '023', '2013', '1005', '1019', '800', '1219', '1227', '910', '1961', '326', '717', '925', '617', '951', '1229', '723', '1030', '611', '1129', '1209', '700', '817', '1959', '1226', '327', '712', '365', '1004', '710', '616', '017', '9999', '1201', '1102', '5150', '1128', '852', '198', '425', '191', '1002', '523', '623', '426', '141', '350', '1101', '516', '256', '753', '1126', '422', '419', '8888', '741', '155', '1108', '1130', '169', '787', '190', '1234567890', '501', '252', '242', '613', '915', '610', '2014', '2015', '2016', '2017', '2018', '2019', '2021', '2021', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
SYMBOLIC_PATTERNS = ['.', '-', '!', '@', '*', '/', '#', '&', ',', '$', '+', '=', '?', '(', ')', '**', '!!', ';', '<', '..', "'", ']', '%', '"', '~', '...', '[', '`', '="', "\\\\'", ':', '!!!', '$$', '***', '^', '--', '@@', '//', '>', '++', '??', '!@', '\\\\', ':)', 'ื', '://', '!@#', '##', "\\\\\\\\\\\\'", '.,', '{', '\\\\\\\\', ',.', '}', '$$$', '><', ',,', '()', 'ั', '้', '/*', '^^', 'ุ', '@#', 'ึ', '+-', '&&', '???', '@@@', '*/', 'ิ', '|', ';;', 'ี', '****', '==', '@!', '....', '!*', '[]', ',./', '---', '=]', '/*-', '@$', '=)', '!!!!', '.-', '#!', '~~', ',]', '´', '!@#$', '-=', '*-', ')(', '+++', '))', '?!', '=-']


def print_banner():
    ascii_art = """                                                                      

                                 .-:                                  
                               -*%%%#+.                               
                             =#%%%%%%%%+.                             
                           .*%%%%%%%%%%%#-                            
                          :#%%%%%%%%%%%%%#=                           
                         :#*%%%#=:..=*%%%*#=                          
                         ##%%+:       .=#@#%:                         
                        =%%*.           .=%%#                         
                        #%=               :#%:                        
                       .@= .              .:%=                        
                        #.:-             :- *:                        
                       ...:%=           :%+ :.   -                    
                      :%+. +%+         -%#: -#: *:                    
                    ..::--:..=+:     .++:.:+=.:#= =                   
                   .-=+++++=-::::   .:.  .. .+#- =-                   
                  -+=-:...::-=+++=:.     .-*#+  *+ :                  
                    :-=++++=-:.  ... .:=#%*-  -#- -.                  
                 .=+=-:..........:=+###+-  .=#+. =:.                  
                 :.  .:::.  .-+#%#*=:   .-*#+. -*:.:                  
                   :-:.  .-#%#+-.   .-+#*+:  -*= :-                   
                 .:.   .+%#+:    :=+*+-.  :=+=. --                    
                      =%#-    :=++-:   .-+=:  :-.                     
                     +%-   .-==-.   .-==:   :-:                       
                    =*.   :=-.   .:--:   .:-:                         
                   :+    --.   .:-:    .::.                           
                   :    ::    .:.    .:.                              
                       :.    :.    ...                                
                      ..    :.    ..                                  
                                                                      """
    print(ascii_art)
    print("Welcome to DICMA. The Dictionary Maker: \n")

def verbose_print(input_string):
    global VERBOSE
    if VERBOSE == True:
        print(input_string)
    
def detec_if_file_or_not(input_to_check):
    path_ = input_to_check
    if os.path.isfile(path_):
        return True
    else:
        return False

def system_detection():
    if os.name == "nt":
        return "windows"
    else:
        return "linux"
        
def is_a_valid_file(file_path, blocksize=512):
    try:
        with open(file_path, 'rb') as file_:
            chunk = file_.read(8192)
        chunk.decode('latin-1')
        return True

    except UnicodeDecodeError:
        return False
    except Exception:
        return False

def save_list_to_file(list_, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for item in list_:
                f.write(f"{item}\n")
        verbose_print(f"[+] Dictionary saved successfully to: {filename}")
    except Exception as e:
        print(f"Error saving dictionary: {e}", file=sys.stderr)

def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

def ask_for_yes_or_no(question):
    while True:
        answer = input(question + " (yes/no): ").strip().lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            print("Please, answer 'yes' or 'no'.")

def generate_usernames(person_name):
    parts = person_name.strip().split()
    if len(parts) <= 1:
        return parts
    if len(parts) >= 3:
        print("[!] Unsuported names of 3 words -> " + str(person_name))
        sys.exit(1)
    name, suername = person_name.strip().split()
    first_let_name = name[0]
    first_let_surname = suername[0]

    combinations = [
        f"{name} {suername}",
        f"{name}{suername}",
        f"{first_let_name}{suername}",
        f"{name}{first_let_surname}",
        f"{name}.{suername}",
        f"{first_let_name}.{suername}",
        f"{name}.{first_let_surname}",
        f"{name}_{suername}",
        f"{first_let_name}_{suername}",
        f"{name}_{first_let_surname}",
        f"{name}-{suername}",
        f"{first_let_name}-{suername}",
        f"{name}-{first_let_surname}",
    ]

    return combinations


def normalize_list(input_):
    file_or_not = detec_if_file_or_not(input_)
    if file_or_not == True:
        with open(input_, 'r', encoding='utf-8') as file_:
            words_list = [line.strip() for line in file_ if line.strip()]
            return words_list
    else:
        raw_list = input_.strip().split(',')
        words_list = [word.strip() for word in raw_list if word.strip()]
        return words_list

def process_file_user(file_name, output_file_name):
    global OUTPUT_FILE_BULEAN
    with open(file_name, 'r', encoding='utf-8') as file_:
        if OUTPUT_FILE_BULEAN == False:
            for line_ in file_:
                line_ = line_.strip()
                if not line_:
                    continue  # Omitir líneas vacías
                combinations = generate_usernames(line_)
                for element in combinations:
                    print(element)
        else:
            complet_list = []
            for line_ in file_:
                line_ = line_.strip()
                if not line_:
                    continue  # Omitir líneas vacías
                combinations = generate_usernames(line_)
                for element in combinations:
                    complet_list.append(element)
            save_list_to_file(complet_list, output_file_name)  
    
def process_input_user(input_, output_file_name):
    global OUTPUT_FILE_BULEAN
    raw_list = input_.strip().split(',')
    people_list = [name.strip() for name in raw_list if name.strip()]
    final_list = []
    if OUTPUT_FILE_BULEAN == False:
        for name in people_list:
            final_list += generate_usernames(name) 
        for element in final_list:
            print(element) 
    else:
        for name in people_list:
            final_list += generate_usernames(name) 
        save_list_to_file(final_list, output_file_name)
  
def process_passwd(words_list, output_file_name):
    global OUTPUT_FILE_BULEAN
    global FULL_MODE
    global LIGHT_MODE
    verbose_print("[+] Creating dictionary.")
    
    # Checking for massive mode:
    if len(words_list) >= 2 and FULL_MODE == True:
        massive_mode(words_list, output_file_name)
        sys.exit(0)
    if len(words_list) >= 20 and LIGHT_MODE == False:
        massive_mode(words_list, output_file_name)
        sys.exit(0) 
    if len(words_list) >= 100:
        massive_mode(words_list, output_file_name)
        sys.exit(0)

    final_list = []
    if OUTPUT_FILE_BULEAN == False:
        for word in words_list:
            final_list += generate_password_list(word) 
        for element in final_list:
            print(element)
    else:
        for word in words_list:
            final_list += generate_password_list(word)
        save_list_to_file(final_list, output_file_name)
        
def find_neighbours(model,word,number):
    words = []
    words.append(word)
    pre_words = model.get_nearest_neighbors(word, k=number)
    semi_words = [text for _, text in pre_words]
    almost_words = [text for text in semi_words if '.' not in text]
    def valid(text):
        return all(not c.isupper() for c in text[1:])
    words += [text for text in almost_words if valid(text)]
    return words
    
def find_neighbours_windows(model, word, number): # CAREFULL, IS LOADING THE FULL MODEL FOR EVERY FUCKING WORD... THIS WILL NEED TO BE FIX...
    command = ["fasttext.exe", "nn", model, str(number)]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    exit, error = process.communicate(input=word + "\n")

    if error:
        print(f"Error while processing '{word}': {error}")
        return []

    neighbors = []
    neighbors.append(word)
    for line in exit.strip().splitlines():
        parts = line.strip().split()
        if len(parts) >= 1:
            neighbors.append(parts[0])
    semi_words = neighbors
    almost_words = [text for text in semi_words if '.' not in text]
    def valid(text):
        return all(not c.isupper() for c in text[1:])
    words = [text for text in almost_words if valid(text)]
    return words

def ml_process_pwd(list_, ml_model, number_neighbours):
    system_os = system_detection()
    if system_os == 'linux':
        try:
            import fasttext
            try:
                model = fasttext.load_model(ml_model)
                verbose_print("[+] Fasttext module loaded successfully.")
                if hasattr(ml_model, 'predict') and callable(ml_model.predict):
                    verbose_print("[+] Model loaded validated.")
            except Exception:
                print("[-] Sorry but doesn't looks like your input file is a valid ML model.")
                print("  You can get this Machine Learning traind models from this website:")
                print("  https://fasttext.cc/docs/en/pretrained-vectors.html")
                print("  You need the .bin file for the lenguage you want.")
                sys.exit(1)

            verbose_print("[+] Looking for the " + str(number_neighbours) + " nearest neighbours for each word.")
            words_list = []
            for word in list_:
                print("[+] Processing -> "+str(word))
                neighbors = find_neighbours(model, word, number_neighbours)
                for neighbor in neighbors:
                    words_list.append(neighbor)
            verbose_print("[+] Neighbors found successfully.")
            return words_list

        except ImportError:
            print("[-] Unable to load fasttext module. Plese install it:")
            print("  $ git clone https://github.com/facebookresearch/fastText.git\n  $ cd fastText\n  $ sudo pip install .")
            sys.exit(1)

    if system_os == 'windows':
        verbose_print('[!] Warning, this function is problematic in windows because "fasttext" library can not be compiled. We are going to use fasttext precompiled binary.')
        if os.path.isfile("fasttext.exe") == False:
            verbose_print("[!] fasttext.exe not found in present directory...")
            verbose_print('[!] We need to download an external fasttext.exe from -> https://github.com/sigmeta/fastText-Windows/releases/')
            if ask_for_yes_or_no("Do you accept ? (answer yes or no)") == True:
                
                # Check Write permisions actual at folder.
                if os.access(".", os.W_OK) == False:
                    print("[-] We don't have write permision in this folder. Move to a folder where you can write, or download fasttext.exe by yourself and move it to this folder.")
                    sys.exit(1)
                    
                # Download Windows binary
                url = 'https://github.com/sigmeta/fastText-Windows/releases/download/0.9.2/fasttext.exe'
                try:
                    urllib.request.urlretrieve(url, "fasttext.exe")
                    print("[+] Binary downloaded successfully")
                except urllib.error.HTTPError as e:
                    print(f"[-] Error HTTP -> {e.code} - {e.reason}")
                except urllib.error.URLError as e:
                    print(f"[-] Connection problem or file not available -> {e.reason}")
                except Exception as e:
                    print(f"[-] Unexpected error -> {e}")

            else:
                print("[-] Sorry but without this binary we won't be able to use fasttext model in Windows. Try to use dicma in linux, macos, or get this binary.")
                sys.exit(1)

        words_list = []
        for word in list_:
            print("[+] Processing -> "+str(word))
            neighbors = find_neighbours_windows(ml_model, word, number_neighbours)
            for neighbor in neighbors:
                words_list.append(neighbor)
        verbose_print("[+] Neighbors found successfully.")
        return words_list

        
def massive_mode(list_, output_file_name):
    global LIGHT_MODE
    global FULL_MODE
    global OUTPUT_FILE_BULEAN
    global MASSIVE_MODE
    
    verbose_print("[!] Massive mode ENABLED")
    VERBOSE = True
    if OUTPUT_FILE_BULEAN == False:
        output_file_name = "output.txt"
        verbose_print("[!] Output file required for the massive mode. Saving results to -> " + str(output_file_name))
    
    # Estimated file size
    output_size_lines = len(list_) * 900000
    if LIGHT_MODE == True:
        output_size_lines = len(list_) * 7700
    if FULL_MODE == True:
        output_size_lines = len(list_) * 8000000
    avg_line_size_bytes = 16
    estimated_size_bytes = output_size_lines * avg_line_size_bytes
    estimated_size_gb =  round(estimated_size_bytes / (1024 ** 3), 2)
    verbose_print("[+] Expected file size -> " + str(estimated_size_gb) + " GB / " + str(output_size_lines) + " Lines (aprox)")
    
    try:
        with open(output_file_name, 'w', encoding='utf-8') as f:
            for index, word in enumerate(list_):
                progress = (index + 1) / len(list_) * 100
                print(f"\r[+] Progress: {progress:.2f}%", end='', flush=True)
                temp_list = generate_password_list(word)
                f.write('\n'.join(temp_list) + '\n')

    except Exception as e:
        print(f"Error saving dictionary: {e}", file=sys.stderr)

    


def generate_password_list(word):
    global amount_of_sufixs_used
    global amount_of_prefixs_used
    global FULL_MODE
    global LIGHT_MODE
    
    if LIGHT_MODE == True:
        amount_of_sufixs_used = amount_of_sufixs_used_light_mode
        amount_of_prefixs_used = amount_of_prefixs_used_light_mode

    # GENERATING BASIC PATTERN:
    basic_pattern = []
    word = str(word).lower()
    word_no_punctuation = remove_accents(word)
    
    basic_pattern.append(word)
    basic_pattern.append(word.upper())
    basic_pattern.append(word.capitalize())
    basic_pattern.append(word_no_punctuation)
    basic_pattern.append(word_no_punctuation.upper())
    basic_pattern.append(word_no_punctuation.capitalize()) 

    basic_pattern = list(set(basic_pattern))
    
    transform_1 = [item.replace("a", "@").replace("A", "@") for item in basic_pattern]
    basic_pattern.extend(transform_1)
    transform_2 = [item.replace("o", "0").replace("O", "0") for item in basic_pattern]
    basic_pattern.extend(transform_2)
    if LIGHT_MODE == False:
        transform_3 = [item.replace("e", "€").replace("E", "€") for item in basic_pattern]
        basic_pattern.extend(transform_3)
        transform_4 = [item.replace("e", "3").replace("E", "3") for item in basic_pattern]
        basic_pattern.extend(transform_4)
        transform_5 = [item.replace("s", "$").replace("S", "$") for item in basic_pattern]
        basic_pattern.extend(transform_5)
        transform_6 = [item.replace("l", "1").replace("L", "1") for item in basic_pattern]
        basic_pattern.extend(transform_6)
    
    non_repeated_list = []
    for item in basic_pattern:
        if item not in non_repeated_list:
            non_repeated_list.append(item)
    
    # word + sufix
    word_sufixs = [a + b for a in basic_pattern for b in BASIC_SUFIXS[:amount_of_sufixs_used]]
    non_repeated_list.extend(word_sufixs)
    # prefix + word
    prefix_word = [a + b for a in BASIC_PREFIXS[:amount_of_prefixs_used] for b in basic_pattern]
    non_repeated_list.extend(prefix_word)    
    # prefix + word + sufix
    prefix_word_sufixs = [a + b + c for a in BASIC_PREFIXS[:amount_of_prefixs_used//3] for b in basic_pattern for c in BASIC_SUFIXS[:amount_of_sufixs_used//3]]
    non_repeated_list.extend(prefix_word_sufixs)
    
    # EXTENDED MODE:
    if FULL_MODE == True:
        # word + number
        word_number = [a + b for a in basic_pattern for b in NUMERIC_PATTERNS[:amount_of_numericpat_used]]
        non_repeated_list.extend(word_number)
        # word + simbol
        word_simbol = [a + b for a in basic_pattern for b in SYMBOLIC_PATTERNS[:amount_of_symbolpat_used]]
        non_repeated_list.extend(word_simbol)
        # word + number + simbol
        word_number_simbol = [a + b + c for a in basic_pattern for b in NUMERIC_PATTERNS[:amount_of_numericpat_used] for c in SYMBOLIC_PATTERNS[:amount_of_symbolpat_used]]
        non_repeated_list.extend(word_number_simbol)
        # word + simbol + number
        word_simbol_number = [a + b + c for a in basic_pattern for b in SYMBOLIC_PATTERNS[:amount_of_symbolpat_used] for c in NUMERIC_PATTERNS[:amount_of_numericpat_used]]
        non_repeated_list.extend(word_simbol_number)
        # simbol + word
        simbol_word = [a + b for a in SYMBOLIC_PATTERNS[:amount_of_symbolpat_used] for b in basic_pattern]
        non_repeated_list.extend(simbol_word)
        # number + word
        number_word = [a + b for a in NUMERIC_PATTERNS[:amount_of_numericpat_used] for b in basic_pattern]
        non_repeated_list.extend(number_word)
        # simbol + word + number
        simbol_word_number = [a + b + c for a in SYMBOLIC_PATTERNS[:amount_of_symbolpat_used] for b in basic_pattern for c in NUMERIC_PATTERNS[:amount_of_numericpat_used]]
        non_repeated_list.extend(simbol_word_number)
        # number + word + simbol
        number_word_simbol = [a + b + c for a in NUMERIC_PATTERNS[:amount_of_numericpat_used] for b in basic_pattern for c in SYMBOLIC_PATTERNS[:amount_of_symbolpat_used]]
        non_repeated_list.extend(number_word_simbol)
        
    non_repeated_list = list(dict.fromkeys(non_repeated_list))
    return non_repeated_list

def extract_patterns(file_input):
    sufixs = []
    prefixs = []
    numbers = []
    symbols = []

    with open(file_input, 'r', encoding='utf-8', errors='ignore') as file_:
        for linea in file_:
            linea = linea.strip()
            
            match = re.search(r'(?:[^\W\d]|-){3,}', linea, flags=re.UNICODE)
            if match:
                concept_start = match.start()
                concept_end = match.end()

                prefix = linea[:concept_start].strip()
                sufix = linea[concept_end:].strip()

                if prefix:
                    prefixs.append(prefix)
                if sufix:
                    sufixs.append(sufix)
            verbose_print("[+] Prefix and Sufix successfully extracted")

            found_numbers = re.findall(r'\d+', linea)
            numbers.extend(found_numbers)
            verbose_print("[+] Numeric patterns successfully extracted")

            found_symbols = re.findall(r'[^\w\s]+', linea, flags=re.UNICODE)
            symbols.extend(found_symbols)
            verbose_print("[+] Symbol patterns successfully extracted")

    sorted_sufixs = [item for item, count in Counter(sufixs).most_common() if count >= 2]
    sorted_prefixs = [item for item, count in Counter(prefixs).most_common() if count >= 2]
    sorted_numbers = [item for item, count in Counter(numbers).most_common() if count >= 2]
    sorted_symbols = [item for item, count in Counter(symbols).most_common() if count >= 2]

    return sorted_sufixs, sorted_prefixs, sorted_numbers, sorted_symbols


def main():
    global VERBOSE
    global LIGHT_MODE
    global FULL_MODE
    global OUTPUT_FILE_BULEAN
    global BASIC_SUFIXS
    global BASIC_PREFIXS
    global NUMERIC_PATTERNS
    global SYMBOLIC_PATTERNS
    global NEIGHBORS_AMMOUNT
    
    if len(sys.argv) == 1:
        print_banner()
    
    output_file_name = ''
    
    parser = argparse.ArgumentParser(description="Welcome to DICMA. The Dictionary Maker:")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--users', help='File with usernames, or usernames list: "jony random,fahim jordan,..."')
    group.add_argument('-p', '--password', help='file with words to "passworize", or list like: "ibis,megacorp,..."')

    parser.add_argument('-l', '--light', action='store_true', help='Light mode, for small list (passwd mode).')
    parser.add_argument('-f', '--full', action='store_true', help='Full mode. Warning, the output could be very heavy (passwd mode).')
    parser.add_argument('-nv','--no-verbose', action='store_true', help='Remove any output except the dictionary itself (Errors will be shown anyway).')
    parser.add_argument('-d','--dictionary', metavar='file_name', help='Extract patterns from your an specific dictionary.')
    parser.add_argument('-o', '--output', metavar='file_name', help='Dictionary will be stored in this file.')
    parser.add_argument('-ml', '--machine-learning-model', metavar='file_name', help='Use a trained machine learning model to include neighbors of your original words.')
    parser.add_argument('-n', '--neighbours-number', metavar='integer', help='Ammount of neighbors for each word (20 by Default).')

    args = parser.parse_args()
    
    if args.light == True and args.full == True:
        print('[!] Light mode and Full mode can not be at same time. Exiting...')
        sys.exit(1)
    if args.no_verbose:
        VERBOSE = False
    if args.light:
        LIGHT_MODE = True
        verbose_print("[+] Light mode enabled.")
    if args.full:
        FULL_MODE = True
        verbose_print("[+] Full mode enabled.")
        verbose_print("[!] Warning, the output could be very heavy.")
    if args.output:
        OUTPUT_FILE_BULEAN = True
        output_file_name = args.output
        verbose_print("[i] Dictionary will be stored in this file -> "+str(output_file_name))
        
    if args.dictionary is not None:
        if is_a_valid_file(args.dictionary):
            verbose_print("[+] Using "+str(args.dictionary)+" as a dictionary.")
        else:
            print("[!] File introduced as dictionary is not valid. Exiting...")
            sys.exit(1)
        dictionary = args.dictionary
        verbose_print("[+] Extracting patterns... this will take a minut.")
        BASIC_SUFIXS, BASIC_PREFIXS, NUMERIC_PATTERNS, SYMBOLIC_PATTERNS = extract_patterns(dictionary)
        verbose_print("[+] Patterns successfuly extracted, creating dictionary...")

    if args.users is not None:
        if args.machine_learning_model is not None:
            print("[-] Sorry, machine-learning-model option is not compatible with USERS mode, is only for PASSWORD mode.")
            sys.exit(1)
        if args.users.strip() == "":
            print("Error: This argument can not be empty", file=sys.stderr)
            sys.exit(1)
        verbose_print("[+] USER mode selected.")
        file_or_not = detec_if_file_or_not(args.users)
        if file_or_not == True:
            process_file_user(args.users, output_file_name)
            sys.exit(0)
        else:
            process_input_user(args.users, output_file_name)
            sys.exit(0)

    elif args.password is not None:
        if args.password.strip() == "":
            print("Error: This argument can not be empty", file=sys.stderr)
            sys.exit(1)
        input_list = normalize_list(args.password)
        
        if args.machine_learning_model is not None:                  # Section under development
            if detec_if_file_or_not(args.machine_learning_model) == False:
                print("[-] Your -ml <input> is not even a file...  ¬¬ , set a file here.")
                sys.exit(1)
            if args.neighbours_number is not None:
                NEIGHBORS_AMMOUNT = int(args.neighbours_number)
            ml_list = ml_process_pwd(input_list, args.machine_learning_model, NEIGHBORS_AMMOUNT)
            process_passwd(ml_list, output_file_name)
            sys.exit(0)

        verbose_print("[+] PASSWORD mode selected.")
        process_passwd(input_list, output_file_name)
        sys.exit(0)


if __name__ == "__main__":
    main()

    
    
    
    
    
    
