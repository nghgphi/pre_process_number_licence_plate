import cv2
import os
import numpy as np
import string
def number_of_elemnts(arr):
    d = 0
    for i in arr:
        d += 1
    return d
error_letter = {'6':['G', 'O'],
                '7':['T','Z'],
                '8':['G'],
                '1':['I', 'L', 'J'],
                '2':['Z'],
                '3':['E', 'F'],
                '4':['A'],
                '5':['S'],
                '9':['O',],
                '0':['O','D','Q','G']}
error_digit = {'A':['4'],
                'B':['8','9'],
                'C':['6','0'],
                'D':['0'],
                'E':['3'],
                'F':['3'],
                'G':['6','0'],
                'I':['1','7'],
                'J':['1','7'],
                'K':['4'],
                'L':['1'],
                'O':['0','8','9','6'],
                'Q':['0'],
                'S':['5'],
                'Z':['2'],
                'T':['7','1']
                }


path_folder_2 = "raw_data/03/"
path_result_2 = "raw_data/crop/"

f = open('test_output.txt','w')

sample_lnb = []

for image in os.listdir(path_folder_2):
    # try: 
        image_path = path_folder_2 + image
        # src = cv2.imread(image_path)

        #lọc ảnh:
        pos = []
        
        for i in range(len(image)):
        
            if image[i] == '_':
                pos.append(i)
        
        sample_lnb.append(int(image[pos[0]+1:pos[1]]))
        # group_name.append(image[pos[3]+1:pos[4]])
        # if int(image[pos[0]+1:pos[1]]) == 2893:
        #     print(image)
        
        # f.write(str(image[pos[3]+1:pos[4]])+'\n')
        
sample_lnb = list(set(sample_lnb)) # sample_lnb giờ là 1 list chứa tên các nhóm biển số
m = 0
for number in sample_lnb:
    
    group_temp = [] # chứa nhãn dự đoán của ảnh được máy tính thực hiện
    confi_temp = [] # chứa độ tự tin dự đoán nhãn trên
    images_temp = [] # chứa toàn bộ tên của ảnh 
    for img in os.listdir(path_folder_2):
        # try:
        pos_temp = []

        for i in range(len(img)):               
                if img[i] == '_':
                    pos_temp.append(i)
            
        if number == int(img[pos_temp[0]+1:pos_temp[1]]):
                images_temp.append(img)
                group_temp.append(img[pos_temp[3]+1:pos_temp[4]])
                confi_temp.append(float(img[pos_temp[4]+1:pos_temp[5]]))
                vehicle_temp = img[pos_temp[2]+1:pos_temp[3]]
                # confi_temp = np.array(confi_temp)               

    # print(group_temp)

    if number_of_elemnts(confi_temp) == 1:
            name_satisfied  = images_temp[0]

            src = cv2.imread(path_folder_2 + name_satisfied)
            cv2.imwrite(path_result_2 + name_satisfied, src)

            # f.write('\n' + path_result_2 + name_satisfied)
    elif number_of_elemnts(confi_temp) >= 2:
        m = m + 1

        confi_temp_check = []
        for i in range(number_of_elemnts(confi_temp)):
            confi_temp_check.append(confi_temp[i] > 0.9)
        # f.write(images_temp[confi_temp.index(max(confi_temp))] + '\n')
        if all(confi_temp_check) > 0.9:

                for i in confi_temp:
                    src = cv2.imread(path_folder_2 + images_temp[confi_temp.index(i)])
                    cv2.imwrite(path_result_2 + images_temp[confi_temp.index(i)], src)
                    # f.write('\n' + path_result_2 + images_temp[confi_temp.index(i)])

        else:           
            confi_idx_max = confi_temp.index(max(confi_temp))
            # f.write(images_temp[confi_temp.index(max(confi_temp))] + '\n')

            if len(group_temp[confi_idx_max]) == 8 or len(group_temp[confi_idx_max]) == 9:
                
                label = group_temp[confi_idx_max]
                fix_image = images_temp[confi_idx_max]
                src_1 = cv2.imread(path_folder_2 + fix_image)
                label_fixed = group_temp[confi_idx_max]
                
                for key_letter, key_digit in zip(error_letter, error_digit):
                    
                    for j in range(len(label)):

                            if j == 2 and label[j] == key_letter:
                    
                                can_be_fix = []
                                
                                for i in range(len(group_temp)):
                                    if len(group_temp[i]) > 2:
                                        if group_temp[i][2] in error_letter[key_letter]:
                                            can_be_fix.append(group_temp[i][2])
                                
                                if number_of_elemnts(can_be_fix) > 0:
                                    letter = max(set(can_be_fix), key= can_be_fix.count)

                                    label_fixed = label.replace(label[j], letter, 1)
                                else:
                                    label_fixed = label.replace(label[j], error_letter[key_letter][0], 1)
                        
                                fix_image = images_temp[confi_idx_max].replace(label, label_fixed, 1)
                            
                            
                            elif label[j] == key_digit and j != 2:
                                can_be_fix = []
                                
                                for i in range(len(group_temp)):
                                    if len(group_temp[i]) > j:
                                        if group_temp[i][j] in error_digit[key_digit]:
                                            can_be_fix.append(group_temp[i][j])
                                
                                if number_of_elemnts(can_be_fix) > 0:
                                    letter = max(set(can_be_fix), key= can_be_fix.count)

                                    label_fixed = label.replace(label[j], letter, 1)
                                else:
                                    label_fixed = label.replace(label[j], error_digit[key_digit][0], 1)
                                fix_image = images_temp[confi_idx_max].replace(label, label_fixed, 1)


                            elif label[j] == key_letter and j != 2:
                                can_be_fix = []
                            
                                for i in range(len(group_temp)):
                                    if len(group_temp[i]) > j:
                                        if group_temp[i][j].isdigit():
                                            can_be_fix.append(group_temp[i][j])
                                if number_of_elemnts(can_be_fix) > 0:
                                    letter = max(set(can_be_fix), key= can_be_fix.count)
                                
                                    label_fixed = label.replace(label[j], letter, 1)
                                    
                                fix_image = images_temp[confi_idx_max].replace(label, label_fixed, 1)

                            
                            elif label[j] == key_digit and j == 2:
                                can_be_fix = []

                                for i in range(len(group_temp)):
                                    if len(group_temp[i]) > 2:
                                        if group_temp[i][2].isalpha():
                                            can_be_fix.append(group_temp[i][2])
                                if number_of_elemnts(can_be_fix) > 0:
                                    letter = max(set(can_be_fix), key= can_be_fix.count)

                                    label_fixed = label.replace(label[j], letter, 1)
                                # else:
                                #     label_fixed = label.replace(label[2], error_digit[key_digit][0], 1)
                                fix_image = images_temp[confi_idx_max].replace(label, label_fixed, 1)

                            
                # f.write('\n' + path_result_2 + fix_image )
                cv2.imwrite(path_result_2 + fix_image, src_1)
            elif len(group_temp[confi_idx_max]) < 8:
                src_2 = cv2.imread(path_folder_2 + images_temp[confi_temp.index(max(confi_temp))])
                # cv2.imwrite(path_result_2 + images_temp[confi_temp.index(max(confi_temp))], src_2)
                    
                # f.write('\n' +  path_result_2 + images_temp[confi_temp.index(max(confi_temp))])


                # path_folder = "sudoku\\data\\"
                # path_result = "sudoku\\result\\"



                        # while not_ok and i < len(error[key]):
                            
                        #     label.replace(label[2],error[key][i])
                            
                        #     i = i + 1

        # confi_temp_np = np.array(confi_temp,np.float)

    # if confi_temp_np.all() > 0.85:
    #     max_confi = max_index(confi_temp)
    #     src = cv2.imread(path_folder_2 + images_temp[max_confi])
    #     cv2.imwrite(path_result_2 + images_temp[max_confi], src)
    
print(m)
f.close()
