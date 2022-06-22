
import os
import re

# pa: 0=genuine, 1=paper including partial paper, 2=video 3=mask and makeup
def parse_label_by_filename(fn):

    """
        Return:
            0 genuine face
            1 paper (photo) attack (include paper mask from ROSE-YOUTU)
            2 replay attack
            3 mask attack


    """
    if bool(re.search(r"/CASIA-FASD/(train_release|test_release)/(\d+)/(1|2|HR_1)\.avi", fn)):
        return 0
    elif bool(re.search(r"/CASIA-FASD/(train_release|test_release)/(\d+)/(3|4|5|6|HR_2|HR_3)\.avi", fn)):
        return 1
    elif bool(re.search(r"/CASIA-FASD/(train_release|test_release)/(\d+)/(7|8|HR_4)\.avi", fn)):
        return 2

    if bool(re.search(r"/REPLAY-ATTACK/enroll/(train|test|devel)/client(\d+)_(.+)\.mov", fn)):
        return 0
    elif bool(re.search(r"/REPLAY-ATTACK/(train|test|devel)/real/client(\d+)_(.+)\.mov", fn)):
        return 0
    elif bool(re.search(r"/REPLAY-ATTACK/(train|test|devel)/attack/(fixed|hand)/attack_print_(.+)\.mov", fn)):
        return 1
    elif bool(re.search(r"/REPLAY-ATTACK/(train|test|devel)/attack/(fixed|hand)/attack_(mobile|highdef)_(.+)\.mov", fn)):
        return 2

    if bool(re.search(r"/OULU-NPU/(Train_files|Test_files|Dev_files)/(\d+)_(\d+)_(\d+)_1\.avi", fn)):
        return 0
    elif bool(re.search(r"/OULU-NPU/(Train_files|Test_files|Dev_files)/(\d+)_(\d+)_(\d+)_(2|3)\.avi", fn)):
        return 1
    elif bool(re.search(r"/OULU-NPU/(Train_files|Test_files|Dev_files)/(\d+)_(\d+)_(\d+)_(4|5)\.avi", fn)):
        return 2

    if bool(re.search(r"/ROSE-YOUTU/(train|test)/(_?)(\d+)/G_(.+)\.mp4", fn)):
        return 0
    elif bool(re.search(r"/ROSE-YOUTU/(train|test)/(_?)(\d+)/(Mc_|Mf_|Mu_|Pq_|Ps_)(.+)\.mp4", fn)):
        return 1
    elif bool(re.search(r"/ROSE-YOUTU/(train|test)/(_?)(\d+)/(Vl_|Vm_)(.+)\.mp4", fn)):
        return 2

    if bool(re.search(r"/SiW/(Train|Test)/live/(\d+)/(\d+)-(\d+)-(1)-(\d+)-(\d+)(\.m)?\.mov", fn)):
        return 0
    elif bool(re.search(r"/SiW/(Train|Test)/spoof/(\d+)/(\d+)-(\d+)-(2)-(\d+)-(\d+)\.mov", fn)):
        return 1
    elif bool(re.search(r"/SiW/(Train|Test)/spoof/(\d+)/(\d+)-(\d+)-(3)-(\d+)-(\d+)\.mov", fn)):
        return 2

    if bool(re.search(r"/SiW-60/(Train)/live/(\d+)/(\d+)-(\d+)-(1)-(\d+)-(\d+)\.mov", fn)):
        return 0
    elif bool(re.search(r"/SiW-60/(Train)/spoof/(\d+)/(\d+)-(\d+)-(2)-(\d+)-(\d+)\.mov", fn)):
        return 1
    elif bool(re.search(r"/SiW-60/(Train)/spoof/(\d+)/(\d+)-(\d+)-(3)-(\d+)-(\d+)\.mov", fn)):
        return 2

    if bool(re.search(r"/SiW-M/(Live/Train|Live/Test)/(.+)\.mov", fn)):
        return 0
    elif bool(re.search(r"/SiW-M/(Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses)/(.+)\.mov", fn)):
        return 1
    elif bool(re.search(r"/SiW-M/(Replay)/(.+)\.mov", fn)):
        return 2
    elif bool(re.search(r"/SiW-M/(Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask)/(.+)\.mov", fn)):
        return 3



    if 'CASIA-SURF-CVPR2019' in fn and 'real_part' in fn:
        return 0
    elif 'CASIA-SURF-CVPR2019' in fn and 'fake_part'in fn:
        return 1


    if 'HKBU_MARs_V2' in fn and 'real' in fn:
        return 0
    elif 'HKBU_MARs_V2' in fn and 'attack' in fn:
        return 3

    if 'CelebA-Spoof' in fn and 'live' in fn:
        return 0
    elif 'CelebA-Spoof' in fn and 'spoof' in fn:
        return 1



    if bool(re.search('(.+)CeFA(.+)\d_\d\d\d_\d_\d_1/(.+)', fn)):
        return 0
    elif bool(re.search('(.+)CeFA(.+)\d_\d\d\d_\d_\d_3/(.+)', fn)):
        # Photo
        return 1
    elif bool(re.search('(.+)CeFA(.+)\d_\d\d\d_\d_\d_4/(.+)', fn)):
        # Screen
        return 2
    elif bool(re.search('(.+)CeFA(.+)\d_\d\d\d_\d_\d_2/(.+)', fn)):
        # Cloth
        return 3

    if 'CelabA-Spoof' in fn and 'live' in fn:
        return 0
    elif 'CelabA-Spoof' in fn and 'spoof' in fn:
        return 1



def get_filenames_under_base_dir(base_dir):
    fns = []
    for path, _, fns_in_path in os.walk(base_dir):
        for fn in fns_in_path:

            _, ext = os.path.splitext(fn)

            if ext in [ '.png', '.jpg', '.mov', '.avi', '.mp4']:
                fn = os.path.join(path, fn)
                # fn = "/" + fn[fn.find("+"):].replace("\\", "/")
                fns.append(fn)
    return fns


def write_protocol_list_file(base_dir, subset_name, regx, output_dir='./'):

    fns = get_filenames_under_base_dir(base_dir)
    filtered_fns = list(filter(lambda fn: re.fullmatch(regx, fn), fns))

    print("#all file under {} | #files of {}={}".format(len(fns), subset_name,len(filtered_fns)))
    os.makedirs(output_dir + "/data_list/", exist_ok=True)

    data_list_file_path = os.path.join(output_dir,"data_list",  subset_name + ".csv")
    print("Write data list to {}".format(data_list_file_path))
    with open(data_list_file_path, "w") as f:
        for fn in filtered_fns:
            label = parse_label_by_filename(fn)
            f.write(fn + ',' + str(label) + "\n")


if __name__ == "__main__":


    # CASIA-FASD
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/CASIA-FASD', subset_name="CASIA-FASD-ALL", regx=r"(.+)/CASIA-FASD/(.+)\.png")
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/CASIA-FASD', subset_name="CASIA-FASD-TRAIN", regx=r"(.+)/CASIA-FASD/train_release/(.+)\.png")
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/CASIA-FASD', subset_name="CASIA-FASD-TEST", regx=r"(.+)/CASIA-FASD/test_release/(.+)\.png")

    # NTU ROSE-YOUTU
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-TRAIN",
                             regx=r"(.+)/ROSE-YOUTU/(train)/(.+)\.png")
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-TEST",
                             regx=r"(.+)/ROSE-YOUTU/(test)/(.+)\.png")
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-REAL-ALL",
                             regx=r"(.+)/ROSE-YOUTU/(train|test)/(.+)/G(.+)\.png")
    write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-FAKE-ALL",
                             regx=r"(.+)/ROSE-YOUTU/(train|test)/(.+)/[^G](.+)\.png")


    # write_protocol_list_file(base_dir, fns, "ROSE-TRAIN", r"/ROSE-YOUTU/(train)/(.+).mp4")
    # write_protocol_list_file(base_dir, fns, "ROSE-TEST", r"/ROSE-YOUTU/(test)/(.+).mp4")
    # write_protocol_list_file(base_dir, fns, "ROSE-REAL-ALL", r"/ROSE-YOUTU/(train|test)/(.+)/G(.+).mp4")
    # write_protocol_list_file(base_dir, fns, "ROSE-FAKE-ALL", r"/ROSE-YOUTU/(train|test)/(.+)/[^G](.+).mp4")

    #write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/REPLAY-ATTACK', subset_name="REPLAY-ATTACK-ALL", regx=r"(.+)/REPLAY-ATTACK/(.+)png")
    #write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-ALL", regx=r"(.+)/ROSE-YOUTU/(.+)png")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU", r"/OULU-NPU/(.+).avi")
    # write_protocol_list_file(base_dir, fns, "SiW", r"/SiW/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-60", r"/SiW-60/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M", r"/SiW-M/(.+).mov")


    # write_protocol_list_file(base_dir, fns, "Replay-Attack-TRAIN", r"/Replay-Attack((/enroll)?)/(train)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "Replay-Attack-DEV", r"/Replay-Attack((/enroll)?)/(devel)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "Replay-Attack-TEST", r"/Replay-Attack((/enroll)?)/(test)/(.+).mov")



    # write_protocol_list_file(base_dir, fns, "SiW-M", r"/SiW-M/(.+).mov")
    # # phone_session_subject_attack.avi   attack:1 live, 2 printer1, 3 printer2, 4 display 1, 5 display 2
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-TRAIN", r"/OULU-NPU/(Train_files)/(\d+)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-DEV", r"/OULU-NPU/(Dev_files)/(\d+)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-TEST", r"/OULU-NPU/(Test_files)/(\d+)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P1-TRAIN", r"/OULU-NPU/(Train_files)/(\d+)_(1|2)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P1-DEV", r"/OULU-NPU/(Dev_files)/(\d+)_(1|2)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P1-TEST", r"/OULU-NPU/(Test_files)/(\d+)_(3)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P2-TRAIN", r"/OULU-NPU/(Train_files)/(\d+)_(\d+)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P2-DEV", r"/OULU-NPU/(Dev_files)/(\d+)_(\d+)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P2-TEST", r"/OULU-NPU/(Test_files)/(\d+)_(\d+)_(\d+)_(1|3|5).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F1-TRAIN", r"/OULU-NPU/(Train_files)/(2|3|4|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F1-DEV", r"/OULU-NPU/(Dev_files)/(2|3|4|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F1-TEST", r"/OULU-NPU/(Test_files)/(1)_(\d+)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F2-TRAIN", r"/OULU-NPU/(Train_files)/(1|3|4|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F2-DEV", r"/OULU-NPU/(Dev_files)/(1|3|4|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F2-TEST", r"/OULU-NPU/(Test_files)/(2)_(\d+)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F3-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|4|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F3-DEV", r"/OULU-NPU/(Dev_files)/(1|2|4|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F3-TEST", r"/OULU-NPU/(Test_files)/(3)_(\d+)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F4-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|3|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F4-DEV", r"/OULU-NPU/(Dev_files)/(1|2|3|5|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F4-TEST", r"/OULU-NPU/(Test_files)/(4)_(\d+)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F5-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|3|4|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F5-DEV", r"/OULU-NPU/(Dev_files)/(1|2|3|4|6)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F5-TEST", r"/OULU-NPU/(Test_files)/(5)_(\d+)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F6-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|3|4|5)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F6-DEV", r"/OULU-NPU/(Dev_files)/(1|2|3|4|5)_(\d+)_(\d+)_(\d+).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P3-F6-TEST", r"/OULU-NPU/(Test_files)/(6)_(\d+)_(\d+)_(\d+).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F1-TRAIN", r"/OULU-NPU/(Train_files)/(2|3|4|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F1-DEV", r"/OULU-NPU/(Dev_files)/(2|3|4|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F1-TEST", r"/OULU-NPU/(Test_files)/(1)_(3)_(\d+)_(1|3|5).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F2-TRAIN", r"/OULU-NPU/(Train_files)/(1|3|4|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F2-DEV", r"/OULU-NPU/(Dev_files)/(1|3|4|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F2-TEST", r"/OULU-NPU/(Test_files)/(2)_(3)_(\d+)_(1|3|5).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F3-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|4|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F3-DEV", r"/OULU-NPU/(Dev_files)/(1|2|4|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F3-TEST", r"/OULU-NPU/(Test_files)/(3)_(3)_(\d+)_(1|3|5).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F4-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|3|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F4-DEV", r"/OULU-NPU/(Dev_files)/(1|2|3|5|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F4-TEST", r"/OULU-NPU/(Test_files)/(4)_(3)_(\d+)_(1|3|5).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F5-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|3|4|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F5-DEV", r"/OULU-NPU/(Dev_files)/(1|2|3|4|6)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F5-TEST", r"/OULU-NPU/(Test_files)/(5)_(3)_(\d+)_(1|3|5).avi")

    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F6-TRAIN", r"/OULU-NPU/(Train_files)/(1|2|3|4|5)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F6-DEV", r"/OULU-NPU/(Dev_files)/(1|2|3|4|5)_(1|2)_(\d+)_(1|2|4).avi")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU-P4-F6-TEST", r"/OULU-NPU/(Test_files)/(6)_(3)_(\d+)_(1|3|5).avi")

    # # SubjectID_SensorID_AttackTypeID(1 live 2 paper 3 replay)_MediumID_SessionID
    # write_protocol_list_file(base_dir, fns, "SiW-P1-TRAIN", r"/SiW-60/(Train)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P1-TEST", r"/SiW/(Test)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F1-TRAIN", r"/SIW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(2|3|4)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F1-TEST", r"/SIW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F2-TRAIN", r"/SIW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1|3|4)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F2-TEST", r"/SIW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(2)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F3-TRAIN", r"/SIW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1|2|4)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F3-TEST", r"/SIW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(3)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F4-TRAIN", r"/SIW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1|2|3)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F4-TEST", r"/SIW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(4)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P3-F1-TRAIN", r"/SIW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|2)-\d-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P3-F1-TEST", r"/SIW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|3)-\d-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P3-F2-TRAIN", r"/SIW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|3)-\d-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P3-F2-TEST", r"/SIW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|2)-\d-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F1-TRAIN", r"/SiW-M/(Live/Train|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F1-TEST", r"/SiW-M/(Live/Test|Makeup/Cosmetic)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F2-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F2-TEST", r"/SiW-M/(Live/Test|Makeup/Impersonation)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F3-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F3-TEST", r"/SiW-M/(Live/Test|Makeup/Obfuscation)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F4-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F4-TEST", r"/SiW-M/(Live/Test|Mask/HalfMask)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F5-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F5-TEST", r"/SiW-M/(Live/Test|Mask/MannequinHead)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F6-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F6-TEST", r"/SiW-M/(Live/Test|Mask/PaperMask)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F7-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F7-TEST", r"/SiW-M/(Live/Test|Mask/SiliconeMask)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F8-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F8-TEST", r"/SiW-M/(Live/Test|Mask/TransparentMask)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F9-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F9-TEST", r"/SiW-M/(Live/Test|Paper)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F10-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/PaperCut|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F10-TEST", r"/SiW-M/(Live/Test|Partial/FunnyeyeGlasses)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F11-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperGlasses|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F11-TEST", r"/SiW-M/(Live/Test|Partial/PaperCut)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F12-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F12-TEST", r"/SiW-M/(Live/Test|Partial/PaperGlasses)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F13-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F13-TEST", r"/SiW-M/(Live/Test|Replay)/(.+).mov")

    # Grandtest protocol
    # write_protocol_list_file(base_dir, fns, "WMCA-P1-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "WMCA-P1-TEST", r"/SiW-M/(Live/Test|Partial/PaperGlasses)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "WMCA-P1-DEV", r"/SiW-M/(Live/Test|Partial/PaperGlasses)/(.+).mov")

    # Unseen attack protocols
    # write_protocol_list_file(base_dir, fns, "WMCA-P2-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Replay)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "WMCA-P2-TEST", r"/SiW-M/(Live/Test|Partial/PaperGlasses)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "WMCA-P2-DEV", r"/SiW-M/(Live/Test|Partial/PaperGlasses)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-M-F13-TRAIN", r"/SiW-M/(Live/Train|Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask|Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M-F13-TEST", r"/SiW-M/(Live/Test|Replay)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "CASIA_SURF_COLOR_ALL", r"/(.+)/color/(.+).jpg")
    # write_protocol_list_file(base_dir, fns, "CASIA_SURF_COLOR_TRAIN", r"/(.+)train(.+)color/(.+).jpg")
    # write_protocol_list_file(base_dir, fns, "CASIA_SURF_COLOR_VAL", r"/(.+)val(.+)/color/(.+).jpg")
    # write_protocol_list_file(base_dir, fns, "CASIA_SURF_COLOR_TEST", r"/(.+)test(.+)/color/(.+).jpg")

    # TODO: CeFA
    # write_protocol_list_file(base_dir, fns, "CeFA_RGB_ALL", r"/(.+)/profile/0001.jpg")
    # write_protocol_list_file(base_dir, fns, "CeFA_RGB_TRAIN", r"(.+)/\d_(0\d\d|00\d|1\d\d|200)_\d_\d_\d/profile/0001.jpg")
    # write_protocol_list_file(base_dir, fns, "CeFA_RGB_DEV", r"(.+)/\d_(20[1-9]|2[1-9]\d|300)_\d_\d_\d/profile/0001.jpg")
    # write_protocol_list_file(base_dir, fns, "CeFA_RGB_TEST", r"(.+)/\d_(3\d[1-9]|[4-5]\d\d)_\d_\d_\d/profile/0001.jpg")

    # CelebA_Spoof
    #write_protocol_list_file(base_dir, fns, "CelebASpoof_TRAIN", r"/(.+)train/(.+)*.jpg")
    #write_protocol_list_file(base_dir, fns, "CelebASpoof_TEST", r"/(.+)test/(.+)*.jpg")

    # CASIA-SURF
    #write_protocol_list_file(base_dir, fns, "CASIA_SURF_TRAIN", r"/(.+)train_part(.+)color/(.+)*.jpg")
    #write_protocol_list_file(base_dir, fns, "CASIA_SURF_TEST", r"/(.+)test_part(.+)/color/(.+)*.jpg")
