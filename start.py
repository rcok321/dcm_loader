import glob
import os
from dataLoader import data_loader

def test(imshow = False, input_path = os.getcwd(),output_path = os.path.join(os.getcwd(),'straightened')):
    file_list = glob.glob(os.path.join(input_path,'*.dcm'),recursive=False)
    total_file_count = str(len(file_list))
    print('==================== Total {total_file_count} files ===================='.format(total_file_count=total_file_count))
    for index, file_path in enumerate(file_list): 
        print('({Nth_file} / {total_file_count})------Start to read...............'.format(Nth_file=str(index+1).zfill(len(total_file_count)),total_file_count=total_file_count), end = '\r')
        dcm_data = data_loader(file_path)
        print('({Nth_file} / {total_file_count})------Straightening...............'.format(Nth_file=str(index+1).zfill(len(total_file_count)),total_file_count=total_file_count), end = '\r')
        dcm_data.img_straighten()
        if imshow:
            print('({Nth_file} / {total_file_count})------Close Window to Continue!!!'.format(Nth_file=str(index+1).zfill(len(total_file_count)),total_file_count=total_file_count), end = '\r')
            dcm_data.img_show()
        dcm_data.dcmwrite(output_path)
        print('({Nth_file} / {total_file_count})------Saving...............'.format(Nth_file=str(index+1).zfill(len(total_file_count)),total_file_count=total_file_count), end = '\r')
    print('============ End. Total processed {total_file_count} files. ============'.format(total_file_count=total_file_count))

if __name__ == '__main__':
    test(imshow = True) # set imshow True to show image Before/After.