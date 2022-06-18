import sys
import os
import zip_helper
import re


def dataset_by_fn(fn):
    ds = re.search(r"/(.+?)/", fn).group()
    ds = ds[2:-1]
    return ds


# pa: 0=genuine, 1=paper including partial paper, 2=video 3=mask and makeup
def parse_label_by_filename(fn):

    """
        Return:
            0 genuine face
            1 paper (photo) attack (include paper mask from ROSE-YOUTU)
            2 replay attack
            3 mask attack


    """
    if re.fullmatch(r"/CASIA-FASD/(train_release|test_release)/(\d+)/(1|2|HR_1)\.avi", fn):
        return 0
    if re.fullmatch(r"/CASIA-FASD/(train_release|test_release)/(\d+)/(3|4|5|6|HR_2|HR_3)\.avi", fn):
        return 1
    if re.fullmatch(r"/CASIA-FASD/(train_release|test_release)/(\d+)/(7|8|HR_4)\.avi", fn):
        return 2

    if re.fullmatch(r"/Replay-Attack/enroll/(train|test|devel)/client(\d+)_(.+)\.mov", fn):
        return 0
    if re.fullmatch(r"/Replay-Attack/(train|test|devel)/real/client(\d+)_(.+)\.mov", fn):
        return 0
    if re.fullmatch(r"/Replay-Attack/(train|test|devel)/attack/(fixed|hand)/attack_print_(.+)\.mov", fn):
        return 1
    if re.fullmatch(r"/Replay-Attack/(train|test|devel)/attack/(fixed|hand)/attack_(mobile|highdef)_(.+)\.mov", fn):
        return 2

    if re.fullmatch(r"/OULU-NPU/(Train_files|Test_files|Dev_files)/(\d+)_(\d+)_(\d+)_1\.avi", fn):
        return 0
    if re.fullmatch(r"/OULU-NPU/(Train_files|Test_files|Dev_files)/(\d+)_(\d+)_(\d+)_(2|3)\.avi", fn):
        return 1
    if re.fullmatch(r"/OULU-NPU/(Train_files|Test_files|Dev_files)/(\d+)_(\d+)_(\d+)_(4|5)\.avi", fn):
        return 2

    if re.fullmatch(r"/ROSE-YOUTU/(train|test)/(_?)(\d+)/G_(.+)\.mp4", fn):
        return 0
    if re.fullmatch(r"/ROSE-YOUTU/(train|test)/(_?)(\d+)/(Mc_|Mf_|Mu_|Pq_|Ps_)(.+)\.mp4", fn):
        return 1
    if re.fullmatch(r"/ROSE-YOUTU/(train|test)/(_?)(\d+)/(Vl_|Vm_)(.+)\.mp4", fn):
        return 2

    if re.fullmatch(r"/SiW/(Train|Test)/live/(\d+)/(\d+)-(\d+)-(1)-(\d+)-(\d+)(\.m)?\.mov", fn):
        return 0
    if re.fullmatch(r"/SiW/(Train|Test)/spoof/(\d+)/(\d+)-(\d+)-(2)-(\d+)-(\d+)\.mov", fn):
        return 1
    if re.fullmatch(r"/SiW/(Train|Test)/spoof/(\d+)/(\d+)-(\d+)-(3)-(\d+)-(\d+)\.mov", fn):
        return 2

    if re.fullmatch(r"/SiW-60/(Train)/live/(\d+)/(\d+)-(\d+)-(1)-(\d+)-(\d+)\.mov", fn):
        return 0
    if re.fullmatch(r"/SiW-60/(Train)/spoof/(\d+)/(\d+)-(\d+)-(2)-(\d+)-(\d+)\.mov", fn):
        return 1
    if re.fullmatch(r"/SiW-60/(Train)/spoof/(\d+)/(\d+)-(\d+)-(3)-(\d+)-(\d+)\.mov", fn):
        return 2

    if re.fullmatch(r"/SiW-M/(Live/Train|Live/Test)/(.+)\.mov", fn):
        return 0
    if re.fullmatch(r"/SiW-M/(Paper|Partial/FunnyeyeGlasses|Partial/PaperCut|Partial/PaperGlasses)/(.+)\.mov", fn):
        return 1
    if re.fullmatch(r"/SiW-M/(Replay)/(.+)\.mov", fn):
        return 2
    if re.fullmatch(r"/SiW-M/(Makeup/Cosmetic|Makeup/Impersonation|Makeup/Obfuscation|Mask/HalfMask|Mask/MannequinHead|Mask/PaperMask|Mask/SiliconeMask|Mask/TransparentMask)/(.+)\.mov", fn):
        return 3



    if 'CASIA-SURF' in fn:
        return 0
    if 'CASIA-SURF' in fn:
        return 0


    if 'HKBU_MARs_V2' in fn and 'real' in fn:
        return 0
    if 'HKBU_MARs_V2' in fn and 'attack' in fn:
        return 3

#def get_info_from_file(fn):
#    info = zip_helper.read_bytes_from_zip_file(fn, "info.txt")
#    info = str(info, "utf-8")
#    face_count, frame_count = info.split()
#    face_count = int(face_count)
#    frame_count = int(frame_count)
#    return face_count, frame_count


def get_fns(root):
    fns = []
    for path, _, fns_in_path in os.walk(root):
        for fn in fns_in_path:

            _, ext = os.path.splitext(fn)

            if ext in [ '.png', '.jpg', '.mov', '.avi', '.mp4']:
                fn = os.path.join(path, fn)
                # fn = "/" + fn[fn.find("+"):].replace("\\", "/")
                fns.append(fn)
    return fns


def write_protocol_list_file(base_dir, fns, subset_name, regx):
    regx += r",(\d+),(\d+),(\d+)"
    filtered_fns = list(filter(lambda fn: re.fullmatch(regx, fn), fns))
    print(subset_name, "\t", len(filtered_fns))

    os.makedirs(base_dir + "/data_list/", exist_ok=True)
    with open(base_dir + "/data_list/" + subset_name + ".csv", "w") as f:
        for fn in filtered_fns:
            f.write(fn + "\n")

def write_protocol_list_file_txt(base_dir, fns, subset_name, regx):
    regx += r",(\d+),(\d+)"
    filtered_fns = list(filter(lambda fn: re.fullmatch(regx, fn), fns))
    print(subset_name, "\t", len(filtered_fns))

    os.makedirs(base_dir + "/data_list/", exist_ok=True)
    with open(base_dir + "/data_list/" + subset_name + ".csv", "w") as f:
        for fn in filtered_fns:
            f.write(fn + "\n")
            
    
    


def main():
    # get the base_dir
    # assert len(sys.argv) == 2
    # base_dir = sys.argv[1]
    base_dir = '/home/Dataset/data/Face_Spoofing/'
    assert os.path.exists(base_dir)
    print("base_dir", base_dir)

    fns = get_fns(base_dir)
    print(len(fns))

    summary = {}
    for i in range(len(fns)):
        fn = fns[i]
        ds = dataset_by_fn(fn)
        pa = parse_label_by_filename(fn)

        assert not "," in fn


    
    # write protocol files
    # write_protocol_list_file(base_dir, fns, "ALL", r"(.+)")

    # write_protocol_list_file(base_dir, fns, "CASIA-FASD", r"/CASIA-FASD/(.+)\.avi")
    # write_protocol_list_file(base_dir, fns, "Replay-Attack", r"/Replay-Attack/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "ROSE", r"/ROSE-YOUTU/(.+).mp4")
    # write_protocol_list_file(base_dir, fns, "ROSE-2019", r"/ROSE-2019/(.+).mp4")
    # write_protocol_list_file(base_dir, fns, "OULU-NPU", r"/OULU-NPU/(.+).avi")
    # write_protocol_list_file(base_dir, fns, "SiW", r"/SiW/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-60", r"/SiW-60/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-M", r"/SiW-M/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "CASIA-FASD-TRAIN", r"/CASIA-FASD/(train_release)/(.+)\.avi")
    # write_protocol_list_file(base_dir, fns, "CASIA-FASD-TEST", r"/CASIA-FASD/(test_release)/(.+)\.avi")

    # write_protocol_list_file(base_dir, fns, "Replay-Attack-TRAIN", r"/Replay-Attack((/enroll)?)/(train)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "Replay-Attack-DEV", r"/Replay-Attack((/enroll)?)/(devel)/(.+).mov")
    # write_protocol_list_file(base_dir, fns, "Replay-Attack-TEST", r"/Replay-Attack((/enroll)?)/(test)/(.+).mov")

    # write_protocol_list_file(base_dir, fns, "ROSE-TRAIN", r"/ROSE-YOUTU/(train)/(.+).mp4")
    # write_protocol_list_file(base_dir, fns, "ROSE-TEST", r"/ROSE-YOUTU/(test)/(.+).mp4")
    #write_protocol_list_file(base_dir, fns, "ROSE-REAL-ALL", r"/ROSE-YOUTU/(train|test)/(.+)/G(.+).mp4")
    #write_protocol_list_file(base_dir, fns, "ROSE-FAKE-ALL", r"/ROSE-YOUTU/(train|test)/(.+)/[^G](.+).mp4")

    write_protocol_list_file(base_dir, fns, "SiW-M", r"/SiW-M/(.+).mov")
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

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F1-TRAIN", r"/SiW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(2|3|4)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F1-TEST", r"/SiW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F2-TRAIN", r"/SiW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1|3|4)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F2-TEST", r"/SiW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(2)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F3-TRAIN", r"/SiW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1|2|4)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F3-TEST", r"/SiW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(3)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P2-F4-TRAIN", r"/SiW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(1|2|3)))-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P2-F4-TEST", r"/SiW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-((1-\d)|(3-(4)))-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P3-F1-TRAIN", r"/SiW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|2)-\d-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P3-F1-TEST", r"/SiW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|3)-\d-\d)((.m)?).mov")

    # write_protocol_list_file(base_dir, fns, "SiW-P3-F2-TRAIN", r"/SiW/(Train)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|3)-\d-\d)((.m)?).mov")
    # write_protocol_list_file(base_dir, fns, "SiW-P3-F2-TEST", r"/SiW/(Test)/(live|spoof)/(\d\d\d)/(\d\d\d-\d-(1|2)-\d-\d)((.m)?).mov")

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



if __name__ == "__main__":
    main()
