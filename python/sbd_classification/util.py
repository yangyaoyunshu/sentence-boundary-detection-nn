import common.sbd_config as sbd
import caffe, os
from tools.netconfig import NetConfig
from os import listdir
from sbd_classification.lexical_classification import LexicalClassifier
from sbd_classification.audio_classification import AudioClassifier
from preprocessing.nlp_pipeline import PosTag

def get_index(index, length, punctuation_pos):
    position = index - punctuation_pos + 1
    if 0 <= position < length:
        return position
    else:
        return -1

def convert_probabilities(token_length, punctuation_pos, probabilities, classes = ["NONE", "COMMA", "PERIOD"]):
    new_probablities = []
    for i in range(0, token_length):
        current_prediction_position = get_index(i, len(probabilities), punctuation_pos)
        if i == token_length - 1:
            new_probablities.append([(1.0 if current == "PERIOD" else 0.0) for current in classes])
        elif current_prediction_position < 0:
            new_probablities.append([(1.0 if current == "NONE" else 0.0) for current in classes])
        else:
            new_probablities.append(probabilities[current_prediction_position].tolist())
    print probabilities, new_probablities
    return new_probablities

def get_filenames(folder):
    for file_ in listdir(folder):
        if file_.endswith(".ini"):
            config_file = folder + "/" + file_
        elif file_.endswith(".caffemodel"):
            caffemodel_file = folder + "/" + file_
        elif file_ == "net.prototxt":
            net_proto = folder + "/" + file_
    return config_file, caffemodel_file, net_proto

def make_lexical_temp_deploy(folder, prototxt, temp_file_name = "temp_deploy.prototxt"):
    WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
    FEATURE_LENGTH = 300 if not sbd.config.getboolean('features', 'pos_tagging') else 300 + len(PosTag)

    with file(prototxt, "r") as input_:
        nc = NetConfig(input_)
    nc.transform_deploy([1, 1, WINDOW_SIZE, FEATURE_LENGTH])
    temp_proto = "%s/%s" % (folder, temp_file_name)
    with file(temp_proto, "w") as output:
        nc.write_to(output)

    return temp_proto

def make_audio_temp_deploy(folder, prototxt, temp_file_name = "temp_deploy.prototxt"):
    WINDOW_SIZE = sbd.config.getint('windowing', 'window_size')
    FEATURE_LENGTH = 4

    with file(prototxt, "r") as input_:
        nc = NetConfig(input_)
    nc.transform_deploy([1, 1, WINDOW_SIZE, FEATURE_LENGTH])
    temp_proto = "%s/%s" % (folder, temp_file_name)
    with file(temp_proto, "w") as output:
        nc.write_to(output)

    return temp_proto

def load_lexical_classifier(folder, vector):
    print('Loading config folder: ' + folder)

    config_file, caffemodel_file, net_proto = get_filenames(folder)

    sbd.SbdConfig(config_file)
    temp_proto = make_lexical_temp_deploy(folder, net_proto)

    net = caffe.Net(temp_proto, caffemodel_file, caffe.TEST)

    if vector:
        classifier = LexicalClassifier(net, vector)
    else:
        classifier = LexicalClassifier(net, vector)

    return classifier

def load_audio_classifier(folder):
    print('Loading config folder: ' + folder)

    config_file, caffemodel_file, net_proto = get_filenames(folder)

    sbd.SbdConfig(config_file)
    temp_proto = make_audio_temp_deploy(folder, net_proto)

    net = caffe.Net(temp_proto, caffemodel_file, caffe.TEST)

    classifier = AudioClassifier(net)

    return classifier

def get_audio_files(folder):
    ctm_file = None
    pitch_file = None
    energy_file = None

    for file_ in listdir(folder):
        if file_.endswith(".ctm"):
            ctm_file = os.path.join(folder, file_)
        elif file_.endswith(".pitch"):
            pitch_file = os.path.join(folder, file_)
        elif file_.endswith(".energy"):
            energy_file = os.path.join(folder, file_)

    return ctm_file, pitch_file, energy_file
