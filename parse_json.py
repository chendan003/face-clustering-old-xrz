import json
import os
import os.path as osp
import numpy as np
import urllib2

import base64

from unpack_stream_to_float32 import unpack_feature_from_stream


def convert_json_file_to_npy(jsonFile):
    jsonDict = load_json_file(jsonFile)
    featId = jsonDict['faces'][0]['featId']
    featPath = './' + featId
    try:
        os.makedirs(featPath)
    except:
        pass
    for individualDict in jsonDict['faces']:
        individual_to_npy(individualDict, featPath)
    return featPath


def downloadPic(picUrl, path):
    response = urllib2.urlopen(picUrl)
    pic = response.read()
    picName = picUrl.split('/')[-1]
    with open(path + '/' + picName, 'wb') as f:
        f.write(pic)
        f.close()
    return


def load_json_file(filePath):
    with open(filePath, 'r') as f:
        jsonString = f.read()
        return json.loads(jsonString)


def code_feature_to_npy(jsonString):
    return unpack_feature_from_stream(jsonString)


def individual_to_npy(individualDict, featPath):
    id = individualDict['id']
    individualPath = featPath + '/' + id
    try:
        os.makedirs(individualPath)
    except:
        pass
    for singlePicDict in individualDict['features']:
        downloadPic(singlePicDict['faceUri'], individualPath)
        picName = singlePicDict['faceUri'].split('/')[-1]

        b64_dat_fn = osp.join(individualPath, picName + '_b64.dat')
        dat_fn = osp.join(individualPath, picName + '.dat')

        fp = open(b64_dat_fn, 'w')
        fp.write(singlePicDict['data'])
        fp.close()

        decoded_stream = base64.decodestring(singlePicDict['data'])
        fp = open(dat_fn, 'wb')
        fp.write(decoded_stream)
        fp.close()

        npyFeature = code_feature_to_npy(singlePicDict['data'])
        npyFeature = np.asarray(npyFeature, dtype=np.float32)
        np.save(file=individualPath + '/' + picName, arr=npyFeature)
    return


if __name__ == "__main__":
    convert_json_file_to_npy('feat1.json')
    convert_json_file_to_npy('feat2.json')
